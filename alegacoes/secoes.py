"""Tabela por secao de 2026: metricas do log (PRE_REGISTRO secao 2) + boletim oficial + marcas S3, S5, S10, S5abs, C3.

Hora: o log esta no relogio local da urna. O deslocamento para Brasilia e por municipio: 8h menos a mediana da hora
de abertura das urnas do municipio (abertura do boletim), arredondado (PRE_REGISTRO 0.3 e emenda E4).

Saida: dados/derivados/secoes/<uf>.parquet  (uma linha por secao principal com log)
Uso: python -m alegacoes.secoes ac,al,... | todas
"""

from __future__ import annotations

import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from .coleta_logs import UFS

RAIZ = Path(__file__).resolve().parents[1]
LOGS = RAIZ / "dados" / "derivados" / "logs"
BWEB = RAIZ / "dados" / "derivados" / "bweb"
APURACAO_UF = RAIZ.parent / "apuracao-eleicoes-2026" / "dados" / "derivados" / "uf"
SAIDA = RAIZ / "dados" / "derivados" / "secoes"
H17, H12, H13, H08 = 17 * 3600, 12 * 3600, 13 * 3600, 8 * 3600
MANUAL = {"manual_mes", "manual_sem"}


def deslocamento_por_municipio(sec: pd.DataFrame) -> pd.Series:
    ab = sec.dropna(subset=["abertura"])
    horas = ab["abertura"].dt.hour + ab["abertura"].dt.minute / 60
    med = horas.groupby(ab["mun"]).median()
    return (8 - med).round().astype(int)


def maior_sequencia(manual: np.ndarray, t: np.ndarray, mes: np.ndarray):
    """Maior sequencia de manuais consecutivas (na ordem dos votos) entre os votos >= 17h; devolve
    (tamanho, mediana do intervalo entre votos da sequencia, mesarios distintos identificados, tem_nao_id)."""
    melhor = (0, np.nan, 0, False)
    i, n = 0, len(manual)
    while i < n:
        if not manual[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and manual[j + 1]:
            j += 1
        tam = j - i + 1
        if tam > melhor[0]:
            interv = np.diff(t[i:j + 1])
            meds = set(mes[i:j + 1]) - {"", "nao_id"}
            melhor = (tam, float(np.median(interv)) if len(interv) else np.nan, len(meds), "nao_id" in set(mes[i:j + 1]))
        i = j + 1
    return melhor


def metricas_secao(g: pd.DataFrame) -> dict:
    g = g.sort_values("t_b")
    t = g["t_b"].to_numpy()
    tipo = g["tipo"].astype(str).to_numpy()
    man = np.isin(tipo, list(MANUAL))
    apos = t >= H17
    antes = ~apos
    dur = (g["t_s"] - g["hab_s"]).to_numpy().astype(float)
    dur[g["hab_s"].to_numpy() < 0] = np.nan
    manha = (t >= H08) & (t < H12)
    iv_manha = np.diff(t[manha])
    seq = maior_sequencia(man[apos], t[apos], g["mesario"].astype(str).to_numpy()[apos])
    nc = g["nao_confere"].to_numpy()
    janela = (t >= H12) & (t < H13)
    return {
        "n_votos": len(g), "n_bio": int((tipo == "biometrica").sum()), "n_manual_mes": int((tipo == "manual_mes").sum()),
        "n_manual_sem": int((tipo == "manual_sem").sum()), "n_outra": int((tipo == "outra").sum()),
        "n_votos_apos17": int(apos.sum()), "n_manual_apos17": int((man & apos).sum()), "n_manual_antes17": int((man & antes).sum()),
        "n_manual_mes_apos17": int(((tipo == "manual_mes") & apos).sum()), "n_manual_sem_apos17": int(((tipo == "manual_sem") & apos).sum()),
        "n_votos_12_13": int(janela.sum()), "n_manual_12_13": int((man & janela).sum()),
        "n_nao_confere": int(nc.sum()), "n_nao_confere_apos17": int(nc[apos].sum()),
        "seq_manual_apos17": seq[0], "seq_mediana_intervalo": seq[1], "seq_mesarios_ident": seq[2], "seq_tem_nao_id": seq[3],
        "p10_intervalo_manha": float(np.percentile(iv_manha, 10)) if len(iv_manha) >= 10 else np.nan,
        "dur_mediana_antes17": float(np.nanmedian(dur[antes])) if antes.any() else np.nan,
        "dur_mediana_apos17": float(np.nanmedian(dur[apos])) if apos.any() else np.nan,
        "dur_mediana_manual_apos17": float(np.nanmedian(dur[man & apos])) if (man & apos).any() else np.nan,
        "dur_mediana_bio_apos17": float(np.nanmedian(dur[(tipo == "biometrica") & apos])) if ((tipo == "biometrica") & apos).any() else np.nan,
        "n_sem_habilitacao": int((~g["habilitado"].to_numpy()).sum()), "n_suspenso_mesario": int(g["suspenso_mesario"].sum()),
        "primeiro_voto_b": int(t[0]) if len(t) else None, "ultimo_voto_b": int(t[-1]) if len(t) else None,
    }


def votos_presidente(uf: str) -> pd.DataFrame:
    v = pd.read_parquet(BWEB / f"2026-{uf}-votos.parquet")
    p = v[v["cargo"] == 1]
    chave = ["mun", "zona", "secao"]
    validos = p[~p["numero"].isin([95, 96])].groupby(chave)["votos"].sum().rename("validos_pres")
    l13 = p[p["numero"] == 13].groupby(chave)["votos"].sum().rename("lula")
    f22 = p[p["numero"] == 22].groupby(chave)["votos"].sum().rename("flavio")
    out = pd.concat([validos, l13, f22], axis=1).fillna(0)
    g = v[v["cargo"] == 3]
    if len(g):
        gv = g[~g["numero"].isin([95, 96])]
        tot = gv.groupby("numero")["votos"].sum().sort_values(ascending=False)
        out = out.join(gv.groupby(chave)["votos"].sum().rename("validos_gov"))
        for k, num in enumerate(tot.index[:2]):
            out = out.join(gv[gv["numero"] == num].groupby(chave)["votos"].sum().rename(f"gov_{k + 1}"))
            out[f"gov_{k + 1}_numero"] = int(num)
    return out.reset_index()


def construir(uf: str) -> dict:
    SAIDA.mkdir(parents=True, exist_ok=True)
    sec = pd.read_parquet(BWEB / f"2026-{uf}-secoes.parquet")
    for c in ("mun", "zona", "secao"):
        sec[c] = sec[c].astype(int)
    desl = deslocamento_por_municipio(sec)
    ev = pd.read_parquet(LOGS / f"{uf}-eleitores.parquet")
    urnas = pd.read_parquet(LOGS / f"{uf}-urnas.parquet")
    for df in (ev, urnas):
        for c in ("mun_cd", "zona", "secao"):
            df[c] = df[c].astype(str).astype(int)
    ev = ev.rename(columns={"mun_cd": "mun"})
    urnas = urnas.rename(columns={"mun_cd": "mun"})
    ev["desl"] = ev["mun"].map(desl).fillna(0).astype(int)
    ev["t_b"] = ev["t_s"] + ev["desl"] * 3600
    linhas = []
    for (mun, zona, secao), g in ev.groupby(["mun", "zona", "secao"], sort=False):
        d = metricas_secao(g)
        d.update({"mun": mun, "zona": zona, "secao": secao})
        linhas.append(d)
    m = pd.DataFrame(linhas)
    urnas["jv"] = urnas["ja_votou_s"].map(json.loads)
    urnas["desl"] = urnas["mun"].map(desl).fillna(0).astype(int)

    def episodios(lst, d):
        """'ja votou' em sequencia (menos de 10 min entre um e outro) conta como um episodio."""
        t = sorted(x + d * 3600 for x in lst)
        ep, ult = [], None
        for x in t:
            if ult is None or x - ult > 600:
                ep.append(x)
            ult = x
        return ep

    urnas["ep"] = [episodios(a, d) for a, d in zip(urnas["jv"], urnas["desl"])]
    urnas["n_ja_votou"] = urnas["jv"].map(len)
    urnas["n_ep_ja_votou"] = urnas["ep"].map(len)
    urnas["n_ep_ja_votou_apos17"] = urnas["ep"].map(lambda e: sum(1 for x in e if x >= H17))
    cont = urnas.groupby(["mun", "zona", "secao"]).agg(contingencia=("contingencia", "max"), n_logs=("hash", "size"),
                                                       n_ja_votou=("n_ja_votou", "sum"), n_ep_ja_votou=("n_ep_ja_votou", "sum"),
                                                       n_ep_ja_votou_apos17=("n_ep_ja_votou_apos17", "sum"), n_impedido=("impedido", "sum")).reset_index()
    m = m.merge(cont, on=["mun", "zona", "secao"], how="left")
    m = m.merge(sec, on=["mun", "zona", "secao"], how="left")
    m = m.merge(votos_presidente(uf), on=["mun", "zona", "secao"], how="left")
    bu = pd.read_parquet(APURACAO_UF / f"{uf}-secoes.parquet")
    bu = bu[~bu["agregada"]][["mun_cd", "zona", "secao", "aptos", "comparecimento"]]
    bu.columns = ["mun", "zona", "secao", "aptos_bu", "comp_bu"]
    for c in ("mun", "zona", "secao"):
        bu[c] = bu[c].astype(int)
    m = m.merge(bu, on=["mun", "zona", "secao"], how="left")
    m["uf"] = uf.upper()
    m["desl_horas"] = m["mun"].map(desl)
    m["cobertura_log"] = m["n_votos"] / m["comp_bu"]
    rel = m["seq_mediana_intervalo"] < m["p10_intervalo_manha"]
    m["S3"] = (m["seq_manual_apos17"] >= 3) & rel
    m["S5"] = (m["seq_manual_apos17"] >= 5) & rel
    m["S10"] = (m["seq_manual_apos17"] >= 10) & rel
    m["S5abs"] = (m["seq_manual_apos17"] >= 5) & (m["seq_mediana_intervalo"] < 60)
    m["C3"] = m["n_nao_confere_apos17"] >= 3
    m.to_parquet(SAIDA / f"{uf}.parquet", index=False)
    return {"uf": uf, "secoes": len(m), "votos_log": int(m["n_votos"].sum()), "sem_bweb": int(m["comparecimento"].isna().sum()),
            "cobertura_100": int((m["cobertura_log"] == 1).sum()), "contingencia": int(m["contingencia"].sum())}


if __name__ == "__main__":
    ufs = UFS if sys.argv[1] == "todas" else sys.argv[1].split(",")
    with ProcessPoolExecutor(max_workers=min(6, len(ufs))) as ex:
        for r in ex.map(construir, ufs):
            print(json.dumps(r), flush=True)
