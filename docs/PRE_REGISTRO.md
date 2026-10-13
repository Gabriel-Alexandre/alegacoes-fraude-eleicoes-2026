# Pré-registro: os critérios, escritos antes de olhar os dados

**Gravado em commit em 13/out/2026, antes de qualquer análise.** A coleta dos logs começou no mesmo dia, um pouco antes deste commit; até ele, nenhum dado foi lido além do teste de integridade da coleta (contagem de arquivos e bytes) e do log de **uma** seção da PB usado para conhecer o formato (plano §3.1). Toda mudança daqui em diante entra na **§9**, dizendo se foi feita **antes** ou **depois** de ver resultado.

> Os números de cada critério vieram do plano aprovado (`docs/PLANO.md` §6). Onde o plano dizia "proposta", este arquivo fixa o valor.

---

## 0. Regras gerais

1. **Unidade:** a seção eleitoral. Seção agregada conta pela urna (a seção principal); as agregadas são marcadas e entram nos totais.
2. **Exterior (ZZ) fica fora** dos testes de seção e de região (fuso, mesário e local de votação não são comparáveis); entra só nos totais nacionais.
3. **Hora de Brasília:** a votação abre às 8h de Brasília no país inteiro. Para cada município, o deslocamento é `8 − mediana da hora de abertura das suas urnas`, arredondado para a hora inteira. Toda hora do log e do boletim é convertida assim. Município com deslocamento que não seja 0, 1, 2 ou −1 é listado e excluído dos testes de hora.
4. **Espelho:** todo teste que procura desvio a favor de um candidato roda **igual** para Lula (13) e para Flávio (22), e, no Ceará, para Elmano e para o segundo colocado ao governo.
5. **Linguagem:** nenhum resultado é "fraude" nem "prova de que não houve fraude". Seção marcada é **"fora do padrão, a conferir no caderno"**. Os vereditos são os da §8.
6. **Privacidade:** o identificador de mesário vira código por HMAC-SHA256 com chave local (fora do git) no momento da leitura. Nenhum identificador real, número de título, CPF ou nome que aparecer em log entra em arquivo derivado, relatório ou gráfico.
7. **Teto do pior caso** em toda alegação testada com dado: o máximo de votos que a alegação poderia ter movido, contra (a) a diferença Flávio − Lula no 1º turno e (b) os votos que Flávio precisaria tirar do adversário para chegar a 50% dos válidos, `V × (1 − 2 × f)`, com V e f oficiais.

## 1. O leitor do log (definições)

O log de cada urna é lido do arquivo `logd.dat` dentro do `log.jez`. Só entram eventos do dia **04/10/2026** do aplicativo de votação (`VOTA`).

**Eleitor (bloco):** a sequência de eventos entre um `O voto do eleitor foi computado` e o seguinte. O instante do voto é a hora do `O voto do eleitor foi computado`.

**Tipo de liberação de cada eleitor:**

| Tipo | Regra |
|---|---|
| `biometrica` | o bloco tem `Tipo de habilitação do eleitor [biométrica]` |
| `manual` | não tem o evento acima e tem `Dado digitado confere` ou `Mesário <id> habilitou o eleitor` |
| `outra` | nenhum dos dois. ⚠️ Se o log tiver outro texto de tipo de habilitação (descoberto no vocabulário, §1.1), ele é classificado aqui e a emenda registra o texto |

**Também por eleitor:** número de `Dado digitado não confere` no bloco; o código do mesário que liberou (manual); se houve `Solicita digital` sem sucesso antes da manual (falha de digital) ou não (sem digital cadastrada); eventos de suspensão e inatividade (`Eleitor sem atividade`, `suspenso`).

**Voto sem habilitação (T1.8):** `O voto do eleitor foi computado` cujo bloco não tem `Eleitor foi habilitado`.

### 1.1 O vocabulário, antes do leitor

Antes de rodar o leitor no país, lê-se o vocabulário de mensagens (texto do evento com os números trocados por `N`) numa amostra de 1.000 logs sorteados (semente 20261013), estratificada por UF. **Isso olha a forma do log, não o resultado:** a saída é a lista de textos e a contagem de cada um, sem ligar a voto nem a seção.

### 1.2 Validação do leitor (antes dos testes)

- **Reconciliação:** para cada seção, `votos computados no log` = `comparecimento do boletim` (urna substituída: soma dos logs). Seção que não bate é listada; se forem mais de 1% das seções, o leitor volta para correção antes de qualquer teste.
- **Leitura à mão:** 30 seções sorteadas (semente 20261013), conferidas linha a linha contra o leitor, nos campos de tipo de liberação e hora.
- **Duas implementações:** os números que vão ao relatório são refeitos por um segundo leitor escrito do zero (`ferramentas/validacao-independente.py`).

## 2. Métricas por seção (2026, do log)

`n_votos` · `n_bio` · `n_manual` · `n_outra` · `n_manual_antes17` · `n_manual_apos17` · `n_votos_apos17` · `n_nao_confere` · `n_nao_confere_apos17` · `maior_sequencia_manual_apos17` (manuais consecutivas, com hora ≥ 17:00:00) · `mediana_intervalo_sequencia` (segundos entre votos dentro dessa sequência) · `p10_intervalo_manha` (percentil 10 dos intervalos entre votos de 08h a 12h) · `mesarios_manual` (quantos códigos distintos liberaram manuais depois das 17h) · `ultimo_voto` · `n_sem_habilitacao` · `n_suspensao`.

Do boletim (CSV oficial e projeto da apuração): aptos, comparecimento, local de votação, votos por cargo e candidato, `QT_ELEITORES_BIOMETRIA_NH`, abertura, encerramento.

## 3. A1 e H1b · mesários e o voto no lugar de quem faltou

**Marca de seção (critério principal, `S5`):** `maior_sequencia_manual_apos17 ≥ 5` **e** `mediana_intervalo_sequencia` < `p10_intervalo_manha` da própria seção (votos mais rápidos que os 10% mais rápidos da manhã). **Sensibilidade:** `S3` e `S10` (sequência ≥ 3 e ≥ 10), e a versão absoluta (mediana < 60 s).

**Marca de chute (`C3`):** `n_nao_confere_apos17 ≥ 3`.

**Marca conjunta de H1b (`J`, T1.11):** `S5` **e** um só código de mesário em toda a sequência **e** comparecimento da seção ≥ mediana das outras seções do mesmo local + 5 pontos.

**T1.3 · desfecho das marcadas:** para cada seção marcada com pelo menos 2 outras seções no mesmo local de votação: `desvio = participação do candidato na seção − média das outras do local` (votos válidos de presidente), e o mesmo para comparecimento. Placebo: 10.000 sorteios em que, dentro de cada local que tem seção marcada, uma seção qualquer faz o papel da marcada. `p` = fração de sorteios com desvio médio ≥ o observado.

**T1.9 · dose e resposta (com a correção 13.4):** regressão, uma linha por seção, com efeito fixo de local de votação e erro agrupado por município:
`participação do candidato = β1 × (manuais depois das 17h / votos) + β2 × (manuais antes das 17h / votos) + efeito do local`.
A alegação prevê **β1 > 0** para o lado acusado, **acima** de β2. **Placebo:** a mesma regressão com a janela falsa 12h–13h no lugar de "depois das 17h".

**Critério de veredito de A1:**

| Veredito | Condição |
|---|---|
| **Indício forte** | T1.3 com `p < 0,01` para o mesmo lado em `S5` e em pelo menos uma das sensibilidades, **e** T1.9 com β1 > β2 e β1 > 0 a 1%, **e** o placebo 12h–13h sem o mesmo efeito |
| **Compatível com os dois** | só uma das condições acima |
| **Não sustentado** | nenhuma, **ou** as liberações depois das 17h são em maioria por digital em todas as regiões **e** o teto do pior caso das seções marcadas fica abaixo de 10% da diferença Flávio − Lula |

O veredito sai por região, para o Ceará e para o país.

## 4. A2 · votos depois das 17h

- **T2.1** 2026: quantos votos computados com hora ≥ 17:00:00 (log). 2018 e 2022: quantas seções encerraram depois das 17h, 18h, 19h e 20h (o CSV não tem hora de cada voto).
- **T2.2** proporção de liberação manual antes e depois das 17h, por região. **Previsão da alegação:** a proporção depois das 17h é pelo menos o dobro da de antes, numa região e não nas outras.
- **T2.3** modelo do voto tardio: `votos depois das 17h ~ aptos + comparecimento + p10_intervalo_manha + proporção manual antes das 17h`, por UF. A previsão da fila é que tamanho e lentidão expliquem; a da fraude é que sobre resíduo concentrado em seções pequenas.
- **T2.4** seções com voto depois das 19h e depois das 21h, listadas uma a uma por UF, com tipo de liberação.
- **T2.5** 2018: seções que encerraram depois das 18h30, com `QT_ELEITORES_BIOMETRIA_NH` contra as outras do mesmo município.

**Veredito de A2:** "não sustentado" se a liberação depois das 17h for majoritariamente por digital em todas as regiões e T2.3 explicar o voto tardio sem resíduo concentrado; "indício" se a manual dobrar depois das 17h numa região e o resíduo se concentrar.

## 5. A3, A8 e A15 · comparecimento, seções extremas e a série do contador

- **T3.1** comparecimento por município 2014, 2018, 2022 e 2026 (1º turno). Município "fora da própria história" = variação 2022→2026 acima de 3 desvios-padrão da variação dos municípios da mesma UF. Conta por região e com o espelho (a direção do voto nesses municípios).
- **T3.2** seções com comparecimento ≥ 95% (aptos ≥ 50), por ano e região, e a proporção de manuais delas em 2026.
- **T8.2** seções com ≥ 95% dos válidos de presidente para um candidato (válidos ≥ 50), 2018, 2022 e 2026, por região, **para os dois lados**.
- **T1.6/T15.1** `QT_ELEITORES_BIOMETRIA_NH / comparecimento` por seção, 2018, 2020, 2022, 2024 e 2026, por região e no Ceará. **Previsão de A15:** a queda de 2022 para 2026 é maior onde a acusação diz que havia fraude (Nordeste, Ceará) do que no resto, **descontada** a queda de 2020 para 2024 (que mede o efeito do cadastro sem disputa presidencial).
- **T15.2** dentro do mesmo local de votação: seções em que o contador mais caiu de 2022 para 2026 perderam mais voto de Lula que as vizinhas? (2022 e 2026 casados por município, zona e seção.)

## 6. A6 · "a conta não fecha"

Refazer, com o resultado oficial: soma dos votos dos senadores **eleitos** do PT e do PL, a soma de **todos** os candidatos ao Senado de cada partido, os votos de Lula e de Flávio, e quantos votos de Senado existem por eleitor (2026 e 2018: duas vagas; 2022: uma). O teste é de aritmética, sem limiar.

## 7. A5, A7 e os documentos

- **A5:** a nota do TSE de 06/out contra o registro de recebimento (projeto da apuração, P2). Sem novo limiar.
- **A7:** 1.000 ordens aleatórias de chegada dos boletins de 2026; a variação da margem entre atualizações sucessivas de 2,5% das seções na ordem real cabe na faixa de 95% das ordens aleatórias?
- **A4, A9 a A14:** documentais. Cada fato vai para `docs/VERIFICACAO_DE_FONTES.md` com duas fontes ou o motivo de não ter.

## 8. Os vereditos

**Confirmado** (prova direta: documento oficial, decisão, flagrante) · **Indício forte** · **Compatível com os dois** · **Não sustentado** · **Desmentido** (o fato alegado é falso ou foi tirado de contexto). Os critérios de cada alegação estão nas seções acima. Toda alegação termina com o teto do pior caso, o que fecharia e quem tem o documento.

## 9. Emendas

| # | Data | Antes ou depois de ver resultado | O que mudou e por quê |
|---|---|---|---|
| E1 | 13/out | **antes** (vocabulário de 300 logs de AC, AL, AM e RR; só a forma) | a liberação manual se divide em **`manual_mes`** (a digital do eleitor falhou e um mesário liberou com a própria digital, Res. 23.759 art. 21) e **`manual_sem`** (eleitor sem digital cadastrada, só o ano de nascimento, art. 20). O vocabulário mostrou que, quando o mesário não se cadastrou no início do dia, o log grava *"Digital coletada bate com uma digital gravada após o registro inicial de mesário. Não é possível associar a habilitação a um mesário."*: a digital do mesário existe e o número não. Esses casos são `manual_mes` com código `nao_id`. Sem isso, iriam para `manual_sem` por engano. Nos testes, "manual" é a soma dos dois; `manual_mes` é o caminho de H1b (o depoimento) e `manual_sem` a porta mais fraca (sem digital de ninguém) |
| E2 | 13/out | **antes** | o T1.8 (caminho do caso de Salvador) usa os eventos que o vocabulário mostrou: *"Eleitor foi suspenso pelo mesário"* e *"Eleitor votou parcialmente e em seguida foi suspenso"*, com *"Atribuido voto nulo por suspensão"* nos cargos não votados |
| E3 | 13/out | **antes** (reconciliação de AC e RR: contagem, sem voto) | **urna de contingência:** quando a urna é trocada no meio do dia, o log publicado cobre só a substituta, e os votos de antes da troca ficam fora do log (estão no boletim). Em AC, 6 de 2.270 seções; em RR, 3 de 1.519. Essas seções são marcadas (`contingencia`, `cobertura_log = votos no log / comparecimento`). **Nos testes de hora entram só seções com cobertura de 100%**; a sensibilidade as inclui. A regra de reconciliação do §1.2 passa a ser: seção com contingência não conta como erro do leitor |
| E5 | 13/out | **antes** (texto da checagem da Justiça Eleitoral de 28/11/2022, recuperada no arquivo da internet) | entra a **duração do voto** (da liberação até o voto computado). A alegação de 2022 dizia que, depois das 17h, *"eleitores que levavam em média 1 minuto e 40 segundos para registrar o voto passaram a votar mais rápido, gastando entre 32 e 35 segundos"*. **T2.6:** mediana da duração antes e depois das 17h, por região e por tipo de liberação. A alegação prevê queda forte depois das 17h nas manuais; a fila prevê duração parecida |
| E6 | 13/out | **antes** (contagens de AM e AC, sem voto) | **o comparecimento de referência de 2026 é o do boletim digital** (`bu.dat`, decodificado pelo projeto da apuração), que bate com o log em 99,6% das seções do AM. O CSV oficial difere do boletim em 7,7% das seções do AM, com aptos e comparecimento menores pelo mesmo número (1 a 5 eleitores ou mais), o que indica eleitores em trânsito ou transferidos contados em outra seção no CSV. **Nas comparações entre anos** (2018 a 2026) usa-se o CSV nos dois lados, para manter a mesma régua |
| E7 | 13/out | **antes** dos testes nacionais (vem do estudo de caso das 7 seções da escola de Salvador do caso C1; nenhum número nacional visto) | **o caminho do "voto pendente" não aparece como liberação manual:** no caso de Salvador, o eleitor verdadeiro foi liberado pela própria digital e outra pessoa votou. O rastro é o evento *"O eleitor identificado já votou"* quando a vítima tenta votar. **Entra a métrica `n_ep_ja_votou`** (episódios: tentativas seguidas com menos de 10 min entre elas contam como um) e `n_ep_ja_votou_apos17`. **T1.12:** episódios "já votou" por 1.000 votos, por região, no CE, antes e depois das 17h, com o espelho (seções em que Lula ou Flávio venceram). Explicações inocentes do evento: o mesário digita um título errado que já votou, ou o eleitor volta por engano. A alegação prevê excesso concentrado; o inocente prevê taxa baixa e espalhada. ⚠️ **Os trechos de log exibidos** em relatório ou vídeo têm **todo** número de 12 dígitos tarjado (o log traz o número do mesário também em *"Biometria do mesário N encontrada"* e *"Biometria coletada não é do mesário N"*) |
| E8 | 13/out | **antes** dos testes (contagens de tipo no AM; sem voto) | o eleitor **sem digital cadastrada** (art. 20) é liberado com o texto *"Ano de nascimento digitado é igual ao do cadastro"*, e não *"Dado digitado confere"*. O leitor mandava esses casos para `outra` (no AM, 99.485 eleitores, 4,5%). **Correção:** esse texto vale como `manual_sem`; *"Ano de nascimento digitado é diferente do cadastro"* e *"Ano de nascimento inválido"* contam como tentativa errada (`nao_confere`). **Lição registrada em `docs/VALIDACAO_DO_LEITOR.md`:** os dois leitores tinham o mesmo ponto cego, então a concordância de 100% não o pegou; e a leitura à mão não sorteava eleitores da categoria `outra`. As duas validações passam a cobrir todas as categorias |
| E9 | 13/out | ⚠️ **depois** de ver a série do contador (`t15_serie`) | o comparador "queda de 2020 para 2024" do T15.1 **não funciona**: em 2020 a identificação biométrica foi suspensa (pandemia) e o contador é zero no país inteiro. **Troca:** a queda do Nordeste e do Ceará de 2022 para 2026 é comparada com (a) a das outras regiões no mesmo período, (b) a variação "normal" entre duas presidenciais (2018→2022) e (c) **a divisão da queda em 2022→2024 e 2024→2026**: se os fiscais de 2026 contiveram o esquema, a queda tem de estar em 2024→2026, depois das convocações de fiscais; se ela já estava toda em 2022→2024 (eleição municipal), não foi a campanha de 2026. Registrado como feito depois de ver a série, porque foi |
| E10 | 13/out | ⚠️ **depois** de ver o T1.9 nacional | **análises exploratórias** (`ferramentas/analise-3-exploratoria.py`), que **não mudam** o veredito pela régua: X1 e X2 repetem o T1.9 com os votos **por digital** depois das 17h (pessoa presente) no lugar ou ao lado dos manuais; X3 mede o **excesso** de liberação manual no fim do dia (manual depois das 17h menos manual antes); X4 testa o comparecimento. Motivo: o T1.9 deu associação em todas as regiões, inclusive onde não há alegação, e a explicação concorrente (quem vota tarde) precisava de um teste que a separasse da alegação. O relatório mostra os dois: o veredito pré-registrado e o que a análise exploratória acrescenta |
| E4 | 13/out | **antes** | a hora de abertura usada no fuso (§0.3) é a `abertura` do boletim de cada seção (projeto da apuração), não um evento do log |
