"""X5/X6 (exploratorios, emenda E12, depois de ver o resultado): a liberacao de quem NAO tem digital cadastrada
(so o ano de nascimento) sobe depois das 17h em todas as regioes. Ela se associa ao voto e ao comparecimento?

X6: dentro da mesma escola, p_lula (e p_flavio, comp_taxa) ~ f_sem_apos17 + f_mes_apos17 + f_bio_apos17 + f_manual_antes17
X7: o excesso de "sem digital" no fim do dia: (sem/votos depois das 17h) - (sem/votos antes), secoes com >= 20 votos tardios
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("x", RAIZ / "ferramentas" / "analise-3-exploratoria.py")
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)


def main() -> None:
    d = x.a1.carregar()
    d["f_sem_apos17"] = d["n_manual_sem_apos17"] / d["n_votos"]
    d["f_mes_apos17"] = d["n_manual_mes_apos17"] / d["n_votos"]
    d["f_bio_apos17"] = (d["n_votos_apos17"] - d["n_manual_apos17"]) / d["n_votos"]
    antes = (d["n_votos"] - d["n_votos_apos17"]).replace(0, np.nan)
    d["excesso_sem_tarde"] = d["n_manual_sem_apos17"] / d["n_votos_apos17"].replace(0, np.nan) - (d["n_manual_sem"] - d["n_manual_sem_apos17"]) / antes
    lin = []
    for escopo, s in [("Brasil", d)] + [(r, d[d["regiao"] == r]) for r in sorted(set(x.a1.REGIAO.values()))] + [("CE", d[d["uf"] == "CE"])]:
        for y in ("p_lula", "p_flavio", "comp_taxa"):
            lin += x.fe(s, y, ["f_sem_apos17", "f_mes_apos17", "f_bio_apos17", "f_manual_antes17"], escopo, "X6 sem digital, mesario e digital depois das 17h")
            lin += x.fe(s, y, ["excesso_sem_tarde"], escopo, "X7 excesso de sem digital no fim do dia", filtro=lambda z: z["n_votos_apos17"] >= 20)
    t = pd.DataFrame(lin)
    t.to_csv(x.a1.SAI / "x6_sem_digital.csv", index=False)
    p = x.a1.SAI / "RESUMO.json"
    r = json.loads(p.read_text(encoding="utf-8"))
    r.setdefault("exploratoria", {})["x6_x7"] = t.to_dict(orient="records")
    p.write_text(json.dumps(r, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    sel = t[t["x"].isin(["f_sem_apos17", "excesso_sem_tarde"])]
    print(sel[["teste", "escopo", "y", "x", "n", "coef", "ep", "p"]].round(4).to_string())


if __name__ == "__main__":
    main()
