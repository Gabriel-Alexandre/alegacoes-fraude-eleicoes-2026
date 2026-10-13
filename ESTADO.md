# ESTADO

**13/out/2026** · plano aprovado; pré-registro gravado (emendas E1 a E9); coleta dos 499.161 logs em andamento.

## Feito

1. ✅ Plano aprovado e melhorias (§13 do plano)
2. ✅ Pré-registro em commit (`3312d5c`), emendas E1 a E9
3. ✅ CSV oficiais de 2014 a 2026 baixados e lidos
4. ✅ Leitor do log validado: reconciliação (99,7%), Manaus contra o quehorasvotar, segundo leitor (100% em 2.000 seções), leitura à mão (74 eleitores), contador oficial (AM, 0,15%) — `docs/VALIDACAO_DO_LEITOR.md`
5. ✅ Testes que dependem só dos CSV (`ferramentas/analise-2-series-e-contas.py`)
6. ✅ Verificação de fontes (1ª rodada), pedidos por LAI e convite público (não protocolados)

## Falta

- ⏳ terminar a coleta dos logs; rodar `derivar_logs`, `secoes` e `ferramentas/analise-1-mesarios-e-17h.py` no país
- ⬜ validação final nas 28 UFs (reconciliação, segundo leitor, V4, leitura à mão com todas as categorias)
- ⬜ revisão adversarial em dois papéis e conferência de viés
- ⬜ relatório, resumo simples, gráficos, `docs/DADOS_LOCAIS.md`

## Como retomar

`python -m alegacoes.coleta_logs todas 75` (retoma de onde parou) → `python -m alegacoes.derivar_logs todas` → `python -m alegacoes.bweb 2014,2018,2020,2022,2024,2026 todas` → `python -m alegacoes.secoes todas` → `python ferramentas/analise-1-mesarios-e-17h.py` → `python ferramentas/analise-2-series-e-contas.py` → `python ferramentas/graficos.py` → `python ferramentas/dados-locais.py`.
