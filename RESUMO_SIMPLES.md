# As alegações de fraude no 1º turno de 2026, em linguagem simples

Este projeto baixou o registro interno de **todas as 499 mil urnas** do 1º turno (o "log", que anota cada passo da urna com hora ao segundo) e os boletins de urna de 2014 a 2026, e testou, uma por uma, as alegações de fraude que mais circularam. A versão completa, com os números e os testes, está em [`RELATORIO.md`](RELATORIO.md).

**Quem fez.** Uma IA (Claude), sob a direção do autor do repositório, que aprovou o plano antes. As regras de cada teste foram escritas e gravadas antes de olhar os dados; o que mudou depois está registrado e marcado.

## O que o log mostra

Para votar, a pessoa é liberada pela própria digital. Se a digital falha, o mesário pergunta o ano de nascimento e libera com a digital **dele**; quem não tem digital cadastrada é liberado só pelo ano de nascimento. **O log registra qual dos caminhos foi usado, eleitor por eleitor.** Quem vota no lugar de outra pessoa não tem a digital dela, então esse tipo de fraude teria de aparecer como liberação "à mão".

## As respostas, uma por uma

**"Mesários votam no lugar de quem faltou, no fim do dia, sobretudo no Nordeste."**
O dado não sustenta isso como esquema capaz de mudar a eleição. A liberação à mão é de 12% dos votos antes das 17h e de 12% depois, e no Nordeste também não sobe. Onde há mais liberação à mão no fim do dia, o comparecimento é **menor**, quando votar por quem faltou o faria maior. As seções que votam até tarde votam um pouco mais em Lula, mas isso acontece igual entre os eleitores liberados pela **própria digital**, ou seja, gente que estava lá: é o perfil de quem vota tarde, e aparece até no Sul. **Casos isolados existem e foram pegos:** uma mesária presa em Salvador no dia da eleição, um mesário que registrou o voto de uma eleitora morta em Santa Catarina em 2016.

**"Os votos depois das 17h são o rastro da fraude."**
3,7 milhões de pessoas votaram depois das 17h (em 2022, 4 milhões). É fila: quem estava na fila às 17h tem direito de votar. 88% delas foram liberadas pela própria digital, e o voto delas durou o mesmo que o da manhã (57 segundos contra 55).

**"A abstenção é usada como reserva."**
O Nordeste vai mais votar que a média desde 2018, não só em 2026. E as seções com comparecimento altíssimo têm **menos** liberação à mão, não mais.

**"Votei e o sistema diz que faltei."**
Foi atraso de processamento, corrigido até 11/10. E a fraude por mesário daria o sintoma **contrário**: quem faltou apareceria como presente.

**"A apuração parou só para presidente."**
Quando a tela voltou, mostrou exatamente o que os boletins já recebidos somavam. Fica uma pergunta para o TSE: a nota diz que os boletins continuaram chegando durante a pausa, e o registro público tem 27 minutos e meio sem nenhum.

**"A conta não fecha: os senadores do PL tiveram mais votos que o Flávio."**
A conta compara **todos** os candidatos do PL com **só os eleitos** do PT, e esquece que cada eleitor votou em **dois** senadores.

**"A curva da apuração é lisa demais para ser verdade."**
Ela é **mais irregular** do que seria se os boletins chegassem em ordem aleatória.

**"Com os fiscais do PL, a fraude parou e o Flávio ficou na frente."**
A queda da liberação sem digital aconteceu entre 2022 e **2024**, numa eleição municipal, antes de qualquer campanha de fiscais de 2026. De 2024 para 2026, no Nordeste, ela até subiu.

**"Mudaram o meu local de votação."**
É verdade: 6.589 seções (1,3% do total) mudaram de local, com quase 2 milhões de eleitores, em todos os estados.

## O teto

Mesmo que **todas** as 441.896 liberações à mão feitas depois das 17h no país fossem fraude, e todas para um lado só, elas seriam **um quinto da diferença** entre Flávio e Lula, e **6%** do que Flávio precisaria para ganhar no 1º turno.

## O que este projeto não consegue ver

Quem estava fisicamente diante da urna (isso está na assinatura do caderno e na ata, que ficam nos cartórios), o software da urna, e cada voto depois das 17h (a urna embaralha a ordem dos votos para proteger o sigilo). Os pedidos para quem tem esses documentos estão prontos em [`docs/PEDIDOS_LAI.md`](docs/PEDIDOS_LAI.md).

## Você pode ajudar

Se você **não** foi votar no 1º turno, consulte a sua situação no e-Título ou no site do TSE. O certo é aparecer que você faltou. Se aparecer que você votou, registre no cartório eleitoral ou na Ouvidoria do TSE. Detalhes em [`docs/CONVITE_PUBLICO.md`](docs/CONVITE_PUBLICO.md).
