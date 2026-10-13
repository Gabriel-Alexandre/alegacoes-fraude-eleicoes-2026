# Dados locais: o que ocupa disco e o que pode ser apagado

Gerado por `ferramentas/dados-locais.py` em 2026-10-13T17:06:10+00:00. Pedido do autor (13/out/2026): os dados serão apagados depois do vídeo, e tudo tem de ficar reutilizável.

## O que precisa existir para reproduzir os resultados **sem** os brutos

- o código (`alegacoes/`, `ferramentas/`) e os critérios (`docs/PRE_REGISTRO.md`)
- `resultados/` inteiro, inclusive `resultados/dados/secoes_2026.parquet` (a tabela por seção, sem dado pessoal) e `resultados/MANIFESTO_DOS_DADOS.json` (o hash de cada banco de logs e de cada zip)
- os testes do `ferramentas/analise-1-*.py` que dependem só da tabela por seção rodam a partir do parquet; os que precisam da linha por voto (leitura à mão, segundo leitor) exigem baixar os logs de novo

## Pasta por pasta

| Pasta | O que tem | Tamanho | Pode apagar? | Como recriar |
|---|---|---|---|---|
| `dados/brutos/logs` | os 499.161 logs de urna de 2026, um banco SQLite por UF, com o `log.jez` original e o sha256 de cada um | 54,1 GB | **sim**, depois do vídeo | `python -m alegacoes.coleta_logs todas 75` (lê os endereços do projeto `apuracao-eleicoes-2026`); ~2 h |
| `dados/brutos/bweb` | CSV oficiais de boletim de urna de 2020, 2024 e 2026 (zip original, conferido pelo sha512 publicado) | 8,6 GB | sim | `python ferramentas/baixar-bweb.py`; ~15 min |
| `dados/brutos/eleitorado` | locais de votação de 2026 (nome, endereço, local original) | 0,2 GB | sim | baixar `eleitorado_local_votacao_2026.zip` do portal de dados abertos |
| `dados/derivados/logs` | uma linha por voto computado (tipo de liberação, hora, código do mesário por HMAC) e uma por urna | 1,2 GB | sim (sai dos brutos) | `python -m alegacoes.derivar_logs todas` |
| `dados/derivados/bweb` | os CSV oficiais de 2014 a 2026 em parquet | 0,1 GB | sim (sai dos brutos) | `python -m alegacoes.bweb 2014,2018,2020,2022,2024,2026 todas` |
| `dados/derivados/secoes` | a tabela por seção de 2026 (métricas do log + boletim) | 0,0 GB | sim: **uma cópia sem dado pessoal fica no git** (`resultados/dados/secoes_2026.parquet`) | `python -m alegacoes.secoes todas` |
| `dados/chave-local.txt` | a chave do HMAC que transforma o número do mesário em código | 0,0 GB | ⚠️ **se apagar, os códigos de mesário mudam** na próxima leitura (os resultados não, só os códigos) | nasce sozinha na primeira leitura |
| `dados/execucao` | saídas de terminal das execuções | 0,0 GB | sim | — |

**Total em `dados/`: 64,2 GB.**

## Para apagar (depois do vídeo)

```bash
rm -rf dados/brutos dados/derivados dados/execucao
```

Antes, confira que `resultados/dados/secoes_2026.parquet` e `resultados/MANIFESTO_DOS_DADOS.json` estão no git (`git status` limpo).

## Para conferir um download refeito

Rode a coleta de novo e depois este script: o `resumo_sha256` de cada UF em `dados/MANIFESTO.json` tem de bater com o de `resultados/MANIFESTO_DOS_DADOS.json`. Se o TSE tirar os arquivos do ar (como aconteceu com os de 2022), o manifesto continua provando o que foi lido.
