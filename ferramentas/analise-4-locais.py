"""A12: secoes cujo local de votacao de 2026 e diferente do local original (arquivo oficial de locais de votacao 2026).

Saida: resultados/a12_mudanca_de_local.csv e o bloco "a12" de RESUMO.json.
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
ZIP = RAIZ / "dados" / "brutos" / "eleitorado" / "eleitorado_local_votacao_2026.zip"


def main() -> None:
    z = zipfile.ZipFile(ZIP)
    partes = []
    for n in z.namelist():
        if not n.endswith(".csv"):
            continue
        d = pd.read_csv(io.TextIOWrapper(z.open(n), encoding="latin-1"), sep=";", dtype=str,
                        usecols=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_TURNO", "NR_LOCAL_VOTACAO", "NR_LOCAL_VOTACAO_ORIGINAL", "QT_ELEITOR_SECAO"])
        partes.append(d[d["NR_TURNO"] == "1"])
    d = pd.concat(partes, ignore_index=True).drop_duplicates(["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]).reset_index(drop=True)
    d["QT_ELEITOR_SECAO"] = pd.to_numeric(d["QT_ELEITOR_SECAO"], errors="coerce")
    orig = d["NR_LOCAL_VOTACAO_ORIGINAL"].fillna("").str.strip()
    d["mudou"] = (orig != "") & (orig != "-1") & (orig != d["NR_LOCAL_VOTACAO"])
    d["eleit_mudou"] = d["QT_ELEITOR_SECAO"].where(d["mudou"], 0)
    por_uf = d.groupby("SG_UF").agg(secoes=("mudou", "size"), secoes_mudaram=("mudou", "sum"),
                                    eleitores_em_secoes_que_mudaram=("eleit_mudou", "sum")).reset_index()
    por_uf.to_csv(RAIZ / "resultados" / "a12_mudanca_de_local.csv", index=False)
    tot = {"secoes": int(len(d)), "secoes_mudaram": int(d["mudou"].sum()), "eleitores_em_secoes_que_mudaram": int(d.loc[d["mudou"], "QT_ELEITOR_SECAO"].sum()),
           "por_uf": por_uf.to_dict(orient="records")}
    p = RAIZ / "resultados" / "RESUMO.json"
    r = json.loads(p.read_text(encoding="utf-8"))
    r["a12"] = tot
    p.write_text(json.dumps(r, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print({k: v for k, v in tot.items() if k != "por_uf"})
    print(por_uf.sort_values("secoes_mudaram", ascending=False).head(8).to_string())


if __name__ == "__main__":
    main()
