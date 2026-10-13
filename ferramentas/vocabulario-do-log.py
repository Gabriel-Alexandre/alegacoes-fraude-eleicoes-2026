"""PRE_REGISTRO 1.1: o vocabulario do log numa amostra estratificada por UF (semente 20261013).

Olha a FORMA do log: texto de cada evento com numeros trocados por N e quantas vezes aparece. Nao liga
evento a voto nem a secao. Saida: resultados/vocabulario_do_log.csv

Uso: python ferramentas/vocabulario-do-log.py [tamanho=1000]
"""

from __future__ import annotations

import random
import sqlite3
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from alegacoes.log import ler_jez, vocabulario  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
LOGS = RAIZ / "dados" / "brutos" / "logs"


def main(tamanho: int) -> None:
    rnd = random.Random(20261013)
    bancos = sorted(LOGS.glob("*.sqlite"))
    contagem = {}
    for b in bancos:
        con = sqlite3.connect(f"file:{b}?mode=ro", uri=True)
        contagem[b.stem] = con.execute("SELECT COUNT(*) FROM raw WHERE status=200").fetchone()[0]
        con.close()
    total = sum(contagem.values())
    voc: dict[str, int] = {}
    lidos = 0
    for b in bancos:
        n = max(5, round(tamanho * contagem[b.stem] / total))
        con = sqlite3.connect(f"file:{b}?mode=ro", uri=True)
        urls = [u for (u,) in con.execute("SELECT url FROM raw WHERE status=200")]
        for u in rnd.sample(urls, min(n, len(urls))):
            blob = con.execute("SELECT body FROM raw WHERE url=?", (u,)).fetchone()[0]
            for k, v in vocabulario(ler_jez(blob)).items():
                voc[k] = voc.get(k, 0) + v
            lidos += 1
        con.close()
    df = pd.DataFrame(sorted(voc.items(), key=lambda x: -x[1]), columns=["evento", "ocorrencias"])
    (RAIZ / "resultados").mkdir(exist_ok=True)
    df.to_csv(RAIZ / "resultados" / "vocabulario_do_log.csv", index=False)
    print(f"{lidos} logs lidos de {len(bancos)} UFs; {len(df)} textos de evento")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1000)
