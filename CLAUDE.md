# CLAUDE.md: como operar neste repositório

Este arquivo é roteador. Se um fato aqui contradisser o arquivo dono, o dono ganha.

## Leia antes de qualquer coisa

| Ordem | Arquivo | Para quê |
|---|---|---|
| 1 | `ESTADO.md` | onde o trabalho parou |
| 2 | `docs/PLANO.md` | as alegações, o método, as fases e as melhorias (§13) |
| 3 | `docs/PRE_REGISTRO.md` | os critérios; nenhum teste roda antes de ele estar em commit |
| 4 | `docs/FONTES_DE_DADOS.md` e `docs/DADOS_LOCAIS.md` | de onde vem cada dado e o que ocupa disco |

## O que nunca fazer

- Escrever "fraude" ou "provou que não houve fraude" como conclusão. Vale a régua de vereditos do pré-registro §8.
- Testar um lado só: todo teste tem espelho (Lula e Flávio; no Ceará, Elmano e o segundo colocado).
- Publicar identificador de mesário, número de título, CPF ou nome que apareça em log. O mesário vira código por HMAC com a chave de `dados/chave-local.txt` (fora do git).
- Chamar de fraudulenta uma seção marcada por teste. Ela é "fora do padrão, a conferir no caderno".
- Mudar critério sem registrar na §9 do pré-registro, dizendo se foi antes ou depois de ver resultado.
- Dar número que não saiu de script, ou número de terceiro sem recálculo.
- Baixar em massa sem teto de requisições (o TSE responde 429; um coletor só, até ~75 req/s).
- Mudar a visibilidade do repositório: **público** por decisão do autor (13/out/2026), sem licença.

## Dados

Os brutos (~44 GB de logs) ficam em `dados/brutos/`, fora do git. Este projeto **lê** os brutos do projeto vizinho `../apuracao-eleicoes-2026` (os `aux.json` e os CSV históricos). O que precisa existir para reproduzir os resultados sem os brutos está em `docs/DADOS_LOCAIS.md`.
