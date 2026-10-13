# Validação do leitor do log

Pré-registro §1.2. Cada validação diz o que foi comparado, com o quê, e o resultado.

## V1 · Reconciliação log × boletim (contagem de votos por seção)

| UF | Seções | Batem exatamente | Não batem | Causa das que não batem |
|---|---|---|---|---|
| AC | 2.270 | 2.264 | 6 | urna de contingência: o log publicado cobre só a urna substituta (emenda E3) |
| RR | 1.519 | 1.516 | 3 | idem |

*(As demais UFs entram aqui quando o leitor rodar no país.)*

## V2 · Comparação externa: o projeto quehorasvotar (Uapé), Manaus, 1º turno de 2026

O quehorasvotar publicou (marioadolfo.com, 10/out/2026) números de Manaus tirados dos mesmos logs. O leitor deste projeto, escrito sem ver o código deles, deu:

| Número | quehorasvotar | Este projeto | Situação |
|---|---|---|---|
| Seções de Manaus | 4.013 | 4.013 | ✅ igual |
| Último voto | 20h11 (hora local) | 20h11 | ✅ igual |
| Seções que votaram mais de 1 h depois das 16h locais | 568 | 568 | ✅ igual |
| Seções que votaram mais de 2 h depois | 34 | 34 | ✅ igual |
| Pessoas que votaram depois das 16h locais | 67.846 | 70.455 pela hora do voto computado; **68.402 pela hora da liberação** | ⚠️ diferença de 0,8% na definição mais próxima; a regra exata deles não foi publicada |

Hora local de Manaus = Brasília − 1 h, então 16h locais = 17h de Brasília.

## V3 · Segundo leitor, escrito do zero com outra lógica

`ferramentas/validacao-independente.py` parte de cada voto computado e volta até a habilitação, só com busca de texto (o leitor principal acompanha tentativas a partir do identificador digitado).

**1ª rodada (600 seções sorteadas de AC, AL, AM, AP e RR):** votos, manuais e votos depois das 17h iguais em 100% das seções; liberações por digital iguais em 99,0%, com 6 votos de diferença. **A causa era do segundo leitor:** às vezes a urna grava *"Tipo de habilitação do eleitor [biométrica]"* logo **depois** de *"Eleitor foi habilitado"*, e ele cortava o trecho na habilitação. Corrigido no segundo leitor; o principal já tratava isso.

**2ª rodada (2.000 seções sorteadas):** **100% iguais** nas quatro contagens (votos 512.785; digital 464.169; manuais 26.331; depois das 17h 28.824). A rodada final, com as 28 UFs, entra quando o leitor rodar no país.

## ⚠️ Lição: concordância entre dois leitores não basta (emenda E8)

Os dois leitores concordavam em 100%, e mesmo assim os dois erravam igual: o eleitor **sem digital cadastrada** é liberado com o texto *"Ano de nascimento digitado é igual ao do cadastro"*, que nenhum dos dois reconhecia, e esses eleitores caíam em `outra` (no AM, 99.485, 4,5% dos votos). A leitura à mão também não pegou, porque só sorteava eleitores das categorias que o leitor já conhecia. **O erro apareceu ao olhar a categoria `outra` de frente.** Correção nos dois leitores e na leitura à mão, que passa a sortear também `manual_sem` e `outra`. Depois da correção, `outra` = 0 no AM e em RR.

## V4 · Comparação com um contador oficial que o leitor nunca viu

O boletim de urna de 2026 traz `QT_ELEI_BIOM_SEM_HABILITACAO`: *"eleitores com biometria, mas que não foram habilitados por meio dela"*. Isso corresponde, no log, à liberação manual **com a digital do mesário** (`manual_mes`: a digital do eleitor existia e falhou). Quem não tem digital cadastrada (`manual_sem`) não entra nesse contador.

| UF | `manual_mes` no log | contador oficial | diferença |
|---|---|---|---|
| AM | 120.263 | 120.448 | −185 (0,15%) |

*(A comparação seção a seção, nas 28 UFs, entra na rodada final.)*

**V4, ensaio com 13 UFs (AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, RR):** nas **189.195 seções com log completo, o número de liberações manuais com digital de mesário é idêntico, seção a seção, ao contador oficial** (3.080.090 nos dois). O leitor reproduz exatamente um número que nunca leu.

## Rodada final (28 UFs, 13/out/2026)

| Validação | Resultado |
|---|---|
| V1 · reconciliação | 499.135 seções; 125.082.741 votos no log contra 125.264.250 no boletim (99,86%); **495.745 seções (99,58%) batem exatamente**; as demais têm urna de contingência (2.834 seções com o procedimento registrado no log; o TSE informou 1.861 urnas trocadas no dia, e a diferença é de definição: o log registra o procedimento de contingência, inclusive quando não houve troca completa) |
| V3 · segundo leitor | **100% iguais em 3.000 seções sorteadas** nas quatro contagens |
| V4 · contador oficial | **495.745 de 495.745 seções idênticas** (8.294.279 liberações manuais com digital de mesário, nos dois) |
| Leitura à mão | 30 seções, **101 eleitores** (42 por digital, 30 manuais com mesário, 29 sem digital cadastrada), **0 divergências** |
