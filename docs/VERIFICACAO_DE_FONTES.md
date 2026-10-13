# Verificação de fontes

Cada fato externo usado no plano, no relatório ou no vídeo, com a fonte primária, a segunda fonte e o estado. Pedido do autor (13/out/2026): *"validar todas essas referências"*. Regra: fato com uma fonte só fica marcado; número de terceiro só entra recalculado; resumo de página não é fonte (o texto foi lido).

**Estados:** ✅ conferido (duas fontes, ou a fonte primária lida) · 🔧 corrigido (a versão que circulava estava errada) · ⚠️ uma fonte só · ⬜ a conferir · ❌ não achado

## 1. Regras e documentos oficiais

| # | Fato | Fonte primária | Segunda fonte | Estado |
|---|---|---|---|---|
| F1 | Liberação manual (Res. TSE 23.759/2026): digital tentada até 4 vezes; sem sucesso, o presidente da mesa digita o ano de nascimento, no máximo 2 vezes; aceito, o eleitor **assina o caderno**, é **habilitado pela digital do mesário**, e o fato vai para a **ata** (art. 19 a 21). Quem não tem digital cadastrada: só o ano de nascimento (art. 20) | texto da resolução no portal do TSE, lido em 13/out | o log real de uma seção da PB mostra a sequência | ✅ |
| F2 | O ano de nascimento **não consta no caderno de votação**; a operação e quem liberou ficam no log | checagem da Justiça Eleitoral de 28/11/2022 (arquivo da internet, 24/11/2025) | outra checagem da JE com o mesmo título ("caderno de votação não tem ano de nascimento") | ✅ (2022; a regra de 2026 mudou: agora o mesário libera com a própria digital) |
| F3 | **4.047.341 pessoas votaram depois das 17h no 1º turno de 2022**; os últimos entre 23h45 e 23h59; 31.714 no 2º turno; tempo médio de voto 61,81 s | mesma checagem de 28/11/2022 (área técnica do TSE) | busca: checagem da JE sobre o 2º turno de 2022 diz que os "4 milhões" eram do 1º turno | ✅ (a recalcular para 2026 com o log) |
| F4 | Às 17h, senhas para quem está na fila, a partir do último; votação continua só para eles (Res. 23.751/2026, art. 160 segundo a imprensa) | TSE, "Conheça os procedimentos que garantem o encerramento seguro" (ago/2026) | Poder360, Bahia Notícias | ✅ (o número do artigo vem da imprensa) |
| F5 | 🆕 2026: os **dois últimos eleitores da fila** ficam para acompanhar o encerramento e recebem cópia do boletim | TSE (mesma matéria) | Diário do Nordeste | ✅ |
| F6 | Pausa da divulgação: ~19h14 (64,81%) a 20h04, só a visualização "Brasil" de presidente; boletins *"continuaram a ser transmitidos, recebidos, processados e publicados"* | nota do TSE, 06/out (íntegra no Poder360) | Agência Brasil, O Tempo | ✅ |
| F7 | Registro público de recebimento: 27,5 min sem nenhum boletim (19:31:50 a 19:59:22) | projeto `apuracao-eleicoes-2026`, `RELATORIO.md` (dado do TSE, com hash) | validação independente do mesmo projeto | ✅ |
| F8 | Urnas trocadas no 1º turno de 2026: **1.861 (0,34%)** no balanço final; 421, 1.121 e 1.543 eram parciais do dia; nenhuma votação manual | SBT News e NC News (balanço do TSE às 18h) | DGABC (421, primeiras horas), A Crítica (1.544) | 🔧 (o plano citava 421 contra 1,5 mil como divergência: eram horários diferentes) |
| F9 | Teste de integridade de 2026, inclusive com biometria: sem divergência relatada | TSE e TRE-SP (out/2026) | Metrópoles (relatório do TSE) | ✅ |
| F10 | Serviço de justificativa mostrou "FALTOU" em 06/out; trocado por "em processamento"; processamento até 11/out (Res. 23.750/2026); quitação suspensa até 11/out | O Povo, Olhar Digital (06/out) | Fato ou Boato da JE (2026) e a tela mostrada no ref-04 | ✅ |
| F11 | Desmentido do TSE (10/ago): procedimentos *"impedem"* o voto no lugar de outro; não menciona a liberação manual | TSE, lido no navegador em 13/out | TRE-AC e TRE-PE republicaram | ✅ |

## 2. Casos

| # | Fato | Fonte | Segunda fonte | Estado |
|---|---|---|---|---|
| C1 | Salvador, 04/out/2026: mesária presa em flagrante (Escola Estadual José Calazans Brandão da Silva, Santa Cruz); o policial militar em trânsito passou pela biometria, ela disse que o eleitor anterior deixou voto em aberto e que, ao resolver, votou no lugar dele; ouvida na PF e liberada | Bahia Notícias (a partir do g1 e da TV Bahia) | Correio, A Tarde | ✅ |
| C2 | Operação Heterônimo (PF), Cabedelo/PB, 23/set/2026: 11 registros de identidade da mesma pessoa por digital; 3 inscrições eleitorais suspeitas (Santa Rita/PB, Benevides/PA, Brasília/DF) | PF, gov.br | Paraíba Online, WSCOM | ✅ |
| C3 | Pescaria Brava/SC, 2016: eleição para prefeito decidida por **um voto**; uma eleitora já morta votou; segundo o Comprova, **a Polícia Civil de SC concluiu que o voto foi registrado deliberadamente por um mesário**; o TRE-SC anulou os 183 votos da urna; o TSE discutiu nova eleição para a seção (julgamento suspenso por vista em 2017; desfecho não achado) | Conjur, 29/jun/2017 | Comprova (SBT News e Correio Braziliense, mar/2024) | ✅ (o desfecho no TSE fica ⬜) |
| C4 | Ceará, 04/out: 23 crimes eleitorais em 15 municípios; 2 prisões por compra de voto (Itapajé, Tabuleiro do Norte); 6 procedimentos da PF; 91 urnas trocadas; nenhum caso noticiado de voto no lugar de outro | Diário do Nordeste | O Povo | ✅ |
| C6 | 2022, Lisboa (voto no exterior): eleitor votou no lugar de outra pessoa; a PF tratou como crime do art. 309 e a urna foi impugnada (votação seguiu em cédula) | Tribuna de Jundiaí (cobertura das eleições 2022) | Canal Rural | ✅ (data pelo endereço das matérias; a conferir no texto) |
| C7 | Código Eleitoral, art. 309: *"votar ou tentar votar mais de uma vez, ou em lugar de outrem"*, reclusão até três anos | LegJur (texto da Lei 4.737/1965) | Estratégia Concursos | ✅ |
| C8 | Boato de 2022 de eleitor morto em 2010 com voto computado em 2022: o TSE classificou como falso (série Viralizou, ago/2026) | TSE | ⬜ | ⚠️ |
| C5 | Camaçari/BA: coligação denunciou mesários entregando papéis na fila | Gomes News | ⬜ | ⚠️ |

## 3. Quem acusou

| # | Fato | Fonte | Segunda fonte | Estado |
|---|---|---|---|---|
| A1 | Eduardo Bolsonaro, 24/abr/2026 (Rede Comunica Brasil): votos da Bahia depois das 17h, mesários *"em conluio"*; TRE-BA respondeu em 25/abr | Bahia Notícias | A Tarde | ✅ |
| A2 | Eduardo Prado (06/out): senadores eleitos do PT 15,9 mi, Lula 53,9 mi; do PL 58,2 mi, Flávio 56,1 mi | O Tempo | — | ⚠️ (os números são refeitos no teste A6) |
| A3 | Flávio, live de 17/set: fiscais *"para evitar que pessoas mal-intencionadas votem no lugar de outras"*, *"em especial no momento em que a urna fechou"* | Metrópoles, 30/set | Agenda do Poder, CLM Brasil | ✅ |
| A4 | Em 2022 também houve chamada de fiscais: o site do PL convidava apoiadores a serem fiscais de urna, e a convocação de bolsonaristas para fiscalizar seções cresceu na véspera do 2º turno | Nexo, 23/out/2022 | Mais Goiás (reportagem sobre o 2º turno de 2022) | ✅ (o comentarista do ref-06 disse que em 2022 *"não botaram o fiscal"*) |
| A5 | Áudio viral de 2022: "descriptografou o log", milhões depois das 17h, votos passaram de 1:40 para 32 a 35 s | checagem da JE de 28/11/2022 | — | ✅ (o conteúdo do áudio vem da checagem) |
| A6 | 2022: PL e Instituto Voto Legal pediram anular votos de ~279 mil urnas antigas pelo código repetido no log; análise da USP, UFSCar e UFPA: alegações infundadas, bug real de baixo impacto | Poder360 | IstoÉ, Spotniks | ✅ |
| A7 | 2022: relatório da Defesa não apontou fraude e disse que não era possível afirmar o sistema isento de código malicioso | O Povo | Jornal Opção, Aos Fatos | ✅ |

## 4. Dados de contexto

| # | Fato | Fonte | Segunda fonte | Estado |
|---|---|---|---|---|
| D1 | Pesquisa **Genial/Quaest**, 5 a 9/fev/2026: 53% concordam que as urnas são confiáveis, 43% discordam; eleitores de Lula em 2022: 75%; de Bolsonaro: 26% | Poder360 | InfoMoney, Diário de Pernambuco | 🔧 (o Spotniks chamou de "Quest") |
| D2 | TCU, 2022: amostra de 4.161 boletins do 1º turno; nenhuma divergência | portal do TCU | Metrópoles, Poder360 | ✅ |
| D3 | Abstenção 2026: 33.453.535 eleitores, 21,1% (imprensa: 21,08%) | CSV oficial do boletim de urna, recalculado | Gazeta SP, Correio da Manhã | ✅ |
| D4 | quehorasvotar (Uapé): em Manaus, 2026, 4.013 seções, 67.846 pessoas votaram depois das 16h locais (17h de Brasília), última às 20h11 na Colônia Antônio Aleixo, 568 seções mais de 1 h além do horário, 34 mais de 2 h; 2022: urnas com 5 ou mais na fila no encerramento caíram de 27% (1º turno) para 0,03% (2º) | marioadolfo.com, 10/out/2026 | ⬜ | ✅ **reproduzido pelo leitor** (`docs/VALIDACAO_DO_LEITOR.md`, V2): 4 de 5 números iguais, o 5º a 0,8% |
| D5 | Elmano (PT) reeleito no 1º turno no Ceará com 53,19% dos válidos; Ciro Gomes 46,22% | CSV oficial do boletim de urna, recalculado | O Povo | ✅ |

## 5. Voto impresso e segurança

| # | Fato | Fonte | Segunda fonte | Estado |
|---|---|---|---|---|
| V1 | Lei 12.034/2009, art. 5º (voto impresso a partir de 2014): STF suspendeu em out/2011 e declarou inconstitucional em 06/11/2013 (ADI 4543, Cármen Lúcia, unânime) | voto da ADI 4543 (Poder360) | Wagner Advogados | ✅ |
| V2 | Lei 13.165/2015, art. 59-A da Lei 9.504: STF declarou inconstitucional em set/2020 (ADI 5889, Gilmar Mendes, unânime) | Sedep (notícia do STF) | Monitor Mercantil | ✅ |
| V3 | PEC 135/2019 rejeitada pela Câmara em 10/08/2021: 229 a 218, uma abstenção (precisava de 308) | Suno | CUT, Congresso em Foco | ✅ |
| V4 | TPS 2012 (UnB, Aranha): embaralhamento do registro digital do voto revertido; corrigido depois | Baguete, Aos Fatos | artigo de Aranha (SBSeg) | ✅ |
| V5 | TPS 2017: bibliotecas sem verificação de integridade, chave compartilhada recuperada, código injetado na urna de teste; TSE passou a assinar todas as bibliotecas | SBSeg (artigo da equipe) | apresentação APCF na Câmara (2018), TecMundo | ✅ |
| V6 | Namíbia: Suprema Corte, 05/02/2020 (caso Itula), urna sem papel conferível é inconstitucional; eleição de 2019 mantida | Namibian Sun, The Namibian | Oxford Human Rights Hub, Africanews | ✅ |
| V7 | Alemanha, 2009 (2 BvC 3/07): o cidadão tem de poder conferir os passos essenciais sem conhecimento técnico | comunicado do Tribunal Constitucional | CCC, EDRi | ✅ |
| V8 | Índia: VVPAT em todas as seções desde 2019; contagem obrigatória em 5 seções sorteadas por distrito; o papel prevalece; mantido pela Suprema Corte em abr/2024 | Scroll (2019) | Deccan Herald (2024), ThePrint | ✅ |
| V9 | EUA: auditoria de limitação de risco, Colorado em todo o estado desde 2017 | Wikipedia + EAC | Carter Center, NASS | ✅ |
| V10 | México: o PREP publica a imagem de cada ata com hash | IEEM (documento técnico) | Posta, El Imparcial | ✅ |
| V11 | Argentina: telegramas de cada mesa escaneados e publicados no escrutínio provisório | Canal 26 (2019) | Chequeado | ⚠️ (fontes de 2015 a 2023) |
| V12 | Invasão da rede do TSE em 2018: ofício do TSE à PF de 07/11/2018 (gestão Rosa Weber); acesso ao código-fonte do Gedai-UE (sistema de preparação das urnas) e a credenciais; TSE: sem impacto no resultado; especialistas: não prova fraude, mostra vulnerabilidade | Metrópoles | Poder360, Gazeta do Povo | ✅ |
