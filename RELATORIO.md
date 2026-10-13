# Alegações de fraude no 1º turno de 2026: o relatório

**13/out/2026.** Dados: os **499.161 logs de urna** do 1º turno de 4/out/2026 (53,4 GB, todos baixados), os boletins de urna de **2014, 2018, 2020, 2022, 2024 e 2026**, o arquivo oficial de locais de votação de 2026 e os registros de chegada dos boletins do projeto `apuracao-eleicoes-2026`. Critérios gravados antes de olhar os dados (`docs/PRE_REGISTRO.md`, commit `3312d5c`), com 11 emendas registradas (§9 de lá), quatro delas feitas **depois** de ver resultado e marcadas assim.

**Quem fez.** O plano e a análise foram feitos por uma IA (Claude) sob a direção do autor do repositório, que aprovou o plano antes da execução. A revisão adversarial está em `docs/REVISAO_ADVERSARIAL.md`. Nenhum identificador de mesário, título, CPF ou nome que aparece nos logs foi publicado.

> **A régua.** Cada alegação recebe um veredito: **confirmado** (prova direta) · **indício forte** · **compatível com os dois** · **não sustentado** (a alegação previa um padrão e o dado mostra outro) · **desmentido** (o fato alegado é falso ou foi tirado de contexto). E termina com o **teto do pior caso**, o que fecharia a questão e quem tem o documento.

---

## 0. O placar

| # | Alegação | Veredito | Em uma linha |
|---|---|---|---|
| A1 | Mesários votam no lugar de quem faltou, no fim do dia, sobretudo no Nordeste | **Não sustentado como esquema que mova a eleição** · casos isolados **confirmados** · a régua pré-registrada ficou ambígua (§1.6) | 88% das liberações depois das 17h foram pela digital do próprio eleitor; a liberação à mão **não sobe** no fim do dia; o voto diferente das seções que votam tarde vem de **quem vota tarde**, liberado pela digital |
| A1 · H1b | O depoimento do Ceará: eleitor comprado vota de novo, liberado pela digital de um mesário pago | **Não sustentado** | no Ceará, mais liberação à mão no fim do dia **não** aumenta o voto em Lula nem em Elmano e **reduz** o comparecimento; nenhuma ocorrência de voto no lugar de outro no balanço policial do estado |
| A2 | Votos depois das 17h são o rastro da fraude | **Não sustentado** | 3,72 milhões votaram depois das 17h (em 2022, 4,05 milhões); a fila explica; o voto tardio dura o mesmo que o da manhã (57 s contra 55 s) |
| A3 | A abstenção serve de reserva | **Não sustentado** | o Nordeste comparece mais que a média desde 2018; as seções com 95% de comparecimento têm **menos** liberação à mão; cadastro fraudado existe e foi pego **pela digital** (Cabedelo) |
| A4 | Votou e aparece como faltoso | **Desmentido** (a leitura de fraude) | o sintoma é o oposto do que a fraude produziria; era atraso de processamento, com prazo até 11/out |
| A5 | A pausa só para presidente ajustou o resultado | **Não sustentado** (a manipulação) · **uma pergunta sem resposta** | a volta da tela bate com os boletins; mas o TSE diz que os boletins continuaram sendo recebidos, e o registro público tem **27,5 min sem nenhum** |
| A6 | "A conta não fecha" | **Desmentido** | a comparação junta **todos** os candidatos do PL com **só os eleitos** do PT, e cada eleitor votou em **dois** senadores |
| A7 | A curva é "lisa demais" | **Desmentido** | a curva real é **mais irregular** que a de ordens sorteadas, não mais lisa |
| A8 | Seções com 100% para um lado no Nordeste | **Não sustentado** | existem desde 2018, para os dois lados, e **caíram** em 2026 (de 1.236 para 822 com 95% ou mais para o PT) |
| A12 | Mudança de local de votação | **Confirmado** (a mudança) | 6.589 seções (1,3%) mudaram de local, com 1,93 milhão de eleitores, em todos os estados; o aviso a cada eleitor o dado não mostra |
| A15 | Os fiscais do PL contiveram a fraude e por isso Flávio ficou na frente | **Não sustentado** | a liberação sem digital caiu de 2022 para **2024** (antes dos fiscais de 2026) e **subiu** de 2024 para 2026 no Nordeste |
| A9 a A14 | Voto impresso, código, instituições, estrangeiros, IA | análise de desenho e de fontes (§9) | o sistema não é independente do software; isso não é prova de fraude, e é por isso que certos tipos de fraude só seriam vistos por amostra |

**O teto do pior caso.** Se **todas** as 441.896 liberações à mão feitas depois das 17h no país fossem fraude, e **todas** para um lado só, elas moveriam **20% da diferença** entre Flávio e Lula (2.239.115 votos) e **6% do que Flávio precisaria para chegar a 50%** (7.052.299 votos). Nas seções que o teste marcou como fora do padrão, são **2.871** votos.

---

## 1. A1 · Mesários votando no lugar de quem faltou

### 1.1 O que se alega (na versão mais forte)

Em parte das seções, sobretudo no Nordeste e no interior, mesários usam o fim do dia e a **liberação à mão** (o ano de nascimento, quando a digital falha ou não existe) para votar no lugar de quem faltou. A versão do depoimento do Ceará: eleitores comprados votam de novo em outras seções, **liberados pela digital de um mesário pago**.

### 1.2 O que a regra permite (e o que fica registrado)

Pela Res. TSE 23.759/2026 (arts. 19 a 21), a digital pode ser tentada até 4 vezes; se falhar, o presidente da mesa digita o ano de nascimento, com no máximo duas tentativas; o eleitor **assina o caderno**, é **liberado pela digital do mesário** e o fato vai para a **ata**. Quem não tem digital cadastrada é liberado só pelo ano de nascimento. **Cada liberação à mão deixa três rastros: o log (público), a assinatura e a ata (no cartório).**

### 1.3 O que o log mostra, no país inteiro

| | Brasil | Nordeste | Ceará |
|---|---|---|---|
| Votos no log | 124.741.807 | 35.449.045 | 5.902.053 |
| Liberados à mão (com digital de mesário + sem digital cadastrada) | 8.319.492 + 6.930.864 | 2.455.058 + 1.600.351 | 405.520 + 237.378 |
| % liberados à mão **antes** das 17h | 12,2% | 11,5% | 10,9% |
| % liberados à mão **depois** das 17h | 11,9% | 11,2% | 10,2% |
| Votos depois das 17h | 3.721.598 | 2.280.432 | 363.213 |

**A liberação à mão não sobe no fim do dia em nenhuma região** (razão depois/antes de 1,0; no Sudeste, 1,2, puxada por eleitores sem digital cadastrada em Minas). Em média, a taxa de liberação à mão depois das 17h é **1,4 ponto menor** que antes, na mesma seção.

### 1.4 As seções fora do padrão (T1.3)

A marca pré-registrada (S5: cinco ou mais liberações à mão seguidas depois das 17h, mais rápidas que as 10% mais rápidas da manhã) pegou **122 seções** no país (59 no Nordeste, 50 no Sudeste, 6 no Ceará). Comparadas com as outras seções **da mesma escola**:

| Escopo | Seções marcadas | Voto em Lula contra as vizinhas | p (placebo, 10.000 sorteios) | Comparecimento contra as vizinhas |
|---|---|---|---|---|
| Brasil | 111 | +0,86 ponto | 0,021 | **−1,05 ponto** |
| Nordeste | 56 | −0,14 ponto | 0,58 | −1,16 ponto |
| Sudeste | 42 | +1,61 ponto | 0,004 | −0,81 ponto |
| Ceará | 6 | −0,58 ponto | 0,61 | −0,54 ponto |

**O comparecimento das marcadas é menor que o das vizinhas.** Voto no lugar de ausente teria de fazê-lo **maior**.

**Onde elas estão:** 37 no Espírito Santo e 36 em Pernambuco, e 21 numa cidade só, **Jaboatão dos Guararapes (PE)**, mais 12 em Serra e 10 em Cariacica (ES). Nessas cidades, a liberação à mão **já é a regra o dia inteiro**: 36% dos votos antes das 17h em Jaboatão, 52% em Serra, 54% em Cariacica (no país, 12%). Onde isso é normal, cinco liberações à mão seguidas à noite são esperadas, e o critério S5 as marca. **Esse é um limite do critério**, que não descontava a taxa local. Comparadas com as outras seções das mesmas escolas, as marcadas de Jaboatão votaram igual (Lula 53,8% contra 53,6%); as de Serra e Cariacica deram 1,5 e 2,5 pontos a mais para Lula (45,2% contra 43,7%; 43,7% contra 41,2%), em 12 e 10 seções, com comparecimento um pouco **menor** que o das vizinhas. A lista completa, com o nome de cada escola, está em `resultados/a1_secoes_marcadas.csv`.

### 1.5 Dose e resposta (T1.9) e o teste que desempata

Pré-registrado: dentro da mesma escola, a fração de votos liberados à mão **depois das 17h**, controlando pela fração liberada à mão **antes**. Resultado: associação com **mais voto em Lula** em **todas** as regiões, inclusive o Sul e o Centro-Oeste, onde ninguém alega fraude (Brasil +4,0 pontos por 10 pontos de liberação manual tardia; Nordeste +4,2; Ceará +5,3, e +5,4 para Elmano). O placebo de 12h às 13h não mostra o mesmo efeito.

**Mas a alegação não é a única explicação:** a fila do fim do dia tem um perfil próprio. O teste que separa as duas (exploratório, emenda E10, feito depois de ver o resultado) põe no mesmo modelo os votos tardios **liberados pela digital**, que são de pessoas presentes:

| Escopo | Liberados à mão depois das 17h | Liberados **pela digital** depois das 17h |
|---|---|---|
| Brasil | +0,50 ponto (p = 0,12) | **+1,33 ponto (p < 0,0001)** |
| Nordeste | +0,32 ponto (p = 0,29) | **+1,42 ponto (p < 0,0001)** |
| Ceará | −0,69 ponto (p = 0,22) | **+1,64 ponto (p < 0,0001)** |
| Sul | 0,00 ponto (p = 0,99) | **+1,21 ponto (p < 0,0001)** |

*(efeito no voto em Lula por 10 pontos de fração; `resultados/x_exploratoria.csv`)*

**Quem carrega a associação é o voto tardio pela digital, de gente presente.** Quem vota depois das 17h vota um pouco diferente de quem votou de manhã, e isso não depende de a liberação ter sido à mão. E o **excesso** de liberação à mão no fim do dia (manual depois menos manual antes) não se associa a mais voto em Lula em nenhuma região; no Ceará, a associação é negativa (p = 0,0001).

### 1.5b A porta mais fraca, separada (exploratório, emenda E12)

A liberação de quem **não tem digital cadastrada** (só o ano de nascimento, sem digital de ninguém) **sobe** depois das 17h em todas as regiões, enquanto a liberação com a digital do mesário **cai**; por isso o total fica estável.

| % dos votos | Sem digital, antes das 17h | Sem digital, depois | Com digital de mesário, antes | Com digital de mesário, depois |
|---|---|---|---|---|
| Brasil | 5,5% | 6,7% | 6,7% | 5,2% |
| Nordeste | 4,4% | 6,0% | 7,0% | 5,2% |
| Ceará | 4,0% | 5,2% | 7,0% | 5,0% |
| Sudeste | 7,3% | 10,9% | 6,4% | 5,6% |
| Sul | 4,5% | 5,2% | 7,8% | 6,7% |

Dentro da mesma escola, mais liberação tardia sem digital **não** vem com mais voto em Lula: no Nordeste, −1,1 ponto por 10 pontos (p = 0,006); no Ceará, −3,5 para Lula e **+1,8 para Flávio** (p = 0,003); e vem com **comparecimento menor** no Nordeste e no Ceará. Voto no lugar de ausente, para qualquer lado, aumentaria o comparecimento. **Leitura:** a alta no fim do dia combina com o perfil de quem chega tarde sem digital cadastrada; é **a primeira coisa a conferir no caderno**, porque é a porta que não exige digital de ninguém.

### 1.6 O veredito pela régua escrita antes, e a leitura

- **Pela régua pré-registrada**, o Brasil, o Nordeste e o Ceará caem ao mesmo tempo em "compatível com os dois" (a dose-resposta passou) e em "não sustentado" (88% das liberações depois das 17h foram por digital e o teto das marcadas é 0,1% da diferença). O Sudeste cai ao mesmo tempo em "indício forte" e no mesmo "não sustentado". **A régua tinha essa sobreposição; ela está registrada (emenda E11), não foi reescrita.**
- **Leitura da IA:** os dados **não sustentam** um esquema de mesários votando no lugar de ausentes que mova o resultado, em nenhuma região. Três previsões da alegação falham ao mesmo tempo: a liberação à mão não sobe no fim do dia, o comparecimento não sobe onde ela é maior, e o voto diferente das seções que votam tarde aparece igual nos votos liberados pela digital. O "indício" do Sudeste vem de 42 seções, 826 votos manuais depois das 17h, e repete o padrão das outras regiões.
- **O que existe, e está confirmado:** casos isolados. Em **Salvador, 4/out/2026**, uma mesária foi presa por votar no lugar de um policial militar (§1.7). Em **Pescaria Brava/SC, 2016**, a Polícia Civil concluiu que um mesário registrou deliberadamente o voto de uma eleitora morta numa eleição decidida por um voto. Em **2022, em Lisboa**, um eleitor votou no lugar de outro. **O mecanismo é possível, e quando acontece fica rastro.**

### 1.7 O caso de Salvador no log

A escola do caso (Escola Estadual José Calazans Brandão da Silva, zona 13, local 1422) tem as seções 315 a 321. Na seção 315, às 09:29:38, um eleitor foi liberado **pela própria digital**, o voto foi computado 22 segundos depois, e em seguida a urna recusou **quatro vezes em dois minutos** liberar um eleitor que *"já votou"*. A sequência é **compatível** com o relato (o policial passou pela biometria e outra pessoa votou); a reportagem não diz a seção, então não dá para afirmar que é ele. **O que isso ensina:** nesse caminho a fraude **não aparece como liberação à mão**, e o rastro é o aviso de "já votou" quando a vítima volta.

**No país:** 75.368 episódios de *"o eleitor identificado já votou"* (0,60 por mil votos), mais nas seções que Lula venceu (0,69) do que nas que Flávio venceu (0,54), **em todas as regiões, inclusive o Sul**. Explicações inocentes (mesário digitando um título errado, eleitor voltando por engano) e a fraude de Salvador produzem o mesmo aviso. **Teto:** 75 mil votos, 3% da diferença. **Compatível com os dois**; o que separa é a ata.

### 1.8 O que fecharia, e quem tem

O **caderno de votação** das 122 seções marcadas (cada liberação à mão tem uma assinatura) e a **ata** (ocorrências de "já votou"). Ficam nos cartórios dos TREs. O pedido está pronto (`docs/PEDIDOS_LAI.md`, P2 e P3), com a lista das seções em `resultados/a1_secoes_marcadas.csv`.

---

## 2. A2 · Votos depois das 17h

- **3.721.598 votos depois das 17h** em 2026 (2,98% dos votos); em 2022 foram **4.047.341** (dado do TSE). Seções com último voto depois das 19h: 7.406; depois das 21h: 179 (132 no Nordeste, 69 na Bahia).
- **88% deles foram liberados pela digital** do próprio eleitor.
- **Quanto tempo cada voto levou:** mediana de 57 s depois das 17h, contra 55 s antes. A alegação de 2022 (*"de 1min40 para 32 a 35 segundos depois das 17h"*) não aparece.
- **O que explica o voto tardio** (T2.3): tamanho da seção, comparecimento e ritmo da manhã explicam de 11% a 64% da variação por estado; o que sobra aparece tanto nas seções **menores** quanto nas **maiores**, em todos os estados, e não concentrado nas pequenas como a alegação previa.
- **Validação externa:** em Manaus, o leitor deste projeto reproduz os números publicados pelo projeto independente quehorasvotar (4.013 seções, último voto às 20h11, 568 seções com mais de 1 h de fila, 34 com mais de 2 h).

**Veredito: não sustentado.** **A pergunta do espectador** (*"há registro oficial de que essas seções ficaram abertas?"*): a hora de encerramento de cada urna é pública; o motivo (quantas senhas foram distribuídas às 17h) está na ata, que não é pública. 🆕 Em 2026, os dois últimos eleitores da fila acompanham o encerramento e recebem cópia do boletim.

## 3. A3 · Abstenção como reserva, mortos e identidades falsas

- **Comparecimento por município (mediana):** Nordeste 77,6% (2014), 80,9% (2018), 79,5% (2022), 81,0% (2026); Brasil 79,6%, 79,5%, 79,0%, 79,4%. O Nordeste comparece mais que a média **desde 2018**, não só em 2026.
- **Municípios fora da própria história em 2026** (variação acima de 3 desvios-padrão do estado): 26 no país, **5 no Nordeste**, 13 no Sudeste.
- **Seções com comparecimento de 95% ou mais:** 932 (2018), 254 (2022), 599 (2026). Em 2026, elas têm **8,7%** de liberação à mão, contra **12,2%** nas demais: o contrário do que a "reserva" exigiria.
- **Cadastro fraudado existe:** a Operação Heterônimo (PF, Cabedelo, 23/set/2026) achou 11 identidades da mesma pessoa **pelo cruzamento de digitais**, antes da eleição.
- **Abstenção de 2026:** 33.453.535 eleitores (21,1%).

**Veredito: não sustentado.** **O que fecharia:** o número de inscrições duplicadas achadas pelo cruzamento de digitais e de mortos com voto registrado, que só o TSE pode cruzar.

## 4. A4 · Votou e aparece como faltoso

O serviço do TSE mostrou "FALTOU" em 6/out, trocado por "em processamento", com processamento até 11/out (a tela que circulou no TikTok mostra a mensagem de suspensão). **Se mesários votassem por ausentes, o sintoma seria o oposto:** quem faltou apareceria como presente. E o comparecimento diz **quem** votou; o boletim conta **os votos**, sem nome. **Veredito: desmentido** (a leitura de fraude). **O teste inverso** (`docs/CONVITE_PUBLICO.md`): se todas as 441.896 liberações à mão depois das 17h fossem voto de ausente, **1 em cada 76** eleitores que se abstiveram apareceria como "votou"; se fossem só as das seções marcadas, 1 em cada 11.650.

## 5. A5 · A pausa só para presidente

Medido no projeto da apuração: a tela parou de 19h06 a 20h08 e voltou mostrando exatamente o que os boletins já recebidos somavam. A nota do TSE (6/out) diz que, durante a pausa, os boletins *"continuaram a ser transmitidos, recebidos, processados e publicados"*; o registro público de recebimento tem **27,5 minutos sem nenhum boletim** (19:31:50 a 19:59:22) e 20.171 nos seis minutos seguintes. **Veredito: não sustentado** (a manipulação: os números da volta batem) e **uma pergunta sem resposta**, com destinatário (`docs/PEDIDOS_LAI.md`, P1).

## 6. A6 · "A conta não fecha"

| 1º turno de 2026 | Votos |
|---|---|
| Senadores **eleitos** do PT (6) | 15.991.205 |
| **Todos** os candidatos do PT ao Senado | 27.306.998 |
| Lula | 53.879.538 |
| Senadores **eleitos** do PL (19) | 45.247.104 |
| **Todos** os candidatos do PL ao Senado | 58.307.861 |
| Flávio | 56.104.503 |
| Votos válidos de Senado por eleitor que compareceu | 1,66 |

Os "58,2 milhões" que circularam são a soma de **todos** os candidatos do PL; os "15,9 milhões", só dos **eleitos** do PT. E cada eleitor teve **dois** votos para o Senado. Em 2018, que também teve duas vagas, os senadores eleitos do PSL somaram 14,5 milhões e Bolsonaro teve 49,3 milhões. **Veredito: desmentido.** *(Números do Senado sem o exterior, que não vota para senador; os de presidente com o exterior. Fonte: `resultados/a6_a_conta.csv`.)*

## 7. A7 · A curva "lisa demais"

A mudança da vantagem de Flávio a cada 2,5% das seções, na ordem real de chegada, tem desvio-padrão de **0,32 ponto**; em 1.000 ordens sorteadas, entre 0,02 e 0,08. **A curva real é mais irregular que o acaso**, porque os estados chegam em blocos (Sul e Centro-Oeste primeiro, Nordeste por último, como mostrou o projeto da apuração). **Veredito: desmentido.**

## 8. A8 e A15 · Seções extremas e os fiscais

- **Seções com 95% ou mais dos válidos para um lado** (válidos ≥ 50): para o PT, 1.007 (2018), 1.236 (2022), **822 (2026)**; para a direita, 1, 10 e 19. A maioria no Nordeste desde antes de 2026, e **caíram**.
- **A série do contador oficial** de eleitores com digital liberados sem ela: Nordeste 9,7% (2018), 9,7% (2022), **6,6% (2024)**, 6,9% (2026); a mesma queda de 2022 para 2024 aparece no Sul (de 10,4% para 7,3%). **A queda aconteceu numa eleição municipal, antes de qualquer campanha de fiscais de 2026**, e de 2024 para 2026 o contador **subiu** no Nordeste. Em 2020 a biometria foi suspensa (pandemia), e a comparação com 2020 foi trocada (emenda E9).
- **Dentro da mesma escola, de 2022 para 2026:** onde a liberação sem digital mais caiu, o voto em Lula caiu **menos** (o oposto do que a hipótese dos fiscais prevê), em todas as regiões.

**Veredito de A15: não sustentado.** O 2022 também teve chamada de fiscais (Nexo; Mais Goiás).

## 9. A9 a A14 · Desenho do sistema, fontes e o espelho

- **Voto impresso (A9):** a urna brasileira registra o voto só em forma eletrônica; o mesmo programa mostra, grava e imprime. **Isso não é prova de fraude**, e é por isso que certos tipos de fraude no software só seriam vistos pela amostra do teste de integridade (sem divergência em 2026). Histórico: voto impresso de 2009 e de 2015 derrubados pelo STF (ADI 4543 em 2013, ADI 5889 em 2020); PEC rejeitada na Câmara em 2021 (229 a 218, precisava de 308). Alemanha (2009), Índia (papel conferido e contagem obrigatória em 5 seções por distrito) e Namíbia (2020) exigem registro conferível; Estados Unidos fazem auditoria estatística sobre o papel. **O Brasil está à frente** na publicação de dados por seção e **atrás** na verificação independente do software.
- **Código e segurança (A10):** falhas reais em testes públicos (2012, 2017) e invasão da rede do TSE em 2018, sem prova de alteração de resultado.
- **O espelho (A11):** todo teste deste relatório rodou para os dois candidatos. Os desvios encontrados (o voto das seções que votam tarde, o aviso de "já votou") vão para o mesmo lado **em todas as regiões, inclusive onde ninguém alega fraude**, o que aponta para o perfil de quem vota, e não para um lado da mesa. As alegações de fraude **a favor de Flávio** (30 comentários) não têm teste próprio além desse espelho, e o espelho também não as sustenta.
- **A IA (A13):** os critérios foram escritos antes; as conclusões principais não dependem de comparar com 2022 (usam a mesma escola, no mesmo dia); os scripts rodam sem IA; e o leitor reproduz, seção a seção, um contador oficial que nunca leu.
- **Estrangeiros (A14):** nenhum incidente registrado encontrado; fica para a resposta do TSE (P7).

## 10. O que este projeto não consegue ver

- **Quem estava diante da urna.** O log mostra como a pessoa foi liberada, não quem era. Isso está no caderno e na ata.
- **Voto a voto depois das 17h.** O registro digital do voto embaralha a ordem para proteger o sigilo; a análise é por seção.
- **O software.** O projeto parte do log e do boletim que a urna gerou.
- **Urnas de contingência.** Em 2.834 seções o log cobre só a urna substituta; elas ficam fora dos testes de horário.

## 11. Como conferir

Critérios e emendas em `docs/PRE_REGISTRO.md`; validação do leitor em `docs/VALIDACAO_DO_LEITOR.md`; fontes em `docs/VERIFICACAO_DE_FONTES.md`; dados e como apagar em `docs/DADOS_LOCAIS.md`. A ordem dos comandos está no `ESTADO.md`.
