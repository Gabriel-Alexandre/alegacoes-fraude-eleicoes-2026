"""Baixa os CSV oficiais de boletim de urna (1o turno) de 2020, 2024 e 2026 do portal de dados abertos do TSE.

Confere cada zip contra o .sha512 publicado ao lado. Os de 2014, 2018 e 2022 ja estao no projeto vizinho
(../apuracao-eleicoes-2026/dados/brutos/historico/) e nao sao baixados de novo.

Uso: python ferramentas/baixar-bweb.py
"""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "dados" / "brutos" / "bweb"
API = "https://dadosabertos.tse.jus.br/api/3/action/package_show?id=resultados-{ano}-boletim-de-urna"
UA = {"User-Agent": "alegacoes-fraude-eleicoes-2026 (pesquisa aberta)"}


def get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r:
        return r.read()


def main() -> None:
    manifesto = []
    for ano in (2026, 2024, 2020):
        pac = json.loads(get(API.format(ano=ano)))["result"]
        res = {r["url"]: r for r in pac["resources"]}
        zips = [u for u in res if u.endswith(".zip") and "_1t_" in u.lower()]
        pasta = DESTINO / str(ano)
        pasta.mkdir(parents=True, exist_ok=True)
        for u in sorted(zips):
            nome = u.rsplit("/", 1)[1]
            alvo = pasta / nome
            esperado = None
            if u + ".sha512" in res:
                esperado = get(u + ".sha512").decode().split()[0].lower()
            if not alvo.exists():
                alvo.write_bytes(get(u))
            sha512 = hashlib.sha512(alvo.read_bytes()).hexdigest()
            ok = esperado is None or esperado == sha512
            manifesto.append({"ano": ano, "arquivo": nome, "url": u, "bytes": alvo.stat().st_size,
                              "sha512": sha512, "sha512_publicado": esperado, "confere": ok})
            print(ano, nome, alvo.stat().st_size, "ok" if ok else "DIVERGE", flush=True)
            if not ok:
                sys.exit(f"hash divergente: {nome}")
    (DESTINO / "MANIFESTO.json").write_text(json.dumps(manifesto, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
