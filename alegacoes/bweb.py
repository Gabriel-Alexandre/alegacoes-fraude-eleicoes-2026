"""Leitura dos CSV oficiais de boletim de urna (BU na Web), 1o turno, de 2014 a 2026.

Saidas em dados/derivados/bweb/:
  <ano>-<uf>-secoes.parquet  uma linha por secao: local de votacao, aptos, comparecimento, abertura, encerramento,
                             eleitores com biometria liberados sem ela (QT_ELEITORES_BIOMETRIA_NH, que em 2026 se
                             chama QT_ELEI_BIOM_SEM_HABILITACAO), tipo de urna, secoes agregadas
  <ano>-<uf>-votos.parquet   votos por secao e cargo (Presidente 1, Governador 3, Senador 5; nas municipais, Prefeito 11),
                             numero do votavel (95 branco, 96 nulo) e partido

2014 nao tem cabecalho nem os campos de biometria e encerramento: dela so sai aptos e comparecimento.

Uso: python -m alegacoes.bweb [anos=2018,2020,2022,2024,2026] [ufs=todas]
"""

from __future__ import annotations

import io
import json
import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
HIST = RAIZ.parent / "apuracao-eleicoes-2026" / "dados" / "brutos" / "historico"
NOVOS = RAIZ / "dados" / "brutos" / "bweb"
DERIV = RAIZ / "dados" / "derivados" / "bweb"

COLS = {
    "SG_UF": "uf", "SG_ UF": "uf", "CD_MUNICIPIO": "mun", "NR_ZONA": "zona", "NR_SECAO": "secao", "NR_LOCAL_VOTACAO": "local",
    "CD_CARGO_PERGUNTA": "cargo", "NR_PARTIDO": "partido", "NR_VOTAVEL": "numero", "QT_VOTOS": "votos",
    "QT_APTOS": "aptos", "QT_COMPARECIMENTO": "comparecimento", "DS_TIPO_URNA": "tipo_urna",
    "DT_ABERTURA": "abertura", "DT_ENCERRAMENTO": "encerramento",
    "QT_ELEITORES_BIOMETRIA_NH": "biom_nh", "QT_ELEI_BIOM_SEM_HABILITACAO": "biom_nh",
    "DS_AGREGADAS": "agregadas", "DS_SECOES_AGREGADAS": "agregadas",
}
CARGOS = {1, 3, 5, 11}


def zips(ano: int) -> list[Path]:
    if ano in (2014, 2018, 2022):
        return sorted((HIST / f"{ano}-1").glob("*.zip"))
    return sorted((NOVOS / str(ano)).glob("*.zip"))


def ler_zip(arg) -> dict:
    ano, path = arg
    DERIV.mkdir(parents=True, exist_ok=True)
    uf = path.name.split("_")[2].lower()
    z = zipfile.ZipFile(path)
    nome = next(n for n in z.namelist() if n.lower().endswith((".csv", ".txt")))
    secoes, votos = [], []
    with z.open(nome) as fh:
        txt = io.TextIOWrapper(fh, encoding="latin-1")
        if ano == 2014:
            leitor = pd.read_csv(txt, sep=";", header=None, dtype=str, chunksize=400_000)
        else:
            leitor = pd.read_csv(txt, sep=";", dtype=str, chunksize=400_000)
        for ch in leitor:
            if ano == 2014:
                # posicoes conferidas numa linha real: 4 UF, 5 cargo, 7 zona, 8 secao, 10 numero, 12 municipio,
                # 15 aptos, 16 abstencoes, 17 comparecimento, 24 votos
                ch = ch.rename(columns={4: "uf", 5: "cargo", 7: "zona", 8: "secao", 10: "numero", 12: "mun",
                                        15: "aptos", 16: "abstencoes", 17: "comparecimento", 24: "votos"})
            else:
                ch = ch.rename(columns={c: COLS[c] for c in ch.columns if c in COLS})
            ch["cargo"] = pd.to_numeric(ch["cargo"], errors="coerce")
            for c in ("mun", "zona", "secao"):
                ch[c] = pd.to_numeric(ch[c], errors="coerce").astype("Int64")
            chave = ["uf", "mun", "zona", "secao"]
            cs = [c for c in ("local", "aptos", "comparecimento", "tipo_urna", "abertura", "encerramento", "biom_nh", "agregadas") if c in ch.columns]
            secoes.append(ch[chave + cs].drop_duplicates(chave))
            v = ch[ch["cargo"].isin(CARGOS)]
            cv = [c for c in ("cargo", "numero", "partido", "votos") if c in v.columns]
            votos.append(v[chave + cv])
    s = pd.concat(secoes).drop_duplicates(["uf", "mun", "zona", "secao"])
    for c in ("aptos", "comparecimento", "biom_nh", "local"):
        if c in s.columns:
            s[c] = pd.to_numeric(s[c], errors="coerce")
    for c in ("abertura", "encerramento"):
        if c in s.columns:
            iso = pd.to_datetime(s[c], format="%Y-%m-%d %H:%M:%S", errors="coerce")
            br = pd.to_datetime(s[c], format="%d/%m/%Y %H:%M:%S", errors="coerce")
            s[c] = iso.fillna(br)
    v = pd.concat(votos)
    for c in ("numero", "partido", "votos"):
        if c in v.columns:
            v[c] = pd.to_numeric(v[c], errors="coerce")
    v = v.groupby(["uf", "mun", "zona", "secao", "cargo", "numero"], dropna=False, observed=True)["votos"].sum().reset_index()
    s.to_parquet(DERIV / f"{ano}-{uf}-secoes.parquet", index=False)
    v.to_parquet(DERIV / f"{ano}-{uf}-votos.parquet", index=False)
    return {"ano": ano, "uf": uf, "secoes": len(s), "linhas_votos": len(v),
            "comparecimento": int(s["comparecimento"].sum()), "biom_nh": int(s["biom_nh"].sum()) if "biom_nh" in s else None}


if __name__ == "__main__":
    anos = [int(a) for a in (sys.argv[1] if len(sys.argv) > 1 else "2018,2020,2022,2024,2026").split(",")]
    ufs = None if len(sys.argv) < 3 or sys.argv[2] == "todas" else set(sys.argv[2].split(","))
    tarefas = [(a, p) for a in anos for p in zips(a) if ufs is None or p.name.split("_")[2].lower() in ufs]
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(ler_zip, tarefas):
            print(json.dumps(r), flush=True)
