"""Gera docs/DADOS_LOCAIS.md e dados/MANIFESTO.json: o que ocupa disco, o hash, como baixar de novo e o que pode ser
apagado sem perder a reproducao (pedido do autor: os brutos serao apagados depois do video).

O hash de cada banco de logs e o resumo "url<TAB>sha256" ordenado (igual ao projeto da apuracao), entao baixar de
novo e conferir e possivel sem guardar os 44 GB.

Uso: python ferramentas/dados-locais.py
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"


def tamanho(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.exists() else 0


def gb(n: int) -> str:
    return f"{n / 1e9:.1f} GB".replace(".", ",")


def resumo_banco(p: Path) -> dict:
    con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    h = hashlib.sha256()
    n = ok = 0
    for url, sha in con.execute("SELECT url, COALESCE(sha256,'-') FROM raw ORDER BY url"):
        h.update(f"{url}\t{sha}\n".encode())
        n += 1
        ok += sha != "-"
    con.close()
    return {"arquivo": str(p.relative_to(RAIZ)).replace("\\", "/"), "bytes": p.stat().st_size, "itens": n, "ok": ok, "resumo_sha256": h.hexdigest()}


def main() -> None:
    # 14/out/2026: os brutos foram apagados depois do vídeo (docs/DADOS_LOCAIS.md). Sem eles, este script regravaria
    # dados/MANIFESTO.json e resultados/MANIFESTO_DOS_DADOS.json vazios, que são a prova do que foi lido. Só roda
    # depois de baixar tudo de novo.
    if not (DADOS / "brutos" / "logs").exists():
        raise SystemExit("dados/brutos/logs não existe: baixe de novo (docs/REPLICAR.md) antes de regravar os manifestos")
    logs = sorted((DADOS / "brutos" / "logs").glob("*.sqlite"))
    manifesto = {"gerado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "logs": [resumo_banco(p) for p in logs]}
    bweb = DADOS / "brutos" / "bweb" / "MANIFESTO.json"
    if bweb.exists():
        manifesto["bweb"] = json.loads(bweb.read_text(encoding="utf-8"))
    (DADOS / "MANIFESTO.json").write_text(json.dumps(manifesto, indent=1, ensure_ascii=False), encoding="utf-8")
    # copia o manifesto para o git (ele nao tem dado pessoal: so enderecos e hashes)
    (RAIZ / "resultados" / "MANIFESTO_DOS_DADOS.json").write_text(json.dumps(manifesto, indent=1, ensure_ascii=False), encoding="utf-8")

    pastas = [
        ("dados/brutos/logs", "os 499.161 logs de urna de 2026, um banco SQLite por UF, com o `log.jez` original e o sha256 de cada um", "**sim**, depois do vídeo", "`python -m alegacoes.coleta_logs todas 75` (lê os endereços do projeto `apuracao-eleicoes-2026`); ~2 h"),
        ("dados/brutos/bweb", "CSV oficiais de boletim de urna de 2020, 2024 e 2026 (zip original, conferido pelo sha512 publicado)", "sim", "`python ferramentas/baixar-bweb.py`; ~15 min"),
        ("dados/brutos/eleitorado", "locais de votação de 2026 (nome, endereço, local original)", "sim", "baixar `eleitorado_local_votacao_2026.zip` do portal de dados abertos"),
        ("dados/derivados/logs", "uma linha por voto computado (tipo de liberação, hora, código do mesário por HMAC) e uma por urna", "sim (sai dos brutos)", "`python -m alegacoes.derivar_logs todas`"),
        ("dados/derivados/bweb", "os CSV oficiais de 2014 a 2026 em parquet", "sim (sai dos brutos)", "`python -m alegacoes.bweb 2014,2018,2020,2022,2024,2026 todas`"),
        ("dados/derivados/secoes", "a tabela por seção de 2026 (métricas do log + boletim)", "sim: **uma cópia sem dado pessoal fica no git** (`resultados/dados/secoes_2026.parquet`)", "`python -m alegacoes.secoes todas`"),
        ("dados/chave-local.txt", "a chave do HMAC que transforma o número do mesário em código", "⚠️ **se apagar, os códigos de mesário mudam** na próxima leitura (os resultados não, só os códigos)", "nasce sozinha na primeira leitura"),
        ("dados/execucao", "saídas de terminal das execuções", "sim", "—"),
    ]
    linhas = ["# Dados locais: o que ocupa disco e o que pode ser apagado", "",
              f"Gerado por `ferramentas/dados-locais.py` em {manifesto['gerado_utc']}. Pedido do autor (13/out/2026): os dados serão apagados depois do vídeo, e tudo tem de ficar reutilizável.", "",
              "## O que precisa existir para reproduzir os resultados **sem** os brutos", "",
              "- o código (`alegacoes/`, `ferramentas/`) e os critérios (`docs/PRE_REGISTRO.md`)",
              "- `resultados/` inteiro, inclusive `resultados/dados/secoes_2026.parquet` (a tabela por seção, sem dado pessoal) e `resultados/MANIFESTO_DOS_DADOS.json` (o hash de cada banco de logs e de cada zip)",
              "- os testes do `ferramentas/analise-1-*.py` que dependem só da tabela por seção rodam a partir do parquet; os que precisam da linha por voto (leitura à mão, segundo leitor) exigem baixar os logs de novo", "",
              "## Pasta por pasta", "", "| Pasta | O que tem | Tamanho | Pode apagar? | Como recriar |", "|---|---|---|---|---|"]
    for pasta, oque, apagar, recriar in pastas:
        p = RAIZ / pasta
        tam = p.stat().st_size if p.is_file() else tamanho(p)
        linhas.append(f"| `{pasta}` | {oque} | {gb(tam)} | {apagar} | {recriar} |")
    total = tamanho(DADOS)
    linhas += ["", f"**Total em `dados/`: {gb(total)}.**", "",
               "## Para apagar (depois do vídeo)", "", "```bash", "rm -rf dados/brutos dados/derivados dados/execucao", "```", "",
               "Antes, confira que `resultados/dados/secoes_2026.parquet` e `resultados/MANIFESTO_DOS_DADOS.json` estão no git (`git status` limpo).", "",
               "## Para conferir um download refeito", "",
               "Rode a coleta de novo e depois este script: o `resumo_sha256` de cada UF em `dados/MANIFESTO.json` tem de bater com o de `resultados/MANIFESTO_DOS_DADOS.json`. Se o TSE tirar os arquivos do ar (como aconteceu com os de 2022), o manifesto continua provando o que foi lido.", ""]
    (RAIZ / "docs" / "DADOS_LOCAIS.md").write_text("\n".join(linhas), encoding="utf-8")
    print("ok", gb(total))


if __name__ == "__main__":
    main()
