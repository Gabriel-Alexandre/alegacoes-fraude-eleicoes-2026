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


def g02_perfil_por_hora() -> None:
    ph = pd.read_csv(RES / "a2_perfil_por_hora.csv")
    fig, ax = figura("Hora a hora: votos e liberações à mão", "Brasil, horário de Brasília. Barras: votos. Linha: % liberados sem digital (até 21h)")
    ph = ph[(ph["hora"] >= 8) & (ph["hora"] <= 21)]
    tot = ph.groupby("hora")["votos"].sum()
    man = ph[ph["tipo"].isin(["manual_mes", "manual_sem"])].groupby("hora")["votos"].sum().reindex(tot.index, fill_value=0)
    ax.bar(tot.index, tot / 1e6, color="#9aa7b4")
    ax.set_ylabel("milhões de votos")
    ax.set_xlabel("hora")
    ax2 = ax.twinx()
    ax2.plot(tot.index, 100 * man / tot, color=COR["destaque"], lw=5, marker="o")
    ax2.set_ylabel("% liberados sem digital", color=COR["destaque"])
    ax2.spines["top"].set_visible(False)
    ax.axvline(16.5, color="#333", ls="--")
    ax.text(16.6, ax.get_ylim()[1] * 0.95, "17h", fontsize=22)
    ax.set_xticks(range(8, 22), [f"{h}h" for h in range(8, 22)], fontsize=18)
    ax2.set_ylim(0, max(25, float((100 * man / tot).max()) * 1.2))
    fig.subplots_adjust(right=0.9)
    salvar(fig, "g02_perfil_por_hora")


def g03_duracao() -> None:
    a = pd.read_csv(RES / "a2_votos_depois_das_17h.csv").set_index("escopo").loc[["Brasil"] + REGIOES]
    fig, ax = figura("Quanto tempo cada eleitor levou para votar", "Mediana, em segundos, da liberação ao voto computado. A alegação de 2022: \"de 1min40 para 32 s depois das 17h\"")
    x = np.arange(len(a))
    ax.bar(x - 0.27, a["dur_mediana_antes17"], 0.27, color="#9aa7b4", label="antes das 17h")
    ax.bar(x, a["dur_mediana_bio_apos17"], 0.27, color="#5b7da3", label="depois das 17h, com digital")
    ax.bar(x + 0.27, a["dur_mediana_manual_apos17"], 0.27, color=COR["destaque"], label="depois das 17h, sem digital")
    ax.set_xticks(x, a.index)
    ax.set_ylabel("segundos")
    ax.legend(frameon=False, fontsize=18)
    salvar(fig, "g03_duracao_do_voto")


def g06_dose_resposta() -> None:
    t = pd.read_csv(RES / "a1_t19_dose_resposta.csv")
    t = t[t["y"].isin(["p_lula", "p_flavio"]) & t["escopo"].isin(["Brasil"] + REGIOES + ["CE"])]
    fig, ax = figura("Liberação à mão depois das 17h e o voto", "Diferença para as outras seções da mesma escola, por 10 pontos a mais de liberação manual tardia (barra: 95%)")
    esc = ["Brasil"] + REGIOES + ["CE"]
    for k, (y, cor, nome) in enumerate([("p_lula", COR["Lula"], "Lula"), ("p_flavio", COR["Flavio"], "Flávio")]):
        for j, (mod, mk) in enumerate([("apos17", "o"), ("placebo_12_13", "s")]):
            s = t[(t["y"] == y) & (t["modelo"] == mod)].set_index("escopo").reindex(esc)
            pos = np.arange(len(esc)) + (k * 2 + j - 1.5) * 0.15
            ax.errorbar(pos, 10 * s["b1"], yerr=10 * 1.96 * s["ep1"], fmt=mk, color=cor, alpha=1 if mod == "apos17" else 0.45, ms=12, lw=3,
                        label=f"{nome}, {'depois das 17h' if mod == 'apos17' else 'placebo 12h-13h'}")
    ax.axhline(0, color="#999")
    ax.set_xticks(range(len(esc)), [e.replace("CE", "Ceará") for e in esc])
    ax.set_ylabel("pontos percentuais")
    ax.legend(frameon=False, fontsize=16, ncol=2)
    salvar(fig, "g06_dose_resposta")


def g12_ja_votou() -> None:
    t = pd.read_csv(RES / "a1_t112_eleitor_ja_votou.csv")
    t = t[t["escopo"].isin(REGIOES + ["CE"])]
    fig, ax = figura("“O eleitor identificado já votou”", "Episódios por mil votos, nas seções que Lula venceu e nas que Flávio venceu")
    esc = REGIOES + ["CE"]
    x = np.arange(len(esc))
    for k, (lado, cor) in enumerate([("Lula", COR["Lula"]), ("Flavio", COR["Flavio"])]):
        s = t[t["secoes_vencidas_por"] == lado].set_index("escopo").reindex(esc)
        ax.bar(x + (k - 0.5) * 0.4, s["por_mil_votos"], 0.4, color=cor, label=f"seções vencidas por {'Flávio' if lado == 'Flavio' else lado}")
    ax.set_xticks(x, [e.replace("CE", "Ceará") for e in esc])
    ax.set_ylabel("episódios por mil votos")
    ax.legend(frameon=False)
    salvar(fig, "g12_eleitor_ja_votou")


def g13_teto() -> None:
    r = json.loads((RES / "RESUMO.json").read_text(encoding="utf-8"))["a1"]["teto"]
    fig, ax = figura("O teto do pior caso", "Mesmo que todo voto suspeito fosse fraude e fosse de um lado só, quanto ele moveria?")
    itens = [("Votos liberados à mão depois das 17h\nnas seções fora do padrão (S5)", r["manuais_apos17_marcadas_S5"], COR["destaque"]),
             ("Todos os votos liberados à mão\ndepois das 17h no país", r["manuais_apos17_brasil"], "#c9a227"),
             ("Diferença entre Flávio e Lula", r["diferenca_flavio_lula"], COR["neutro"]),
             ("Votos que Flávio precisaria tirar\ndo adversário para chegar a 50%", r["votos_para_flavio_chegar_a_50"], "#333")]
    y = np.arange(len(itens))[::-1]
    for yy, (rot, v, cor) in zip(y, itens):
        ax.barh(yy, v / 1e6, color=cor)
        rot_v = br(v / 1e6, 2) + " milhões" if v >= 1e6 else br(v / 1e3, 1) + " mil"
        ax.text(v / 1e6 + 0.05, yy, rot_v, va="center", fontsize=22)
    ax.set_yticks(y, [i[0] for i in itens], fontsize=18)
    ax.set_xlabel("milhões de votos")
    ax.set_xlim(0, r["votos_para_flavio_chegar_a_50"] / 1e6 * 1.22)
    fig.subplots_adjust(left=0.33)
    salvar(fig, "g13_teto_do_pior_caso")


def g07_quem_vota_tarde() -> None:
    t = pd.read_csv(RES / "x_exploratoria.csv")
    t = t[(t["teste"].str.startswith("X2")) & (t["y"] == "p_lula") & t["x"].isin(["f_manual_apos17", "f_bio_apos17"])]
    esc = ["Brasil"] + REGIOES + ["CE"]
    fig, ax = figura("O que pesa: a liberação à mão ou quem vota tarde?", "Os dois no mesmo modelo, dentro da mesma escola: efeito no voto em Lula por 10 pontos")
    for k, (x, cor, nome) in enumerate([("f_manual_apos17", COR["destaque"], "liberados à mão depois das 17h"), ("f_bio_apos17", "#5b7da3", "liberados pela digital depois das 17h (pessoa presente)")]):
        s = t[t["x"] == x].set_index("escopo").reindex(esc)
        pos = np.arange(len(esc)) + (k - 0.5) * 0.3
        ax.errorbar(pos, 10 * s["coef"], yerr=10 * 1.96 * s["ep"], fmt="o", color=cor, ms=13, lw=3, label=nome)
    ax.axhline(0, color="#999")
    ax.set_xticks(range(len(esc)), [e.replace("CE", "Ceará") for e in esc])
    ax.set_ylabel("pontos percentuais")
    ax.legend(frameon=False, fontsize=18, loc="upper left")
    salvar(fig, "g07_quem_vota_tarde")


def main() -> None:
    for f in (g01_manual_antes_depois, g02_perfil_por_hora, g03_duracao, g04_serie_contador, g06_dose_resposta, g07_quem_vota_tarde, g08_a_conta, g09_curva, g12_ja_votou, g13_teto):
        try:
            f()
            print("ok", f.__name__)
        except FileNotFoundError as e:
            print("falta", f.__name__, e)


if __name__ == "__main__":
    main()
