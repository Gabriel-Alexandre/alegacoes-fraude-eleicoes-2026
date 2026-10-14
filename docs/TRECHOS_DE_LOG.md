# Trechos de registro de urna

Gerado por `ferramentas/trechos-de-log.py` a partir do log público de cada urna (TSE, 1º turno de 2026, `arquivo-urna/.../<seção>-log.jez`, ver `docs/FONTES_DE_DADOS.md`). As linhas estão como no log, com a hora local da urna; todo identificador (título, CPF, mesário) está tarjado.

## Paraíba · município 20672 · zona 13 · seção 137

Quatro tentativas de digital sem sucesso, o ano de nascimento não confere na primeira vez e confere na segunda, e o mesário libera com a digital dele.

```
08:27:35  Capturada a digital. Tentativa [4] de [4]
08:27:37  Número de tentativas de reconhecimento do dedo. Tentativa [4] de [4]
08:27:42  Solicitação de dado pessoal do eleitor para habilitação manual
08:27:56  Dado digitado não confere
08:28:11  Solicitação de dado pessoal do eleitor para habilitação manual
08:28:29  Dado digitado confere
08:28:29  Solicita digital do mesário
08:28:38  Batimento de digitais retornou o score 4
08:28:38  Biometria coletada não é do mesário ••••••••••• (••••••)
08:28:40  Batimento de digitais retornou o score 37
08:28:40  Biometria do mesário ••••••••••• encontrada nos arquivos coletados (••••••)
08:28:40  Mesário ••••••••••• habilitou o eleitor
08:28:46  Eleitor foi habilitado
```

## Salvador (BA) · município 38490 · zona 13 · seção 315

A escola do caso da mesária presa (Escola Estadual José Calazans Brandão da Silva, seções 315 a 321). Às 09:29:38 um eleitor é liberado pela própria digital, o voto é computado 22 segundos depois e, em seguida, a urna recusa quatro vezes liberar alguém que já votou. A reportagem não diz a seção: é compatível com o relato, não é prova de que seja o mesmo caso.

```
09:28:58  Identificador do eleitor digitado pelo mesário
09:28:58  Identificador digitado pelo mesário foi: (Título de eleitor)
09:29:03  Solicita digital. Tentativa [1] de [4]
09:29:11  Capturada a digital. Tentativa [1] de [4]
09:29:13  Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4]
09:29:18  Solicita digital. Tentativa [2] de [4]
09:29:21  Capturada a digital. Tentativa [2] de [4]
09:29:24  Número de tentativas de reconhecimento do dedo. Tentativa [2] de [4]
09:29:26  Solicita digital. Tentativa [3] de [4]
09:29:33  Capturada a digital. Tentativa [3] de [4]
09:29:38  Tipo de habilitação do eleitor [biométrica]
09:29:38  Eleitor foi habilitado
09:29:59  Voto confirmado para [Presidente]
09:30:00  O voto do eleitor foi computado
09:30:01  Aguardando digitação do identificador do eleitor
09:30:24  Identificador do eleitor digitado pelo mesário
09:30:24  Identificador digitado pelo mesário foi: (Título de eleitor)
09:30:24  O eleitor identificado já votou
09:30:26  Aguardando digitação do identificador do eleitor
09:30:48  Identificador do eleitor digitado pelo mesário
09:30:48  Identificador digitado pelo mesário foi: (Título de eleitor)
09:30:48  O eleitor identificado já votou
09:30:51  Aguardando digitação do identificador do eleitor
09:31:13  Identificador do eleitor digitado pelo mesário
09:31:13  Identificador digitado pelo mesário foi: (Título de eleitor)
09:31:13  O eleitor identificado já votou
09:31:15  Aguardando digitação do identificador do eleitor
09:31:23  Aguardando digitação do identificador do eleitor
09:31:48  Aguardando digitação do identificador do eleitor
09:32:06  Identificador do eleitor digitado pelo mesário
09:32:06  Identificador digitado pelo mesário foi: (Título de eleitor)
09:32:06  O eleitor identificado já votou
```
