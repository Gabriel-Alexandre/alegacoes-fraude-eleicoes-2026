"""Segundo leitor do log, escrito do zero com outra logica (PRE_REGISTRO 1.2).

O leitor principal (alegacoes/log.py) acompanha "tentativas" que abrem no identificador digitado. Este aqui faz o
caminho inverso: acha cada "O voto do eleitor foi computado", volta ate o "Eleitor foi habilitado" mais recente, e
classifica pelo que aparece entre o voto computado anterior e essa habilitacao, so com busca de texto.

Compara, por secao, numa amostra sorteada (semente 20261013): votos, liberacoes por digital, manuais, e votos com
hora local >= 17h de Brasilia. Saida: resultados/validacao_independente.csv e um resumo no terminal.

Uso: python ferramentas/validacao-independente.py [secoes=2000]
"""

from __future__ import annotations

import io
import random
import sqlite3
import sys
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
LOGS = RAIZ / "dados" / "brutos" / "logs"
SECOES = RAIZ / "dados" / "derivados" / "secoes"


def eventos(blob: bytes):
    z = zipfile.ZipFile(io.BytesIO(blob))
    txt = z.read([n for n in z.namelist() if n.endswith(".dat")][0]).decode("latin-1")
    out = []
    for ln in txt.split("\n"):
        if ln[:10] != "04/10/2026":
            continue
        c = ln.split("\t")
        if len(c) > 4 and c[3] == "VOTA":
            hh, mm, ss = c[0][11:19].split(":")
            out.append((int(hh) * 3600 + int(mm) * 60 + int(ss), c[4]))
    return out


def contar(evs, limite_local: int):
    n = bio = man = apos = 0
    anterior = -1
    for k, (t, msg) in enumerate(evs):
        if msg != "O voto do eleitor foi computado":
            continue
        n += 1
        if t >= limite_local:
            apos += 1
        h = None
        for j in range(k - 1, anterior, -1):
            if evs[j][1] == "Eleitor foi habilitado":
                h = j
                break
        # vai ate o voto computado: a urna as vezes grava o tipo "[biometrica]" logo DEPOIS de "Eleitor foi habilitado"
        trecho = [m for _, m in evs[anterior + 1:k + 1]]
        # o tipo e o da ultima habilitacao: corta o trecho no ultimo identificador digitado antes dela
        ult_id = max([i for i, m in enumerate(trecho) if m.startswith("Identificador digitado")], default=0)
        trecho = trecho[ult_id:]
        if any("[biom" in m for m in trecho):
            bio += 1
        elif any(m.startswith("Dado digitado confere") or "digital do mes" in m or "habilitou o eleitor" in m
                 or m.startswith("Digital coletada bate") for m in trecho):
            man += 1
        anterior = k
    return n, bio, man, apos


def main(tamanho: int) -> None:
    rnd = random.Random(20261013)
    tabelas = {p.stem: pd.read_parquet(p) for p in SECOES.glob("*.parquet")}
    alvo = []
    for uf, tab in tabelas.items():
        tab = tab[tab["n_logs"] == 1]
        alvo += [(uf, r) for r in tab.itertuples()]
    amostra = rnd.sample(alvo, min(tamanho, len(alvo)))
    linhas = []
    cons = {uf: sqlite3.connect(f"file:{LOGS / (uf + '.sqlite')}?mode=ro", uri=True) for uf in tabelas}
    for uf, r in amostra:
        padrao = f"%/{uf}/{r.mun:05d}/{r.zona:04d}/{r.secao:04d}/%"
        blob = cons[uf].execute("SELECT body FROM raw WHERE url LIKE ? AND status=200", (padrao,)).fetchone()[0]
        limite = 17 * 3600 - int(r.desl_horas) * 3600
        n, bio, man, apos = contar(eventos(blob), limite)
        linhas.append({"uf": uf, "mun": r.mun, "zona": r.zona, "secao": r.secao,
                       "votos_1": r.n_votos, "votos_2": n, "bio_1": r.n_bio, "bio_2": bio,
                       "manual_1": r.n_manual_mes + r.n_manual_sem, "manual_2": man,
                       "apos17_1": r.n_votos_apos17, "apos17_2": apos})
    d = pd.DataFrame(linhas)
    (RAIZ / "resultados").mkdir(exist_ok=True)
    d.to_csv(RAIZ / "resultados" / "validacao_independente.csv", index=False)
    for c in ("votos", "bio", "manual", "apos17"):
        igual = (d[f"{c}_1"] == d[f"{c}_2"]).mean()
        print(f"{c}: {100 * igual:.2f}% das {len(d)} secoes iguais; soma 1={d[f'{c}_1'].sum()} 2={d[f'{c}_2'].sum()}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
