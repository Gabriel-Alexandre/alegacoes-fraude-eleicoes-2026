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
