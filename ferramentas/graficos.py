"""Graficos 1920x1080 dos resultados (resultados/figuras/). Le os CSV de resultados/ e o RESUMO.json.

Uso: python ferramentas/graficos.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "resultados"
FIG = RES / "figuras"
FONTE = "Fonte: logs das urnas e boletins de urna do TSE; análise do repositório alegacoes-fraude-eleicoes-2026"
COR = {"Lula": "#c0392b", "Flavio": "#1f5fa8", "neutro": "#555555", "destaque": "#e0a100"}
REGIOES = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

plt.rcParams.update({"font.size": 22, "axes.titlesize": 34, "axes.titleweight": "bold", "axes.spines.top": False,
                     "axes.spines.right": False, "font.family": "DejaVu Sans"})


def figura(titulo: str, subtitulo: str = ""):
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.82, bottom=0.14)
    fig.text(0.08, 0.93, titulo, fontsize=38, fontweight="bold")
    if subtitulo:
        fig.text(0.08, 0.875, subtitulo, fontsize=24, color="#444")
    fig.text(0.08, 0.03, FONTE, fontsize=16, color="#777")
    return fig, ax


def salvar(fig, nome: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{nome}.png")
    plt.close(fig)


def br(x: float, casas: int = 1) -> str:
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def g01_manual_antes_depois() -> None:
    a = pd.read_csv(RES / "a2_votos_depois_das_17h.csv").set_index("escopo").loc[REGIOES + ["CE"]]
    fig, ax = figura("Liberação sem digital: antes e depois das 17h", "Porcentagem dos votos liberados à mão (ano de nascimento), por região")
    x = np.arange(len(a))
    ax.bar(x - 0.2, a["pct_manual_antes17"], 0.4, color="#9aa7b4", label="antes das 17h")
    ax.bar(x + 0.2, a["pct_manual_apos17"], 0.4, color=COR["destaque"], label="depois das 17h")
    for i, (u, v) in enumerate(zip(a["pct_manual_antes17"], a["pct_manual_apos17"])):
        ax.text(i - 0.2, u + 0.2, br(u) + "%", ha="center", fontsize=20)
        ax.text(i + 0.2, v + 0.2, br(v) + "%", ha="center", fontsize=20)
    ax.set_xticks(x, [i.replace("CE", "Ceará") for i in a.index])
    ax.set_ylabel("% dos votos")
    ax.legend(frameon=False)
    salvar(fig, "g01_manual_antes_depois_17h")


def g04_serie_contador() -> None:
    t = pd.read_csv(RES / "t15_serie_contador_sem_biometria.csv")
    fig, ax = figura("Eleitores com digital liberados sem ela, 2018 a 2026", "Porcentagem do comparecimento. Em 2020 a biometria foi suspensa (pandemia)")
    for esc in REGIOES:
        s = t[(t["escopo"] == esc) & (t["ano"] != 2020)]
        cor = COR["destaque"] if esc == "Nordeste" else "#9aa7b4"
        lw = 6 if esc == "Nordeste" else 3
        ax.plot(s["ano"], s["taxa_nh_pct"], marker="o", lw=lw, color=cor)
        ajuste = {"Centro-Oeste": 0.12, "Sudeste": -0.12}.get(esc, 0)
        ax.text(2026.15, s["taxa_nh_pct"].iloc[-1] + ajuste, esc, va="center", fontsize=20, color=cor)
    ax.axvspan(2024.2, 2025.8, color="#eee")
    ax.text(2025, ax.get_ylim()[1] * 0.97, "campanha de fiscais\n(2026)", ha="center", va="top", fontsize=18, color="#666")
    ax.set_xticks([2018, 2022, 2024, 2026])
    ax.set_xlim(2017.5, 2027.3)
    ax.set_ylabel("% do comparecimento")
    salvar(fig, "g04_serie_contador_sem_biometria")


def g08_a_conta() -> None:
    a = pd.read_csv(RES / "a6_a_conta.csv").set_index("ano").loc[2026]
    fig, ax = figura("“A conta não fecha”: a soma compara coisas diferentes", "1º turno de 2026, milhões de votos. Cada eleitor votou em dois senadores")
    rot = ["Senadores\neleitos do PT", "Todos os candidatos\ndo PT ao Senado", "Lula", "Senadores\neleitos do PL", "Todos os candidatos\ndo PL ao Senado", "Flávio"]
    val = [a["senado_eleitos_PT"], a["senado_todos_PT"], a["presidente_PT"], a["senado_eleitos_PL"], a["senado_todos_PL"], a["presidente_direita"]]
    cores = ["#e8a49c", "#e8a49c", COR["Lula"], "#9cb8e0", "#9cb8e0", COR["Flavio"]]
    ax.bar(range(6), np.array(val) / 1e6, color=cores)
    for i, v in enumerate(val):
        ax.text(i, v / 1e6 + 0.8, br(v / 1e6), ha="center", fontsize=22)
    ax.set_xticks(range(6), rot, fontsize=18)
    ax.set_ylabel("milhões de votos")
    salvar(fig, "g08_a_conta_nao_fecha")


def g09_curva() -> None:
    r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))["a7"]
    inc = np.array(r["incrementos_reais"])
    fig, ax = figura("A curva da apuração não é “lisa demais”", "Mudança da vantagem de Flávio a cada 2,5% das seções: ordem real e o que a sorte daria")
    ax.bar(range(1, len(inc) + 1), inc, color=COR["neutro"], label="ordem real de chegada")
    ax.axhspan(-2 * r["sd_incremento_aleatorio_p97_5"], 2 * r["sd_incremento_aleatorio_p97_5"], color=COR["destaque"], alpha=0.35,
               label="faixa das ordens sorteadas")
    ax.axhline(0, color="#999")
    ax.set_xlabel("atualização (cada uma = 2,5% das seções)")
    ax.set_ylabel("variação da vantagem (pontos)")
    ax.legend(frameon=False)
    salvar(fig, "g09_curva_nao_e_lisa")


def main() -> None:
    for f in (g01_manual_antes_depois, g04_serie_contador, g08_a_conta, g09_curva):
        try:
            f()
            print("ok", f.__name__)
        except FileNotFoundError as e:
            print("falta", f.__name__, e)


if __name__ == "__main__":
    main()
