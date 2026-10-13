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
| | | | |
