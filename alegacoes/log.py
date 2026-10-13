"""Leitor do log da urna (logd.dat dentro do log.jez), definicoes do PRE_REGISTRO.md secao 1.

Formato de cada linha: DD/MM/AAAA HH:MM:SS <TAB> nivel <TAB> id da urna <TAB> aplicativo <TAB> mensagem <TAB> verificador.
So entram eventos de 04/10/2026 do aplicativo VOTA.

Cada eleitor e uma TENTATIVA que termina em "O voto do eleitor foi computado". Uma tentativa comeca em
"Identificador digitado pelo mesario foi:" (redigitar o titulo reabre a tentativa). O tipo de liberacao e o da
ultima habilitacao antes do voto computado:
  biometrica   "Tipo de habilitacao do eleitor [biometrica]"
  manual_mes   sem biometrica e com a digital de um mesario na tentativa (a digital do eleitor falhou; Res. 23.759,
               art. 21): "Solicita digital do mesario", "Capturada a digital do mesario", "Mesario <id> habilitou o
               eleitor" ou "Digital coletada bate com uma digital gravada apos o registro inicial de mesario" (este
               ultimo e o mesario que nao se cadastrou no inicio do dia: a digital existe, o numero nao; codigo "nao_id")
  manual_sem   sem biometrica, com "Dado digitado confere" e sem mesario (eleitor sem digital cadastrada; art. 20)
  outra        nenhum dos tres (o texto do tipo, se houver, fica em `tipo_txt`)
"""

from __future__ import annotations

import hmac
import hashlib
import io
import re
import zipfile
from dataclasses import dataclass, field

DIA = "04/10/2026"
RE_MESARIO = re.compile(r"Mes.rio (\d+) habilitou o eleitor")
RE_TIPO = re.compile(r"Tipo de habilita..o do eleitor \[(.+?)\]")
RE_IDENT = re.compile(r"Identificador digitado pelo mes.rio foi: \((.+?)\)")


def ler_jez(blob: bytes) -> list[str]:
    z = zipfile.ZipFile(io.BytesIO(blob))
    nome = next(n for n in z.namelist() if n.lower().endswith(".dat"))
    return z.read(nome).decode("latin-1").splitlines()


def segundos(hhmmss: str) -> int:
    h, m, s = hhmmss.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


@dataclass
class Tentativa:
    ident: str = ""
    tipo_txt: str = ""
    biometrica: bool = False
    confere: bool = False
    nao_confere: int = 0
    pediu_dado: bool = False
    mesario: str = ""
    digital_mesario: bool = False
    tentativas_digital: int = 0
    suspenso_mesario: bool = False
    habilitado: bool = False
    suspensao: int = 0


@dataclass
class Leitura:
    eleitores: list = field(default_factory=list)  # (t_voto_s, tipo, nao_confere, mesario_cod, tentativas_digital, ident, suspensao, habilitado, suspenso_mesario)
    primeiro_evento_s: int | None = None
    pronta_s: int | None = None
    encerrar_s: int | None = None
    id_urna: str = ""
    linhas_dia: int = 0
    tipos_txt: dict = field(default_factory=dict)
    contingencia: bool = False


def classificar(t: Tentativa) -> str:
    if t.biometrica:
        return "biometrica"
    if t.mesario or t.digital_mesario:
        return "manual_mes"
    if t.confere:
        return "manual_sem"
    return "outra"


def ler_log(linhas: list[str], chave: bytes) -> Leitura:
    out = Leitura()
    t = Tentativa()
    for ln in linhas:
        if not ln.startswith(DIA):
            continue
        partes = ln.split("\t")
        if len(partes) < 5:
            continue
        out.linhas_dia += 1
        hora = partes[0][11:19]
        app, msg = partes[3], partes[4]
        s = segundos(hora)
        if out.primeiro_evento_s is None:
            out.primeiro_evento_s = s
            out.id_urna = partes[2]
        if app != "VOTA":
            if "conting" in msg.lower():
                out.contingencia = True
            continue
        if msg.startswith("Identificador digitado pelo mes"):
            m = RE_IDENT.search(msg)
            t = Tentativa(ident=m.group(1) if m else "")
        elif msg.startswith("Tipo de habilita"):
            m = RE_TIPO.search(msg)
            txt = m.group(1) if m else msg
            t.tipo_txt = txt
            out.tipos_txt[txt] = out.tipos_txt.get(txt, 0) + 1
            if txt.lower().startswith("biom"):
                t.biometrica = True
        elif msg.startswith("Solicita digital do mes") or msg.startswith("Capturada a digital do mes"):
            t.digital_mesario = True
        elif msg.startswith("Digital coletada bate com uma digital gravada"):
            t.digital_mesario = True
            if not t.mesario:
                t.mesario = "nao_id"
        elif msg.startswith("Solicita digital"):
            t.tentativas_digital += 1
        elif msg.startswith("Solicita") and "dado pessoal" in msg:
            t.pediu_dado = True
        elif msg.startswith("Dado digitado n"):
            t.nao_confere += 1
        elif msg.startswith("Dado digitado confere"):
            t.confere = True
        elif "habilitou o eleitor" in msg:
            m = RE_MESARIO.search(msg)
            if m:
                t.mesario = hmac.new(chave, m.group(1).encode(), hashlib.sha256).hexdigest()[:12]
        elif msg.startswith("Eleitor foi habilitado"):
            t.habilitado = True
        elif msg.startswith("Eleitor foi suspenso") or msg.startswith("Eleitor votou parcialmente e em seguida foi suspenso"):
            t.suspenso_mesario = True
            t.suspensao += 1
        elif "sem atividade" in msg or "suspen" in msg:
            t.suspensao += 1
        elif msg.startswith("O voto do eleitor foi computado"):
            out.eleitores.append((s, classificar(t), t.nao_confere, t.mesario, t.tentativas_digital, t.ident, t.suspensao, t.habilitado, t.suspenso_mesario))
            t = Tentativa()
        elif msg.startswith("Urna pronta para receber votos"):
            if out.pronta_s is None:
                out.pronta_s = s
        elif msg.startswith("Operador selecionou: Encerrar vota"):
            out.encerrar_s = s
    return out


def vocabulario(linhas: list[str]) -> dict[str, int]:
    """Texto de cada evento do dia, com numeros trocados por N (PRE_REGISTRO 1.1: a forma, nao o resultado)."""
    voc: dict[str, int] = {}
    for ln in linhas:
        if not ln.startswith(DIA):
            continue
        p = ln.split("\t")
        if len(p) < 5:
            continue
        k = p[3] + " | " + re.sub(r"\d+", "N", p[4])
        voc[k] = voc.get(k, 0) + 1
    return voc
