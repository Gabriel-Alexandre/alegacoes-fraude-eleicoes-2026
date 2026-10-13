# Fontes de dados

| Dado | Endereço | Ano | Para quê |
|---|---|---|---|
| Log de cada urna (`log.jez` → `logd.dat`) | `https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/dados/<uf>/<mun>/<zona>/<secao>/<hash>/o03220<uf><mun><zona><secao>-log.jez` | 2026 | liberação de cada eleitor (digital ou manual), hora de cada voto, mesário que liberou (vira código) |
| Índice de cada seção (`aux.json`) | baixado e guardado com hash pelo projeto `apuracao-eleicoes-2026` (`dados/brutos/<uf>.sqlite`) | 2026 | os hashes e nomes dos arquivos de cada seção |
| Boletim de urna em CSV (`bweb_1t_<UF>_*.zip`) | `https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/buweb/` e equivalentes de 2018, 2020, 2022, 2024 (portal de dados abertos, conjunto `resultados-<ano>-boletim-de-urna`) | 2018–2026 | votos por seção, local de votação, abertura, encerramento, `QT_ELEITORES_BIOMETRIA_NH` |
| Seções e votos de 2026 derivados | `../apuracao-eleicoes-2026/dados/derivados/uf/` | 2026 | comparecimento, local, votos por cargo |
| CSV de 2014, 2018 e 2022 | `../apuracao-eleicoes-2026/dados/brutos/historico/` | 2014–2022 | comparecimento e encerramento históricos |

**Definição oficial** (leia-me do TSE do boletim de urna): `QT_ELEITORES_BIOMETRIA_NH` é o *"quantitativo de eleitores com biometria, mas que não foram habilitados por meio dela"*.

**Não existe em dado público:** a ata da mesa, o caderno de votação (assinaturas), a lista de fiscais credenciados por seção, o registro interno do sistema de recebimento do TSE, e os logs por seção de 2022 e 2018 (respondem 404).
