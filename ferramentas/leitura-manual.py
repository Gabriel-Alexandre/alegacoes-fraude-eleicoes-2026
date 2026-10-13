"""PRE_REGISTRO 1.2: leitura a mao de 30 secoes sorteadas (semente 20261013).

Para cada secao, sorteia 3 eleitores (um liberado por digital, um manual se houver, um depois das 17h se houver) e
imprime as linhas cruas do bloco de cada um, com todo numero de 12 digitos tarjado, ao lado da classificacao do
leitor. Quem le confere se a classificacao bate. Nada disso vai para o git (as linhas cruas podem ter dado pessoal).

Uso: python ferramentas/leitura-manual.py > dados/execucao/leitura-manual.txt
"""

from __future__ import annotations

import random
import re
import sqlite3
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from alegacoes.log import ler_jez  # noqa: E402

PULAR = ("Tecla indevida", "Quantidade de mem", "Espa", "Voto confirmado", "Eleitor corrigiu", "Urna ligada", "Captura", "Capturada", "Número de tentativas", "Número")


def main() -> None:
    rnd = random.Random(20261013)
    ev_por_uf = {p.stem.split("-")[0]: p for p in (RAIZ / "dados" / "derivados" / "logs").glob("*-eleitores.parquet")}
    sec_por_uf = {p.stem: pd.read_parquet(p) for p in (RAIZ / "dados" / "derivados" / "secoes").glob("*.parquet")}
    alvo = [(uf, r) for uf, t in sec_por_uf.items() for r in t[(t["n_logs"] == 1) & (t["cobertura_log"] == 1)].itertuples()]
    for uf, r in rnd.sample(alvo, 30):
        ev = pd.read_parquet(ev_por_uf[uf])
        for c in ("mun_cd", "zona", "secao"):
            ev[c] = ev[c].astype(str).astype(int)
        e = ev[(ev["mun_cd"] == r.mun) & (ev["zona"] == r.zona) & (ev["secao"] == r.secao)].sort_values("t_s").reset_index(drop=True)
        escolhas = []
        for cond in (e["tipo"] == "biometrica", e["tipo"] == "manual_mes", e["tipo"] == "manual_sem", e["tipo"] == "outra",
                     e["t_s"] + int(r.desl_horas) * 3600 >= 17 * 3600):
            idx = list(e.index[cond])
            if idx:
                escolhas.append(rnd.choice(idx))
        con = sqlite3.connect(f"file:{RAIZ / 'dados' / 'brutos' / 'logs' / (uf + '.sqlite')}?mode=ro", uri=True)
        blob = con.execute("SELECT body FROM raw WHERE url LIKE ? AND status=200", (f"%/{uf}/{r.mun:05d}/{r.zona:04d}/{r.secao:04d}/%",)).fetchone()[0]
        linhas = [l.split("\t") for l in ler_jez(blob) if l.startswith("04/10/2026") and "\tVOTA\t" in l]
        computados = [i for i, l in enumerate(linhas) if l[4] == "O voto do eleitor foi computado"]
        print(f"#### {uf.upper()} mun {r.mun} zona {r.zona} secao {r.secao} (votos {r.n_votos})")
        for k in sorted(set(escolhas)):
            ini = computados[k - 1] + 1 if k > 0 else 0
            fim = computados[k]
            print(f"-- eleitor {k + 1}: leitor diz tipo={e.loc[k, 'tipo']} nao_confere={e.loc[k, 'nao_confere']} hora_local={e.loc[k, 't_s'] // 3600:02d}:{(e.loc[k, 't_s'] % 3600) // 60:02d}")
            for l in linhas[ini:fim + 1]:
                if not l[4].startswith(PULAR):
                    print("   ", l[0][11:], re.sub(r"\d{12}", "############", l[4])[:90])


if __name__ == "__main__":
    main()
