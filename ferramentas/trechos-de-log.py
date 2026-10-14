"""Os dois trechos de registro de urna que o vídeo mostra, lidos do log público do TSE e gravados em
docs/TRECHOS_DE_LOG.md, com todo identificador tarjado.

- Paraíba, município 20672, zona 13, seção 137, 1º turno de 2026: uma liberação pelo mesário depois de o ano de
  nascimento não conferir na primeira tentativa.
- Salvador (BA), município 38490, zona 13, seção 315 (Escola Estadual José Calazans Brandão da Silva), o caso da
  mesária presa: uma liberação pela digital da própria pessoa e, em seguida, quatro avisos de "o eleitor identificado
  já votou".

Tarja: todo número de 11 ou 12 dígitos (título, CPF, identificador de mesário) e o código entre parênteses do
batimento de digitais. Nada mais é alterado: as linhas saem como estão no log, com a hora local da urna.

Uso: python ferramentas/trechos-de-log.py      (precisa dos logs locais em dados/brutos/logs, ver docs/REPLICAR.md)
"""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from alegacoes.log import ler_jez  # noqa: E402

TRECHOS = [
    ("Paraíba · município 20672 · zona 13 · seção 137", "pb", "%/pb/20672/0013/0137/%", "08:27:35", "08:28:46",
     "Quatro tentativas de digital sem sucesso, o ano de nascimento não confere na primeira vez e confere na segunda, e o "
     "mesário libera com a digital dele."),
    ("Salvador (BA) · município 38490 · zona 13 · seção 315", "ba", "%/ba/38490/0013/0315/%", "09:28:58", "09:32:06",
     "A escola do caso da mesária presa (Escola Estadual José Calazans Brandão da Silva, seções 315 a 321). Às 09:29:38 "
     "um eleitor é liberado pela própria digital, o voto é computado 22 segundos depois e, em seguida, a urna recusa "
     "quatro vezes liberar alguém que já votou. A reportagem não diz a seção: é compatível com o relato, não é prova de "
     "que seja o mesmo caso."),
]


def tarjar(t: str) -> str:
    t = re.sub(r"\d{11,12}", "•••••••••••", t)
    return re.sub(r"\(\d+\)", "(••••••)", t)


def main() -> None:
    saida = ["# Trechos de registro de urna", "",
             "Gerado por `ferramentas/trechos-de-log.py` a partir do log público de cada urna (TSE, 1º turno de 2026, "
             "`arquivo-urna/.../<seção>-log.jez`, ver `docs/FONTES_DE_DADOS.md`). As linhas estão como no log, com a hora "
             "local da urna; todo identificador (título, CPF, mesário) está tarjado.", ""]
    for titulo, uf, padrao, ini, fim, nota in TRECHOS:
        con = sqlite3.connect(f"file:{RAIZ / 'dados' / 'brutos' / 'logs' / (uf + '.sqlite')}?mode=ro", uri=True)
        blob = con.execute("SELECT body FROM raw WHERE url LIKE ? AND status=200", (padrao,)).fetchone()[0]
        linhas = []
        for l in ler_jez(blob):
            if not l.startswith("04/10/2026"):
                continue
            c = l.split("\t")
            h = c[0][11:19]
            if ini <= h <= fim and not c[4].startswith("Tecla indevida"):
                linhas.append(f"{h}  {tarjar(c[4])}")
        saida += [f"## {titulo}", "", nota, "", "```", *linhas, "```", ""]
    (RAIZ / "docs" / "TRECHOS_DE_LOG.md").write_text("\n".join(saida), encoding="utf-8")
    print("ok docs/TRECHOS_DE_LOG.md")


if __name__ == "__main__":
    main()
