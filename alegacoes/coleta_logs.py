"""Coleta dos logs de urna (log.jez) do 1o turno de 2026, uma secao por vez.

Os enderecos saem dos aux.json que o projeto apuracao-eleicoes-2026 ja baixou (com hash), entao nenhuma
consulta de indice e refeita. Cada log vai para dados/brutos/logs/<uf>.sqlite, tabela raw, com sha256,
tamanho e hora da coleta, no mesmo formato do projeto da apuracao.

Limite: um coletor so, teto adaptativo de requisicoes por segundo (o TSE responde 429 acima disso; licao
registrada no projeto da apuracao, docs/CORRECOES.md de la).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import aiohttp

RAIZ = Path(__file__).resolve().parents[1]
APURACAO = RAIZ.parent / "apuracao-eleicoes-2026"
BRUTOS_APURACAO = APURACAO / "dados" / "brutos"
BRUTOS = RAIZ / "dados" / "brutos" / "logs"
UA = "alegacoes-fraude-eleicoes-2026 (pesquisa aberta; contato via GitHub Gabriel-Alexandre)"

UFS = ["ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg", "ms", "mt", "pa", "pb", "pe",
       "pi", "pr", "rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to", "zz"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS raw (
  url TEXT PRIMARY KEY, status INTEGER NOT NULL, fetched_utc TEXT NOT NULL,
  nbytes INTEGER NOT NULL, sha256 TEXT, body BLOB
);
"""


def agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def abrir(uf: str) -> sqlite3.Connection:
    BRUTOS.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(BRUTOS / f"{uf}.sqlite")
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")
    con.executescript(SCHEMA)
    return con


def urls_de_log(uf: str) -> list[str]:
    """Todos os log.jez listados nos aux.json da UF (uma secao pode ter mais de um hash: urna substituida)."""
    con = sqlite3.connect(f"file:{BRUTOS_APURACAO / (uf + '.sqlite')}?mode=ro", uri=True)
    out = []
    for url, body in con.execute("SELECT url, body FROM raw WHERE url LIKE '%-aux.json' AND status=200"):
        base = url.rsplit("/", 1)[0]
        dado = json.loads(body)
        for h in dado.get("hashes", []):
            for arq in h.get("arq", []):
                if arq.get("tp") == "log":
                    out.append(f"{base}/{h['hash']}/{arq['nm']}")
    con.close()
    return sorted(set(out))


class Limitador:
    """Teto adaptativo: cai ao receber 429 e sobe devagar enquanto tudo responde (copiado do projeto da apuracao)."""

    def __init__(self, por_segundo: float):
        self.teto = por_segundo
        self.taxa = por_segundo
        self._prox = 0.0
        self._lock = asyncio.Lock()
        self._ok = 0
        self.penalizacoes = 0

    async def esperar(self) -> None:
        async with self._lock:
            agora_ = time.monotonic()
            if self._prox > agora_:
                await asyncio.sleep(self._prox - agora_)
                agora_ = self._prox
            self._prox = agora_ + 1.0 / self.taxa

    def penalizar(self) -> None:
        self.taxa = max(5.0, self.taxa * 0.6)
        self._ok = 0
        self.penalizacoes += 1

    def sucesso(self) -> None:
        self._ok += 1
        if self._ok >= 150:
            self._ok = 0
            self.taxa = min(self.teto, self.taxa * 1.08)


async def baixar(sessao, lim: Limitador, url: str, tentativas: int = 10):
    ultimo = None
    for t in range(tentativas):
        await lim.esperar()
        try:
            async with sessao.get(url) as r:
                corpo = await r.read()
                if r.status in (200, 404, 403):
                    lim.sucesso()
                    return r.status, corpo
                if r.status == 429:
                    lim.penalizar()
                    espera = float(r.headers.get("Retry-After", 0) or 0) or min(30, 1.6**t)
                    await asyncio.sleep(espera)
                    ultimo = "HTTP 429"
                    continue
                ultimo = f"HTTP {r.status}"
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            ultimo = repr(e)
        await asyncio.sleep(min(30, 1.5**t))
    return 0, (ultimo or "falha").encode()


async def coletar_uf(uf: str, lim: Limitador, concorrencia: int) -> dict:
    urls = urls_de_log(uf)
    con = abrir(uf)
    feitos = {u for (u,) in con.execute("SELECT url FROM raw WHERE status IN (200,404)")}
    pendentes = [u for u in urls if u not in feitos]
    escrita = asyncio.Lock()
    sem = asyncio.Semaphore(concorrencia)
    n = 0
    t0 = time.time()
    timeout = aiohttp.ClientTimeout(total=90, connect=20)
    conector = aiohttp.TCPConnector(limit=concorrencia, ttl_dns_cache=300)
    async with aiohttp.ClientSession(headers={"User-Agent": UA}, timeout=timeout, connector=conector) as sessao:

        async def um(url):
            nonlocal n
            async with sem:
                st, corpo = await baixar(sessao, lim, url)
                sha = hashlib.sha256(corpo).hexdigest() if st == 200 else None
                async with escrita:
                    con.execute(
                        "INSERT OR REPLACE INTO raw(url,status,fetched_utc,nbytes,sha256,body) VALUES (?,?,?,?,?,?)",
                        (url, st, agora(), len(corpo), sha, corpo if st == 200 else None),
                    )
                    n += 1
                    if n % 1000 == 0:
                        con.commit()
                        taxa = n / max(1, time.time() - t0)
                        print(f"{uf} {n}/{len(pendentes)} {taxa:.0f}/s teto={lim.taxa:.0f} 429={lim.penalizacoes}", flush=True)

        await asyncio.gather(*[um(u) for u in pendentes])
    con.commit()
    total = con.execute("SELECT COUNT(*), SUM(status=200), SUM(nbytes) FROM raw").fetchone()
    con.close()
    return {"uf": uf, "listados": len(urls), "baixados_agora": len(pendentes), "linhas": total[0], "ok": total[1], "bytes": total[2]}


async def main(ufs: list[str], por_segundo: float, concorrencia: int) -> None:
    lim = Limitador(por_segundo)
    for uf in ufs:
        r = await coletar_uf(uf, lim, concorrencia)
        print(json.dumps(r), flush=True)


if __name__ == "__main__":
    ufs = sys.argv[1].split(",") if len(sys.argv) > 1 and sys.argv[1] != "todas" else UFS
    taxa = float(sys.argv[2]) if len(sys.argv) > 2 else 70
    asyncio.run(main(ufs, taxa, concorrencia=48))
