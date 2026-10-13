# Como refazer tudo, do zero

Quem quiser conferir ou criticar este projeto consegue chegar aos mesmos números com os passos abaixo. Todo número do `RELATORIO.md` sai de um script rodado sobre arquivo público do TSE, e o `resultados/RESUMO.json` guarda cada um.

Há dois caminhos: **conferir os resultados sem baixar nada** (minutos) ou **refazer a coleta inteira** (horas, ~80 GB).

## Requisitos

- Python 3.10 ou mais novo (o projeto rodou em 3.11.9).
- `python -m pip install -r requirements.txt`
- Para refazer a coleta: ~80 GB livres (64 GB deste projeto, ~12 GB do projeto da apuração) e internet. A coleta dos logs leva ~2 h; a do projeto da apuração, de 1 a 3 h.

## Caminho 1 · conferir sem baixar nada

O git já traz a tabela por seção, sem dado pessoal (`resultados/dados/secoes_2026.parquet`), todos os CSV de resultado e o manifesto com o hash de cada arquivo lido (`resultados/MANIFESTO_DOS_DADOS.json`).

| O que conferir | Onde |
|---|---|
| os vereditos e o teto | `RELATORIO.md`, com cada número em `resultados/RESUMO.json` |
| os critérios, gravados antes | `docs/PRE_REGISTRO.md` (o histórico do git mostra o commit do pré-registro antes do dos resultados; as emendas estão na §9, cada uma dizendo se foi feita antes ou depois de ver o resultado) |
| a leitura do log contra o contador oficial | `docs/VALIDACAO_DO_LEITOR.md` (495.745 de 495.745 seções iguais) |
| as seções marcadas, com o nome da escola | `resultados/a1_secoes_marcadas.csv` |
| os gráficos | `resultados/figuras/` |

## Caminho 2 · refazer a coleta inteira

### 2.1 Primeiro, o projeto da apuração (dependência)

Este projeto lê os endereços dos logs e os boletins de 2026 que o projeto aberto [`apuracao-eleicoes-2026`](https://github.com/Gabriel-Alexandre/apuracao-eleicoes-2026) já baixou e guardou com hash. Ele precisa estar **na mesma pasta-mãe**, com este nome:

```
pasta-mae/
├── apuracao-eleicoes-2026/
└── alegacoes-fraude-eleicoes-2026/
```

```bash
git clone https://github.com/Gabriel-Alexandre/apuracao-eleicoes-2026
cd apuracao-eleicoes-2026
python -m pip install -r requirements.txt
python -m apuracao coletar                     # aux.json e bu.dat de cada seção de 2026 (retomável)
python -m apuracao oficial                     # resultado oficial, usado na validação de lá
python ferramentas/analise-1-validacao-e-curva.py   # deriva as tabelas por seção em dados/derivados/uf/ (e valida)
python ferramentas/baixar-historico.py          # CSV de boletim de 2014, 2018 e 2022, com o hash publicado
cd ..
```

O guia completo de lá está em `apuracao-eleicoes-2026/docs/REPLICAR.md`.

### 2.2 Depois, este projeto

| Passo | Comando | O que faz |
|---|---|---|
| 1 | `python -m alegacoes.coleta_logs todas 75` | baixa os 499.161 logs de urna (`log.jez`) para `dados/brutos/logs/`, com o sha256 de cada um. O `75` é o teto de requisições por segundo; o limitador baixa sozinho se o TSE responder 429. Retomável |
| 2 | `python ferramentas/baixar-bweb.py` | baixa os CSV de boletim de 2020, 2024 e 2026 e confere o hash publicado (2014 a 2022 vêm do projeto da apuração) |
| 3 | baixar [`eleitorado_local_votacao_2026.zip`](https://cdn.tse.jus.br/estatistica/sead/odsele/eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip) para `dados/brutos/eleitorado/` | os locais de votação de 2026 (portal de dados abertos do TSE, conjunto `eleitorado-2026`) |
| 4 | `python -m alegacoes.derivar_logs todas` | uma linha por voto: tipo de liberação, hora, e o mesário como **código** (HMAC com uma chave local que nasce sozinha em `dados/chave-local.txt`) |
| 5 | `python -m alegacoes.bweb 2014,2018,2020,2022,2024,2026 todas` | os boletins de cada ano em parquet |
| 6 | `python -m alegacoes.secoes todas` | a tabela por seção de 2026 (log + boletim) |
| 7 | `python ferramentas/analise-2-series-e-contas.py` | séries históricas, "a conta não fecha", a curva |
| 8 | `python ferramentas/analise-1-mesarios-e-17h.py` | os testes dos mesários e das 17h |
| 9 | `python ferramentas/analise-3-exploratoria.py` | os testes exploratórios (marcados como feitos depois de ver o resultado) |
| 10 | `python ferramentas/analise-4-locais.py` | escolas das seções marcadas e mudança de local |
| 11 | `python ferramentas/analise-5-sem-digital.py` | a liberação sem digital cadastrada, separada |
| 12 | `python ferramentas/graficos.py` | os gráficos em 1920×1080 |
| 13 | `python ferramentas/dados-locais.py` | o manifesto de hashes e o guia de disco |

**Validação:** `python ferramentas/validacao-independente.py 3000` (segundo leitor, escrito do zero, sobre 3.000 seções sorteadas) e `python ferramentas/leitura-manual.py` (amostra de linhas para ler à mão, em todas as categorias).

## Como saber se você leu os mesmos arquivos

O `resumo_sha256` de cada UF no seu `dados/MANIFESTO.json` tem de bater com o de `resultados/MANIFESTO_DOS_DADOS.json`. ⚠️ O TSE pode republicar ou tirar arquivos do ar (os logs por seção de 2022 e 2018 já respondem 404); se o resumo diferir, compare seção por seção antes de concluir qualquer coisa.

## O que não dá para refazer com dado público

O caderno de votação (as assinaturas), a ata de cada mesa, a lista de fiscais por seção e o registro interno do sistema de recebimento do TSE. Os pedidos para quem tem esses documentos estão em `docs/PEDIDOS_LAI.md`.

## Privacidade

O log traz o número do título ou do CPF digitado pelo mesário e o identificador de cada mesário. Nada disso sai deste projeto: o mesário vira código, e nenhum número de título, CPF ou nome é publicado. Quem refizer a coleta tem os mesmos arquivos na mão e a mesma responsabilidade.
