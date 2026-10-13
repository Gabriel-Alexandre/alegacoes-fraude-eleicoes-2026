"""Testes de serie e de conta: T1.6/T15 (contador de liberacao sem biometria, 2018 a 2026, e os fiscais), T3.1 e
T3.2 (comparecimento), T8.2 (secoes com 95% para um lado), A6 ("a conta nao fecha") e A7 (a curva "linear demais").

Criterios: docs/PRE_REGISTRO.md secoes 5, 6 e 7. Le dados/derivados/bweb/ e dados/derivados/secoes/.
Saidas em resultados/t15_*.csv, t3_*.csv, t8_*.csv, a6_*.csv, a7_*.csv e os blocos de resultados/RESUMO.json.

Uso: python ferramentas/analise-2-series-e-contas.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

RAIZ = Path(__file__).resolve().parents[1]
BW = RAIZ / "dados" / "derivados" / "bweb"
SEC = RAIZ / "dados" / "derivados" / "secoes"
APURACAO_UF = RAIZ.parent / "apuracao-eleicoes-2026" / "dados" / "derivados" / "uf"
SAI = RAIZ / "resultados"
REGIAO = {
    **dict.fromkeys(["AC", "AP", "AM", "PA", "RO", "RR", "TO"], "Norte"),
    **dict.fromkeys(["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"], "Nordeste"),
    **dict.fromkeys(["DF", "GO", "MT", "MS"], "Centro-Oeste"),
    **dict.fromkeys(["ES", "MG", "RJ", "SP"], "Sudeste"),
    **dict.fromkeys(["PR", "RS", "SC"], "Sul"),
}
CHAVE = ["uf", "mun", "zona", "secao"]
CANDIDATOS = {2018: (17, 13), 2022: (22, 13), 2026: (22, 13)}  # (direita, PT)
SEMENTE = 20261013


def secoes(ano: int) -> pd.DataFrame:
    d = pd.concat([pd.read_parquet(p) for p in sorted(BW.glob(f"{ano}-*-secoes.parquet"))], ignore_index=True)
    d = d[d["uf"] != "ZZ"].copy()
    for c in ("mun", "zona", "secao"):
        d[c] = d[c].astype(int)
    d["regiao"] = d["uf"].map(REGIAO)
    return d


def votos(ano: int, cargo: int, exterior: bool = False) -> pd.DataFrame:
    d = pd.concat([pd.read_parquet(p) for p in sorted(BW.glob(f"{ano}-*-votos.parquet"))], ignore_index=True)
    d = d[((d["uf"] != "ZZ") | exterior) & (d["cargo"] == cargo)].copy()
    for c in ("mun", "zona", "secao"):
        d[c] = d[c].astype(int)
    return d


def presidente_por_secao(ano: int) -> pd.DataFrame:
    v = votos(ano, 1)
    dire, pt = CANDIDATOS[ano]
    val = v[~v["numero"].isin([95, 96])].groupby(CHAVE)["votos"].sum().rename("validos")
    a = v[v["numero"] == dire].groupby(CHAVE)["votos"].sum().rename("direita")
    b = v[v["numero"] == pt].groupby(CHAVE)["votos"].sum().rename("pt")
    return pd.concat([val, a, b], axis=1).fillna(0).reset_index()


def t15(resumo: dict) -> None:
    anos = [2018, 2020, 2022, 2024, 2026]
    lin = []
    for ano in anos:
        s = secoes(ano)
        for escopo, g in [("Brasil", s)] + [(r, s[s["regiao"] == r]) for r in sorted(set(REGIAO.values()))] + [("CE", s[s["uf"] == "CE"])]:
            lin.append({"ano": ano, "escopo": escopo, "secoes": len(g), "comparecimento": int(g["comparecimento"].sum()),
                        "biom_nh": int(g["biom_nh"].sum()), "taxa_nh_pct": 100 * g["biom_nh"].sum() / g["comparecimento"].sum()})
    t = pd.DataFrame(lin)
    t.to_csv(SAI / "t15_serie_contador_sem_biometria.csv", index=False)
    piv = t.pivot(index="escopo", columns="ano", values="taxa_nh_pct")
    piv["delta_pres_2022_2026"] = piv[2026] - piv[2022]
    piv["delta_2022_2024"] = piv[2024] - piv[2022]   # emenda E9: a queda antes de qualquer campanha de fiscais de 2026
    piv["delta_2024_2026"] = piv[2026] - piv[2024]   # emenda E9: o que mudou de 2024 para 2026
    piv["delta_pres_2018_2022"] = piv[2022] - piv[2018]  # emenda E9: a variacao "normal" entre duas presidenciais
    resto = {}
    for esc in piv.index:
        if esc == "Brasil":
            continue
        resto[esc] = esc
    piv.to_csv(SAI / "t15_deltas.csv")
    resumo["t15"] = {"serie": t.to_dict(orient="records"), "deltas": piv.reset_index().to_dict(orient="records")}

    # T15.2: dentro do local de votacao, secoes casadas 2022-2026
    s22, s26 = secoes(2022), secoes(2026)
    p22, p26 = presidente_por_secao(2022), presidente_por_secao(2026)
    a = s22.merge(p22, on=CHAVE).assign(nh=lambda x: x["biom_nh"] / x["comparecimento"], pt=lambda x: x["pt"] / x["validos"], dir=lambda x: x["direita"] / x["validos"])
    b = s26.merge(p26, on=CHAVE).assign(nh=lambda x: x["biom_nh"] / x["comparecimento"], pt=lambda x: x["pt"] / x["validos"], dir=lambda x: x["direita"] / x["validos"])
    m = a[CHAVE + ["nh", "pt", "dir"]].merge(b[CHAVE + ["nh", "pt", "dir", "local", "regiao", "validos"]], on=CHAVE, suffixes=("_22", "_26"))
    m = m[m["validos"] >= 50].replace([np.inf, -np.inf], np.nan).dropna()
    m["d_nh"], m["d_pt"], m["d_dir"] = m["nh_26"] - m["nh_22"], m["pt_26"] - m["pt_22"], m["dir_26"] - m["dir_22"]
    reg = []
    for escopo, g in [("Brasil", m)] + [(r, m[m["regiao"] == r]) for r in sorted(set(REGIAO.values()))] + [("CE", m[m["uf"] == "CE"])]:
        g = g.copy()
        g["n_local"] = g.groupby(["uf", "mun", "local"])["secao"].transform("count")
        g = g[g["n_local"] >= 2]
        for y in ("d_pt", "d_dir"):
            for c in (y, "d_nh"):
                g[c + "_dm"] = g[c] - g.groupby(["uf", "mun", "local"])[c].transform("mean")
            mod = sm.OLS(g[y + "_dm"], g[["d_nh_dm"]]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(g["uf"] + g["mun"].astype(str))[0]})
            reg.append({"escopo": escopo, "y": y, "n": len(g), "coef_d_nh": mod.params.iloc[0], "ep": mod.bse.iloc[0], "p": mod.pvalues.iloc[0]})
    pd.DataFrame(reg).to_csv(SAI / "t15_2_dentro_do_local.csv", index=False)
    resumo["t15_2"] = reg

    # T15.3: a virada por municipio contra a queda do contador
    def municipal(sx, px):
        j = sx.merge(px, on=CHAVE)
        g = j.groupby(["uf", "mun"]).agg(comp=("comparecimento", "sum"), nh=("biom_nh", "sum"), val=("validos", "sum"), dire=("direita", "sum"), pt=("pt", "sum"))
        g["nh_taxa"] = g["nh"] / g["comp"]
        g["margem_dir"] = (g["dire"] - g["pt"]) / g["val"]
        return g
    g22, g26 = municipal(s22, p22), municipal(s26, p26)
    gm = g22[["nh_taxa", "margem_dir"]].join(g26[["nh_taxa", "margem_dir", "val"]], lsuffix="_22", rsuffix="_26").dropna()
    gm["virada"] = gm["margem_dir_26"] - gm["margem_dir_22"]
    gm["d_nh"] = gm["nh_taxa_26"] - gm["nh_taxa_22"]
    gm = gm.reset_index()
    gm["regiao"] = gm["uf"].map(REGIAO)
    v = []
    for escopo, g in [("Brasil", gm)] + [(r, gm[gm["regiao"] == r]) for r in sorted(set(REGIAO.values()))]:
        X = sm.add_constant(g["d_nh"])
        mod = sm.WLS(g["virada"], X, weights=g["val"]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(g["uf"])[0]})
        v.append({"escopo": escopo, "municipios": len(g), "coef_virada_sobre_d_nh": mod.params["d_nh"], "ep": mod.bse["d_nh"], "p": mod.pvalues["d_nh"],
                  "virada_media_pond": float(np.average(g["virada"], weights=g["val"])), "d_nh_medio_pond": float(np.average(g["d_nh"], weights=g["val"]))})
    pd.DataFrame(v).to_csv(SAI / "t15_3_virada_por_municipio.csv", index=False)
    resumo["t15_3"] = v


def t3_t8(resumo: dict) -> None:
    # T3.1 comparecimento por municipio
    taxas = {}
    for ano in (2014, 2018, 2022, 2026):
        s = secoes(ano)
        g = s.groupby(["uf", "mun"]).agg(aptos=("aptos", "sum"), comp=("comparecimento", "sum"))
        taxas[ano] = g["comp"] / g["aptos"]
    t = pd.DataFrame(taxas).dropna(subset=[2022, 2026]).reset_index()
    t["regiao"] = t["uf"].map(REGIAO)
    t["d"] = t[2026] - t[2022]
    t["z"] = t.groupby("uf")["d"].transform(lambda x: (x - x.mean()) / x.std())
    p22, p26 = presidente_por_secao(2022), presidente_por_secao(2026)
    def pt_mun(p):
        g = p.groupby(["uf", "mun"]).agg(val=("validos", "sum"), pt=("pt", "sum"))
        return g["pt"] / g["val"]
    t = t.merge(pd.DataFrame({"pt22": pt_mun(p22), "pt26": pt_mun(p26)}).reset_index(), on=["uf", "mun"], how="left")
    t["d_pt"] = t["pt26"] - t["pt22"]
    t.to_csv(SAI / "t3_1_comparecimento_por_municipio.csv", index=False)
    lin = []
    for escopo, g in [("Brasil", t)] + [(r, t[t["regiao"] == r]) for r in sorted(set(REGIAO.values()))] + [("CE", t[t["uf"] == "CE"])]:
        acima, abaixo = g[g["z"] > 3], g[g["z"] < -3]
        lin.append({"escopo": escopo, "municipios": len(g), "comparec_2014": float(np.nanmedian(g[2014])), "comparec_2018": float(np.nanmedian(g[2018])),
                    "comparec_2022": float(np.nanmedian(g[2022])), "comparec_2026": float(np.nanmedian(g[2026])),
                    "fora_da_historia_acima": len(acima), "fora_da_historia_abaixo": len(abaixo),
                    "d_pt_medio_nos_acima": float(acima["d_pt"].mean()) if len(acima) else None, "d_pt_medio_geral": float(g["d_pt"].mean())})
    resumo["t3_1"] = lin
    pd.DataFrame(lin).to_csv(SAI / "t3_1_resumo.csv", index=False)

    # T3.2 secoes com comparecimento >= 95% (aptos >= 50)
    lin = []
    for ano in (2018, 2022, 2026):
        s = secoes(ano)
        s = s[s["aptos"] >= 50]
        s["alta"] = s["comparecimento"] / s["aptos"] >= 0.95
        for escopo, g in [("Brasil", s)] + [(r, s[s["regiao"] == r]) for r in sorted(set(REGIAO.values()))]:
            lin.append({"ano": ano, "escopo": escopo, "secoes": len(g), "comparec_95": int(g["alta"].sum()), "pct": 100 * g["alta"].mean()})
    log = pd.concat([pd.read_parquet(p) for p in SEC.glob("*.parquet")])
    log = log[log["uf"] != "ZZ"]
    log = log[log["aptos_bu"] >= 50]
    alta = log["comp_bu"] / log["aptos_bu"] >= 0.95
    resumo["t3_2"] = {"por_ano": lin, "manual_pct_alta_2026": float(100 * log.loc[alta, ["n_manual_mes", "n_manual_sem"]].sum().sum() / log.loc[alta, "n_votos"].sum()),
                      "manual_pct_demais_2026": float(100 * log.loc[~alta, ["n_manual_mes", "n_manual_sem"]].sum().sum() / log.loc[~alta, "n_votos"].sum()),
                      "secoes_alta_2026_log": int(alta.sum())}
    pd.DataFrame(lin).to_csv(SAI / "t3_2_comparecimento_95.csv", index=False)

    # T8.2 secoes com >= 95% dos validos para um lado (validos >= 50)
    lin = []
    for ano in (2018, 2022, 2026):
        s = secoes(ano)[CHAVE + ["regiao"]].merge(presidente_por_secao(ano), on=CHAVE)
        s = s[s["validos"] >= 50]
        for escopo, g in [("Brasil", s)] + [(r, s[s["regiao"] == r]) for r in sorted(set(REGIAO.values()))]:
            lin.append({"ano": ano, "escopo": escopo, "secoes": len(g), "pt_95": int((g["pt"] / g["validos"] >= 0.95).sum()),
                        "direita_95": int((g["direita"] / g["validos"] >= 0.95).sum())})
    pd.DataFrame(lin).to_csv(SAI / "t8_2_secoes_95_um_lado.csv", index=False)
    resumo["t8_2"] = lin


def a6(resumo: dict) -> None:
    lin = []
    vagas = {2018: 2, 2022: 1, 2026: 2}
    for ano in (2018, 2022, 2026):
        sen = votos(ano, 5)
        sen = sen[~sen["numero"].isin([95, 96])]
        porc = sen.groupby(["uf", "numero"])["votos"].sum().reset_index()
        porc["partido"] = porc["numero"] // 10
        porc["rank"] = porc.groupby("uf")["votos"].rank(ascending=False, method="first")
        eleitos = porc[porc["rank"] <= vagas[ano]]
        pres = votos(ano, 1, exterior=True)  # presidente inclui o exterior
        dire, pt = CANDIDATOS[ano]
        comp = secoes(ano)["comparecimento"].sum()
        lin.append({"ano": ano, "vagas_por_estado": vagas[ano],
                    "senado_eleitos_PT": int(eleitos.loc[eleitos["partido"] == 13, "votos"].sum()),
                    "senado_eleitos_PL": int(eleitos.loc[eleitos["partido"] == 22, "votos"].sum()),
                    "senado_eleitos_PSL_2018": int(eleitos.loc[eleitos["partido"] == 17, "votos"].sum()),
                    "senado_todos_PT": int(porc.loc[porc["partido"] == 13, "votos"].sum()),
                    "senado_todos_PL": int(porc.loc[porc["partido"] == 22, "votos"].sum()),
                    "senado_validos_total": int(porc["votos"].sum()), "comparecimento": int(comp),
                    "senado_validos_por_eleitor": float(porc["votos"].sum() / comp),
                    "presidente_PT": int(pres.loc[pres["numero"] == pt, "votos"].sum()),
                    "presidente_direita": int(pres.loc[pres["numero"] == dire, "votos"].sum()),
                    "eleitos_PT": int((eleitos["partido"] == 13).sum()), "eleitos_PL": int((eleitos["partido"] == 22).sum())})
    pd.DataFrame(lin).to_csv(SAI / "a6_a_conta.csv", index=False)
    resumo["a6"] = lin


def a7(resumo: dict) -> None:
    """Curva 'linear demais': variacao da margem entre passos de 2,5% das secoes, ordem real contra 1.000 ordens aleatorias."""
    sec = pd.concat([pd.read_parquet(p) for p in APURACAO_UF.glob("*-secoes.parquet")])
    sec = sec[~sec["agregada"]].dropna(subset=["recebido"])
    vot = pd.concat([pd.read_parquet(p.with_name(p.name.replace("-secoes", "-votos"))) for p in APURACAO_UF.glob("*-secoes.parquet")])
    v = vot[vot["cargo"] == 1]
    chave = ["uf", "mun_cd", "zona", "secao"]
    val = v[v["tipo"] == 1].groupby(chave)["votos"].sum().rename("val")
    f = v[(v["tipo"] == 1) & (v["numero"] == 22)].groupby(chave)["votos"].sum().rename("f")
    l = v[(v["tipo"] == 1) & (v["numero"] == 13)].groupby(chave)["votos"].sum().rename("l")
    s = sec.set_index(chave).join(pd.concat([val, f, l], axis=1)).fillna({"val": 0, "f": 0, "l": 0})
    s = s.sort_values("recebido")
    arr = s[["val", "f", "l"]].to_numpy()
    n = len(arr)
    passos = np.linspace(0, n, 41).astype(int)[1:]

    def incrementos(a):
        c = np.cumsum(a, axis=0)[passos - 1]
        marg = 100 * (c[:, 1] - c[:, 2]) / c[:, 0]
        return np.diff(marg)

    real = incrementos(arr)
    rng = np.random.default_rng(SEMENTE)
    sds, absmed = [], []
    for _ in range(1000):
        inc = incrementos(arr[rng.permutation(n)])
        sds.append(inc.std())
        absmed.append(np.abs(inc).mean())
    resumo["a7"] = {"passos": 40, "sd_incremento_real": float(real.std()), "sd_incremento_aleatorio_p2_5": float(np.percentile(sds, 2.5)),
                    "sd_incremento_aleatorio_p97_5": float(np.percentile(sds, 97.5)), "media_abs_incremento_real": float(np.abs(real).mean()),
                    "media_abs_incremento_aleatorio_mediana": float(np.median(absmed)), "incrementos_reais": [float(x) for x in real]}
    pd.DataFrame({"passo": range(1, len(real) + 1), "incremento_margem_pontos": real}).to_csv(SAI / "a7_incrementos_reais.csv", index=False)


def main() -> None:
    SAI.mkdir(exist_ok=True)
    resumo: dict = {}
    t15(resumo)
    t3_t8(resumo)
    a6(resumo)
    a7(resumo)
    p = SAI / "RESUMO.json"
    tudo = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    tudo.update(resumo)
    p.write_text(json.dumps(tudo, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
