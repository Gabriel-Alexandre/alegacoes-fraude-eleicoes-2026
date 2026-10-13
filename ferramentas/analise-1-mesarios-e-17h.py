"""Testes de A1 (mesarios e o voto no lugar de quem faltou, com H1b) e A2 (votos depois das 17h).

Criterios: docs/PRE_REGISTRO.md secoes 3 e 4, com as emendas E1 a E6. Le dados/derivados/secoes/*.parquet.
Saidas em resultados/a1_*.csv, resultados/a2_*.csv e o bloco "a1"/"a2" de resultados/RESUMO.json.

Uso: python ferramentas/analise-1-mesarios-e-17h.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
SAI = RAIZ / "resultados"
REGIAO = {
    **dict.fromkeys(["AC", "AP", "AM", "PA", "RO", "RR", "TO"], "Norte"),
    **dict.fromkeys(["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"], "Nordeste"),
    **dict.fromkeys(["DF", "GO", "MT", "MS"], "Centro-Oeste"),
    **dict.fromkeys(["ES", "MG", "RJ", "SP"], "Sudeste"),
    **dict.fromkeys(["PR", "RS", "SC"], "Sul"),
}
SEMENTE = 20261013
MARCAS = ["S5", "S3", "S10", "S5abs", "C3", "J"]


def carregar() -> pd.DataFrame:
    d = pd.concat([pd.read_parquet(p) for p in sorted((RAIZ / "dados" / "derivados" / "secoes").glob("*.parquet"))], ignore_index=True)
    d = d[d["uf"] != "ZZ"].copy()
    d["regiao"] = d["uf"].map(REGIAO)
    d["validos_pres"] = d["validos_pres"].fillna(0)
    d["p_lula"] = d["lula"] / d["validos_pres"].where(d["validos_pres"] > 0)
    d["p_flavio"] = d["flavio"] / d["validos_pres"].where(d["validos_pres"] > 0)
    d["comp_taxa"] = d["comp_bu"] / d["aptos_bu"]
    d["n_manual"] = d["n_manual_mes"] + d["n_manual_sem"]
    d["f_manual_apos17"] = d["n_manual_apos17"] / d["n_votos"]
    d["f_manual_antes17"] = d["n_manual_antes17"] / d["n_votos"]
    d["f_manual_12_13"] = d["n_manual_12_13"] / d["n_votos"]
    d["f_manual_fora_12_13"] = (d["n_manual"] - d["n_manual_12_13"]) / d["n_votos"]
    d["cob100"] = d["cobertura_log"] == 1
    # marca conjunta J (H1b): S5, um so mesario identificado (ou so 'nao_id'), comparecimento >= mediana das outras do local + 5 pontos
    g = d.groupby(["uf", "mun", "local"])["comp_taxa"]
    soma, cont = g.transform("sum"), g.transform("count")
    d["comp_outras_local"] = (soma - d["comp_taxa"]) / (cont - 1)
    med_outras = d.groupby(["uf", "mun", "local"])["comp_taxa"].transform(lambda s: s.median())
    d["J"] = d["S5"] & (d["seq_mesarios_ident"] <= 1) & (d["comp_taxa"] >= med_outras + 0.05) & (cont >= 3)
    return d


def desvios_no_local(d: pd.DataFrame, col: str) -> pd.Series:
    """valor da secao menos a media das OUTRAS secoes do mesmo local de votacao."""
    g = d.groupby(["uf", "mun", "local"])[col]
    soma, cont = g.transform("sum"), g.transform("count")
    return d[col] - (soma - d[col]) / (cont - 1)


def t13(d: pd.DataFrame, marca: str, rng: np.random.Generator, n_sorteios: int = 10000) -> list[dict]:
    """T1.3: desvio medio das marcadas contra as outras do local, e placebo por permutacao dentro dos locais."""
    base = d[d["cob100"]].copy()
    base["n_local"] = base.groupby(["uf", "mun", "local"])["secao"].transform("count")
    base = base[base["n_local"] >= 3]
    out = []
    for escopo, sub in [("Brasil", base)] + [(r, base[base["regiao"] == r]) for r in sorted(set(REGIAO.values()))] + [("CE", base[base["uf"] == "CE"])]:
        sub = sub.copy()
        for col in ("p_lula", "p_flavio", "comp_taxa"):
            sub[f"dv_{col}"] = desvios_no_local(sub, col)
        marc = sub[sub[marca]]
        linha = {"marca": marca, "escopo": escopo, "secoes": len(sub), "marcadas": len(marc),
                 "votos_manuais_apos17_marcadas": int(marc["n_manual_apos17"].sum())}
        if len(marc) == 0:
            out.append(linha)
            continue
        # placebo: em cada local com secao marcada, sorteia o mesmo numero de secoes do local (sem reposicao)
        locais = marc.groupby(["uf", "mun", "local"]).size()
        sub = sub.sort_values(["uf", "mun", "local"])
        chave_sub = list(zip(sub["uf"], sub["mun"], sub["local"]))
        pos = {}
        for i, k in enumerate(chave_sub):
            pos.setdefault(k, []).append(i)
        for col in ("p_lula", "p_flavio", "comp_taxa"):
            vals = sub[f"dv_{col}"].to_numpy()
            obs = float(np.nanmean(marc[f"dv_{col}"].to_numpy()))
            um = [(np.array(pos[k]), int(n)) for k, n in locais.items() if n == 1]
            varios = [(np.array(pos[k]), int(n)) for k, n in locais.items() if n > 1]
            total_marc = int(locais.sum())
            soma = np.zeros(n_sorteios)
            if um:
                tamanhos = np.array([len(a) for a, _ in um])
                inicio = np.concatenate([[0], np.cumsum(tamanhos)[:-1]])
                todos = np.concatenate([a for a, _ in um])
                escolha = inicio + (rng.random((n_sorteios, len(um))) * tamanhos).astype(int)
                soma += np.nansum(vals[todos[escolha]], axis=1)
            for a, n in varios:
                for s in range(n_sorteios):
                    soma[s] += np.nansum(vals[rng.choice(a, size=min(n, len(a)), replace=False)])
            sorteios = soma / total_marc
            linha[f"{col}_desvio"] = obs
            linha[f"{col}_placebo_media"] = float(sorteios.mean())
            linha[f"{col}_p_maior"] = float((sorteios >= obs).mean())
            linha[f"{col}_p_menor"] = float((sorteios <= obs).mean())
        out.append(linha)
    return out


def t19(d: pd.DataFrame, y: str, x1: str, x2: str, escopo: str) -> dict:
    """T1.9: y = b1*x1 + b2*x2 + efeito fixo do local; erro agrupado por municipio."""
    s = d[d["cob100"] & d[y].notna() & (d["n_votos"] >= 50)].copy()
    s["n_local"] = s.groupby(["uf", "mun", "local"])["secao"].transform("count")
    s = s[s["n_local"] >= 2]
    if len(s) < 100:
        return {"escopo": escopo, "y": y, "x1": x1, "n": len(s)}
    for c in (y, x1, x2):
        s[c + "_dm"] = s[c] - s.groupby(["uf", "mun", "local"])[c].transform("mean")
    X = s[[x1 + "_dm", x2 + "_dm"]].to_numpy()
    mod = sm.OLS(s[y + "_dm"].to_numpy(), X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(s["uf"] + s["mun"].astype(str))[0]})
    return {"escopo": escopo, "y": y, "x1": x1, "x2": x2, "n": len(s), "b1": mod.params[0], "ep1": mod.bse[0], "p1": mod.pvalues[0],
            "b2": mod.params[1], "ep2": mod.bse[1], "p2": mod.pvalues[1]}


def main() -> None:
    SAI.mkdir(exist_ok=True)
    d = carregar()
    # a tabela por secao vai para o git (sem dado pessoal: so contagens), para reproduzir sem os brutos
    (SAI / "dados").mkdir(exist_ok=True)
    d.to_csv(SAI / "dados" / "secoes_2026.csv.gz", index=False, compression="gzip")
    rng = np.random.default_rng(SEMENTE)
    resumo: dict = {"a1": {}, "a2": {}}
    regioes = sorted(set(REGIAO.values()))

    # ---------- inventario e marcas
    inv = []
    for escopo, s in [("Brasil", d)] + [(r, d[d["regiao"] == r]) for r in regioes] + [("CE", d[d["uf"] == "CE"])]:
        linha = {"escopo": escopo, "secoes": len(s), "secoes_cob100": int(s["cob100"].sum()), "votos": int(s["n_votos"].sum()),
                 "bio": int(s["n_bio"].sum()), "manual_mes": int(s["n_manual_mes"].sum()), "manual_sem": int(s["n_manual_sem"].sum()),
                 "outra": int(s["n_outra"].sum()), "votos_apos17": int(s["n_votos_apos17"].sum()),
                 "manual_apos17": int(s["n_manual_apos17"].sum()), "manual_antes17": int(s["n_manual_antes17"].sum()),
                 "nao_confere": int(s["n_nao_confere"].sum()), "sem_habilitacao": int(s["n_sem_habilitacao"].sum()),
                 "suspenso_mesario": int(s["n_suspenso_mesario"].sum()), "contingencia": int(s["contingencia"].sum())}
        for m in MARCAS:
            linha[f"marcadas_{m}"] = int(s[m].sum())
        inv.append(linha)
    inv = pd.DataFrame(inv)
    inv["pct_manual"] = 100 * (inv["manual_mes"] + inv["manual_sem"]) / inv["votos"]
    inv["pct_manual_antes17"] = 100 * inv["manual_antes17"] / (inv["votos"] - inv["votos_apos17"])
    inv["pct_manual_apos17"] = 100 * inv["manual_apos17"] / inv["votos_apos17"]
    inv["pct_votos_apos17"] = 100 * inv["votos_apos17"] / inv["votos"]
    inv.to_csv(SAI / "a1_inventario.csv", index=False)
    resumo["a1"]["inventario"] = inv.to_dict(orient="records")

    # ---------- T1.3 (desfecho das marcadas, com placebo)
    t13_lin = []
    for m in MARCAS:
        t13_lin += t13(d, m, rng, n_sorteios=2000 if m != "S5" else 10000)
    t13_df = pd.DataFrame(t13_lin)
    t13_df.to_csv(SAI / "a1_t13_desfecho_das_marcadas.csv", index=False)
    resumo["a1"]["t13"] = t13_df.to_dict(orient="records")

    # ---------- T1.9 (dose e resposta) e o placebo 12h-13h
    t19_lin = []
    for escopo, s in [("Brasil", d)] + [(r, d[d["regiao"] == r]) for r in regioes] + [("CE", d[d["uf"] == "CE"])]:
        for y in ("p_lula", "p_flavio"):
            r = t19(s, y, "f_manual_apos17", "f_manual_antes17", escopo)
            r["modelo"] = "apos17"
            t19_lin.append(r)
            r = t19(s, y, "f_manual_12_13", "f_manual_fora_12_13", escopo)
            r["modelo"] = "placebo_12_13"
            t19_lin.append(r)
    ce = d[d["uf"] == "CE"].copy()
    if "gov_1" in ce and len(ce):
        ce["p_gov_1"] = ce["gov_1"] / ce["validos_gov"]
        ce["p_gov_2"] = ce["gov_2"] / ce["validos_gov"]
        for y in ("p_gov_1", "p_gov_2"):
            r = t19(ce, y, "f_manual_apos17", "f_manual_antes17", "CE governador")
            r["modelo"] = "apos17"
            t19_lin.append(r)
        resumo["a1"]["ce_governador_numeros"] = {"gov_1": int(ce["gov_1_numero"].dropna().iloc[0]), "gov_2": int(ce["gov_2_numero"].dropna().iloc[0])}
    t19_df = pd.DataFrame(t19_lin)
    t19_df.to_csv(SAI / "a1_t19_dose_resposta.csv", index=False)
    resumo["a1"]["t19"] = t19_df.to_dict(orient="records")


    # ---------- T1.12 o evento "eleitor ja votou" (emenda E7), com espelho por quem venceu a secao
    d["vence"] = np.where(d["lula"] > d["flavio"], "Lula", np.where(d["flavio"] > d["lula"], "Flavio", "empate"))
    t112 = []
    for escopo, s in [("Brasil", d)] + [(r, d[d["regiao"] == r]) for r in regioes] + [("CE", d[d["uf"] == "CE"])]:
        for lado in ("todas", "Lula", "Flavio"):
            g = s if lado == "todas" else s[s["vence"] == lado]
            t112.append({"escopo": escopo, "secoes_vencidas_por": lado, "secoes": len(g), "votos": int(g["n_votos"].sum()),
                         "episodios_ja_votou": int(g["n_ep_ja_votou"].sum()), "episodios_apos17": int(g["n_ep_ja_votou_apos17"].sum()),
                         "por_mil_votos": 1000 * g["n_ep_ja_votou"].sum() / max(1, g["n_votos"].sum()),
                         "secoes_com_episodio": int((g["n_ep_ja_votou"] > 0).sum()),
                         "secoes_com_3_ou_mais": int((g["n_ep_ja_votou"] >= 3).sum())})
    t112 = pd.DataFrame(t112)
    t112.to_csv(SAI / "a1_t112_eleitor_ja_votou.csv", index=False)
    resumo["a1"]["t112"] = t112.to_dict(orient="records")

    # ---------- V4: o log contra o contador oficial (eleitores com biometria liberados sem ela)
    v4 = d.loc[d["cob100"] & d["biom_nh"].notna(), ["uf", "n_manual_mes", "biom_nh"]]
    resumo["validacao_v4"] = {"secoes": len(v4), "iguais": int((v4["n_manual_mes"] == v4["biom_nh"]).sum()),
                              "soma_log_manual_mes": int(v4["n_manual_mes"].sum()), "soma_oficial": int(v4["biom_nh"].sum()),
                              "por_uf": v4.groupby("uf").agg(log=("n_manual_mes", "sum"), oficial=("biom_nh", "sum")).reset_index().to_dict(orient="records")}

    # ---------- T1.7 teto do pior caso e T1.8
    validos = float(d["validos_pres"].sum())
    lula, flavio = float(d["lula"].sum()), float(d["flavio"].sum())
    precisa_50 = validos * (1 - 2 * flavio / validos)
    resumo["a1"]["teto"] = {
        "validos_presidente_secoes_com_log": validos, "lula": lula, "flavio": flavio, "diferenca_flavio_lula": flavio - lula,
        "votos_para_flavio_chegar_a_50": precisa_50,
        "manuais_apos17_brasil": int(d["n_manual_apos17"].sum()),
        "manuais_apos17_marcadas_S5": int(d.loc[d["S5"], "n_manual_apos17"].sum()),
        "manuais_apos17_marcadas_S3": int(d.loc[d["S3"], "n_manual_apos17"].sum()),
        "manuais_dia_todo_brasil": int(d["n_manual"].sum()),
    }

    # ---------- A2
    a2 = []
    for escopo, s in [("Brasil", d)] + [(r, d[d["regiao"] == r]) for r in regioes] + [("CE", d[d["uf"] == "CE"]), ("BA", d[d["uf"] == "BA"])]:
        c = s[s["cob100"]]
        a2.append({"escopo": escopo, "votos_apos17": int(s["n_votos_apos17"].sum()),
                   "secoes_ultimo_voto_apos_18h": int((s["ultimo_voto_b"] >= 18 * 3600).sum()),
                   "secoes_ultimo_voto_apos_19h": int((s["ultimo_voto_b"] >= 19 * 3600).sum()),
                   "secoes_ultimo_voto_apos_20h": int((s["ultimo_voto_b"] >= 20 * 3600).sum()),
                   "secoes_ultimo_voto_apos_21h": int((s["ultimo_voto_b"] >= 21 * 3600).sum()),
                   "pct_manual_antes17": 100 * c["n_manual_antes17"].sum() / (c["n_votos"] - c["n_votos_apos17"]).sum(),
                   "pct_manual_apos17": 100 * c["n_manual_apos17"].sum() / max(1, c["n_votos_apos17"].sum()),
                   "pct_manual_mes_apos17": 100 * c["n_manual_mes_apos17"].sum() / max(1, c["n_votos_apos17"].sum()),
                   "pct_manual_sem_apos17": 100 * c["n_manual_sem_apos17"].sum() / max(1, c["n_votos_apos17"].sum()),
                   "dur_mediana_antes17": float(c["dur_mediana_antes17"].median()), "dur_mediana_apos17": float(c["dur_mediana_apos17"].median()),
                   "dur_mediana_manual_apos17": float(c["dur_mediana_manual_apos17"].median()),
                   "dur_mediana_bio_apos17": float(c["dur_mediana_bio_apos17"].median())})
    a2 = pd.DataFrame(a2)
    a2["razao_manual_apos_antes"] = a2["pct_manual_apos17"] / a2["pct_manual_antes17"]
    a2.to_csv(SAI / "a2_votos_depois_das_17h.csv", index=False)
    resumo["a2"]["por_escopo"] = a2.to_dict(orient="records")

    # T2.3 modelo do voto tardio, por UF
    t23 = []
    for uf, s in d[d["cob100"]].groupby("uf"):
        s = s.dropna(subset=["p10_intervalo_manha", "aptos_bu", "comp_bu"])
        X = sm.add_constant(s[["aptos_bu", "comp_bu", "p10_intervalo_manha", "f_manual_antes17"]])
        mod = sm.OLS(s["n_votos_apos17"], X).fit()
        s = s.assign(resid=mod.resid, quintil=pd.qcut(s["aptos_bu"], 5, labels=False, duplicates="drop"))
        por_q = s.groupby("quintil")["resid"].mean().to_dict()
        t23.append({"uf": uf, "r2": mod.rsquared, "n": len(s), **{f"resid_medio_quintil_{int(k) + 1}": v for k, v in por_q.items()}})
    pd.DataFrame(t23).to_csv(SAI / "a2_t23_modelo_voto_tardio.csv", index=False)
    resumo["a2"]["t23"] = t23

    # T2.4 secoes com voto depois das 19h e 21h (lista)
    tard = d[d["ultimo_voto_b"] >= 19 * 3600][["uf", "mun", "zona", "secao", "local", "ultimo_voto_b", "n_votos", "n_votos_apos17",
                                                "n_manual_apos17", "aptos_bu", "comp_bu", "contingencia"]]
    tard = tard.sort_values("ultimo_voto_b", ascending=False)
    tard.to_csv(SAI / "a2_t24_secoes_depois_das_19h.csv", index=False)
    resumo["a2"]["t24_secoes_depois_19h"] = len(tard)
    resumo["a2"]["t24_secoes_depois_21h"] = int((tard["ultimo_voto_b"] >= 21 * 3600).sum())

    p = SAI / "RESUMO.json"
    tudo = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    tudo.update(resumo)
    p.write_text(json.dumps(tudo, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print("ok", len(d), "secoes")


if __name__ == "__main__":
    main()
