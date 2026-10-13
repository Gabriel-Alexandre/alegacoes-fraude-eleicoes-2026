"""Analises EXPLORATORIAS, feitas DEPOIS de ver o T1.9 (registradas como tal no PRE_REGISTRO, emenda E10).

Pergunta: a associacao entre "votos liberados a mao depois das 17h" e o voto em Lula, dentro da mesma escola,
vem da liberacao manual (o que a alegacao preve) ou de QUEM vota tarde (a fila)?

X1  o mesmo modelo do T1.9 com as liberacoes POR DIGITAL depois das 17h no lugar das manuais. Voto por digital e de
    pessoa presente: se a associacao for parecida, ela vem da fila, nao da liberacao manual.
X2  os dois juntos (manual depois das 17h e digital depois das 17h) mais a manual antes das 17h.
X3  o EXCESSO de liberacao manual no fim do dia: (manuais/votos depois das 17h) - (manuais/votos antes das 17h),
    em secoes com pelo menos 20 votos depois das 17h. A fraude por mesario aumenta esse excesso; a fila nao.
X4  comparecimento contra a fracao manual depois das 17h (a fraude por ausente preve comparecimento MAIOR).

Saida: resultados/x_exploratoria.csv e o bloco "exploratoria" de RESUMO.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "ferramentas"))
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("a1", RAIZ / "ferramentas" / "analise-1-mesarios-e-17h.py")
a1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a1)


def fe(d: pd.DataFrame, y: str, xs: list[str], escopo: str, nome: str, filtro=None) -> list[dict]:
    s = d[d["cob100"] & d[y].notna() & (d["n_votos"] >= 50)].copy()
    if filtro is not None:
        s = s[filtro(s)]
    s["n_local"] = s.groupby(["uf", "mun", "local"])["secao"].transform("count")
    s = s[s["n_local"] >= 2].dropna(subset=xs)
    if len(s) < 100:
        return []
    for c in [y] + xs:
        s[c + "_dm"] = s[c] - s.groupby(["uf", "mun", "local"])[c].transform("mean")
    mod = sm.OLS(s[y + "_dm"].to_numpy(), s[[x + "_dm" for x in xs]].to_numpy()).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(s["uf"] + s["mun"].astype(str))[0]})
    return [{"teste": nome, "escopo": escopo, "y": y, "x": x, "n": len(s), "coef": mod.params[i], "ep": mod.bse[i], "p": mod.pvalues[i]}
            for i, x in enumerate(xs)]


def main() -> None:
    d = a1.carregar()
    d["n_bio_apos17"] = d["n_votos_apos17"] - d["n_manual_apos17"]
    d["f_bio_apos17"] = d["n_bio_apos17"] / d["n_votos"]
    d["f_votos_apos17"] = d["n_votos_apos17"] / d["n_votos"]
    antes = (d["n_votos"] - d["n_votos_apos17"]).replace(0, np.nan)
    d["excesso_manual_tarde"] = d["n_manual_apos17"] / d["n_votos_apos17"].replace(0, np.nan) - d["n_manual_antes17"] / antes
    linhas = []
    regioes = sorted(set(a1.REGIAO.values()))
    for escopo, s in [("Brasil", d)] + [(r, d[d["regiao"] == r]) for r in regioes] + [("CE", d[d["uf"] == "CE"])]:
        for y in ("p_lula", "p_flavio"):
            linhas += fe(s, y, ["f_bio_apos17", "f_manual_antes17"], escopo, "X1 digital depois das 17h")
            linhas += fe(s, y, ["f_manual_apos17", "f_bio_apos17", "f_manual_antes17"], escopo, "X2 manual e digital depois das 17h")
            linhas += fe(s, y, ["excesso_manual_tarde"], escopo, "X3 excesso de manual no fim do dia", filtro=lambda x: x["n_votos_apos17"] >= 20)
        linhas += fe(s, "comp_taxa", ["f_manual_apos17", "f_manual_antes17"], escopo, "X4 comparecimento")
    t = pd.DataFrame(linhas)
    t.to_csv(a1.SAI / "x_exploratoria.csv", index=False)
    # descricao do excesso: a fracao manual depois das 17h e maior que antes em quantas secoes?
    s = d[d["cob100"] & (d["n_votos_apos17"] >= 20)]
    desc = {"secoes_com_20_ou_mais_votos_apos17": len(s), "excesso_medio_pontos": float(100 * s["excesso_manual_tarde"].mean()),
            "secoes_com_excesso_acima_de_20_pontos": int((s["excesso_manual_tarde"] > 0.20).sum())}
    p = a1.SAI / "RESUMO.json"
    tudo = json.loads(p.read_text(encoding="utf-8"))
    tudo["exploratoria"] = {"testes": t.to_dict(orient="records"), "excesso": desc}
    p.write_text(json.dumps(tudo, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print(t.round(4).to_string())
    print(desc)


if __name__ == "__main__":
    main()
