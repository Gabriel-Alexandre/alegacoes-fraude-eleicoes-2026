# Revisão adversarial e conferência de viés

**13/out/2026.** Plano §4 (M8) e §9.1. Duas leituras do relatório, cada uma tentando derrubá-lo de um lado. ⚠️ **As duas foram feitas pela mesma IA que fez a análise, não por pessoas.** É um limite: uma revisão humana de cada lado seria mais forte.

---

## 1. O advogado da acusação (o que o projeto pode ter deixado passar)

| # | Crítica | Procede? | O que foi feito |
|---|---|---|---|
| R1 | **O log não vê quem estava na urna.** Liberação pela digital também pode esconder fraude, se o eleitor verdadeiro estiver presente e outra pessoa votar (o caso de Salvador) | ✅ procede | o caminho foi medido pelo aviso *"o eleitor identificado já votou"* (75.368 episódios, 0,60 por mil votos). Teto: 3% da diferença. Fica **compatível com os dois**, e o que separa é a ata (pedido P2) |
| R2 | **A porta mais fraca foi somada à outra.** Quem não tem digital cadastrada é liberado só pelo ano de nascimento, e o teste juntava esse caminho com o da digital do mesário | ✅ procedia | separado (emenda E12). **Achado:** essa liberação **sobe** depois das 17h em todas as regiões. Mas não vem com mais voto em Lula nem com mais comparecimento; no Ceará vem com mais voto em Flávio. Entrou no relatório (§1.5b) como **a primeira coisa a conferir no caderno** |
| R3 | **O desenho dentro da mesma escola não pega fraude na escola inteira.** Se todas as seções de um local forem fraudadas juntas, não há vizinha limpa para comparar | ✅ procede | duas coisas pegam fraude ampla e não dependem da vizinha: a liberação à mão **não sobe** no fim do dia em nenhuma região (agregado), e o comparecimento por município não sai da própria história no Nordeste (5 de 1.794 municípios). Limite registrado no relatório |
| R4 | **O log vem do mesmo sistema que conta o voto.** Conferir log com boletim prova coerência, não autenticidade | ✅ procede | dito no relatório (§10 e A9). O projeto testa o que pessoas fazem na seção, não o software |
| R5 | **O critério S5 pode deixar passar fraude mais lenta** (votos no ritmo normal) | ✅ procede | a dose-resposta (T1.9) não depende da velocidade e cobre isso; o resultado dela é o do §1.5 |
| R6 | **Duas regiões passaram em "indício forte" ou perto disso** (Sudeste; e no Brasil o p de 0,02) e a análise exploratória "explicou" depois | ⚠️ procede em parte | o veredito pela régua está publicado como saiu (inclusive o "indício" do Sudeste), e a análise exploratória está marcada como feita depois de ver o resultado (E10). A leitura final é da IA, e diz isso |

## 2. O advogado da defesa (o que o projeto pode ter exagerado)

| # | Crítica | Procede? | O que foi feito |
|---|---|---|---|
| D1 | **O vazio de 27,5 minutos pode ser artefato de carimbo de hora**, não parada de recebimento; chamar de "contradição" com a nota do TSE é forte | ✅ procede | o relatório trata como **pergunta sem resposta**, não como prova, e o pedido P1 pergunta exatamente o que o carimbo registra |
| D2 | **"Indício forte" no Sudeste, publicado, vai ser recortado** sem o resto | ✅ procede | o relatório põe na mesma frase a régua, a sobreposição (E11), o comparecimento menor, o tamanho (42 seções, 826 votos) e a análise que desempata |
| D3 | **Mais "já votou" nas seções que Lula venceu** pode ser lido como suspeita | ✅ procede | o relatório diz que acontece **em todas as regiões, inclusive no Sul**, que há explicação inocente e que o teto é de 3% da diferença |
| D4 | **Destacar a liberação sem digital subindo à noite** pode virar manchete de fraude | ⚠️ procede em parte | está no relatório porque é um achado verdadeiro; vem junto com o teste que mostra que ele não acompanha o voto nem o comparecimento |
| D5 | **Os casos isolados (Salvador, Pescaria Brava, Lisboa) ganham peso desproporcional** | ⚠️ procede em parte | eles provam que o mecanismo existe e deixa rastro; o relatório separa "existe" de "move a eleição" pelo teto |
| D6 | **A comparação com outros países pode soar como "o Brasil é atrasado"** | ✅ procede | o relatório diz onde o Brasil está à frente (publicação de dados por seção) e onde está atrás (verificação independente do software) |

## 3. A conferência de viés (plano §9.1)

| Pergunta | Resposta |
|---|---|
| Todo teste tem espelho? | ✅ todos os testes de voto rodaram para Lula e para Flávio; no Ceará, também para Elmano e para o segundo colocado |
| O que a acusação acertou está com o mesmo destaque? | ✅ no placar e no texto: os casos reais (Salvador, Pescaria Brava, Lisboa, Cabedelo), a mudança de local (A12, **confirmado**), a pergunta sem resposta da pausa, a porta sem digital subindo à noite, o "indício" do Sudeste pela régua |
| O que pesa contra a acusação está dito? | ✅ A4, A6 e A7 desmentidos com o número; A1, A2, A3, A8 e A15 não sustentados, cada um com a previsão que falhou |
| Os desmentidos oficiais passaram pela mesma régua? | ✅ o "impedem" do TSE é dito como forte demais (os procedimentos registram, não impedem); a nota da pausa não explica o vazio do registro |
| Algum adjetivo qualifica fonte antes do fato? | ✅ nenhum no relatório; as pessoas aparecem pelo cargo ou pelo veículo |
| Alguma conclusão mais forte que o número? | ⚠️ uma foi pega e corrigida antes de publicar: as seções marcadas de Serra e Cariacica tinham sido descritas como "votaram como as vizinhas", e deram 1,5 e 2,5 pontos a mais para Lula. O texto agora diz os números |
| Algum achado a favor da acusação ficou de fora? | ✅ não: a busca do lado da acusação pegou a porta sem digital (R2), que entrou mesmo depois do resultado principal |
| A linguagem evita "fraude" e "provou que não houve"? | ✅ os vereditos são da régua; "fraude" aparece só como nome da alegação |
