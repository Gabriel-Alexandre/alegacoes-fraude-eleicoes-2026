# ESTADO

**13/out/2026** · ✅ **executado de ponta a ponta.** Plano aprovado; pré-registro com 12 emendas (quatro feitas depois de ver resultado, marcadas); 499.161 logs de urna (53,4 GB) lidos e validados; relatório, resumo simples, revisão adversarial, gráficos, pedidos por LAI e convite público prontos.

## Onde está cada coisa

| | |
|---|---|
| Resultados | `RELATORIO.md` (completo) e `RESUMO_SIMPLES.md` |
| Critérios | `docs/PRE_REGISTRO.md` (emendas na §9) |
| Validação do leitor | `docs/VALIDACAO_DO_LEITOR.md` (log contra o contador oficial do TSE: 495.745 de 495.745 seções idênticas) |
| Fontes | `docs/VERIFICACAO_DE_FONTES.md` |
| Revisão | `docs/REVISAO_ADVERSARIAL.md` |
| Pedidos e convite | `docs/PEDIDOS_LAI.md` (não protocolados) e `docs/CONVITE_PUBLICO.md` |
| Gráficos | `resultados/figuras/` (1920×1080) |
| Dados e como apagar | `docs/DADOS_LOCAIS.md` |

## ⬜ Decisões do autor

Protocolar os pedidos (se o público engajar) · fazer o convite público · ✅ **`dados/` apagado em 14/out/2026**, com o vídeo 8 pronto (~64 GB; o que ficou e como refazer em `docs/DADOS_LOCAIS.md`). ✅ Repositório **público** desde 13/out/2026 (decisão do autor), sem licença.

## Como refazer tudo

Guia completo, com a dependência do projeto `apuracao-eleicoes-2026`: [`docs/REPLICAR.md`](docs/REPLICAR.md).


`python -m alegacoes.coleta_logs todas 75` → `python ferramentas/baixar-bweb.py` → `python -m alegacoes.derivar_logs todas` → `python -m alegacoes.bweb 2014,2018,2020,2022,2024,2026 todas` → `python -m alegacoes.secoes todas` → `python ferramentas/analise-2-series-e-contas.py` → `python ferramentas/analise-1-mesarios-e-17h.py` → `python ferramentas/analise-3-exploratoria.py` → `python ferramentas/analise-4-locais.py` → `python ferramentas/analise-5-sem-digital.py` → `python ferramentas/graficos.py` → `python ferramentas/dados-locais.py`. Validação: `python ferramentas/validacao-independente.py 3000` e `python ferramentas/leitura-manual.py`.
