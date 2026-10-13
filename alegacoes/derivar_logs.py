"""Le os logs de uma UF e grava duas tabelas em dados/derivados/logs/:

  <uf>-eleitores.parquet  uma linha por voto computado: secao, hora local (s), tipo de liberacao, "nao confere",
                          codigo do mesario (HMAC; nunca o numero), tentativas de digital, identificador usado
                          (titulo ou CPF, so o TIPO), suspensao
  <uf>-urnas.parquet      uma linha por log (urna): secao, hash, id da urna, linhas do dia, primeiro evento,
                          "urna pronta", "encerrar votacao", tipos de habilitacao vistos

Uso: python -m alegacoes.derivar_logs ac,al,... | todas
"""

from __future__ import annotations

import json
import secrets
import sqlite3
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

from .coleta_logs import BRUTOS, UFS
from .log import ler_jez, ler_log

RAIZ = Path(__file__).resolve().parents[1]
DERIV = RAIZ / "dados" / "derivados" / "logs"
CHAVE = RAIZ / "dados" / "chave-local.txt"


def chave() -> bytes:
    if not CHAVE.exists():
        CHAVE.parent.mkdir(parents=True, exist_ok=True)
        CHAVE.write_text(secrets.token_hex(32))
    return bytes.fromhex(CHAVE.read_text().strip())


def partes_da_url(url: str):
    # .../dados/<uf>/<mun>/<zona>/<secao>/<hash>/<arquivo>
    p = url.split("/")
    return p[-6].upper(), p[-5], p[-4], p[-3], p[-2]


def derivar_uf(uf: str) -> dict:
    DERIV.mkdir(parents=True, exist_ok=True)
    k = chave()
    con = sqlite3.connect(f"file:{BRUTOS / (uf + '.sqlite')}?mode=ro", uri=True)
    eleitores, urnas, falhas = [], [], []
    for url, body in con.execute("SELECT url, body FROM raw WHERE status=200"):
        sg, mun, zona, secao, h = partes_da_url(url)
        try:
            lt = ler_log(ler_jez(body), k)
        except Exception as e:  # registro, nao silencio
            falhas.append({"url": url, "erro": repr(e)[:200]})
            continue
        urnas.append({"uf": sg, "mun_cd": mun, "zona": zona, "secao": secao, "hash": h, "id_urna": lt.id_urna,
                      "linhas_dia": lt.linhas_dia, "primeiro_evento_s": lt.primeiro_evento_s, "pronta_s": lt.pronta_s,
                      "encerrar_s": lt.encerrar_s, "n_votos": len(lt.eleitores), "contingencia": lt.contingencia, "tipos_txt": json.dumps(lt.tipos_txt, ensure_ascii=False)})
        for e in lt.eleitores:
            eleitores.append((sg, mun, zona, secao, h) + e)
    con.close()
    cols = ["uf", "mun_cd", "zona", "secao", "hash", "t_s", "tipo", "nao_confere", "mesario", "tent_digital",
            "ident", "suspensao", "habilitado", "suspenso_mesario", "hab_s"]
    ev = pd.DataFrame(eleitores, columns=cols)
    for c in ("uf", "mun_cd", "zona", "secao", "hash", "tipo", "mesario", "ident"):
        ev[c] = ev[c].astype("category")
    ev.to_parquet(DERIV / f"{uf}-eleitores.parquet", index=False)
    pd.DataFrame(urnas).to_parquet(DERIV / f"{uf}-urnas.parquet", index=False)
    if falhas:
        pd.DataFrame(falhas).to_csv(DERIV / f"{uf}-falhas.csv", index=False)
    return {"uf": uf, "logs": len(urnas), "votos": len(ev), "falhas": len(falhas)}


if __name__ == "__main__":
    ufs = UFS if sys.argv[1] == "todas" else sys.argv[1].split(",")
    chave()
    with ProcessPoolExecutor(max_workers=min(8, len(ufs))) as ex:
        for r in ex.map(derivar_uf, ufs):
            print(json.dumps(r), flush=True)
