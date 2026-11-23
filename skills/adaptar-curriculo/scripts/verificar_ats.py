#!/usr/bin/env python3
"""Lê um currículo em PDF do jeito que um ATS lê e aponta problemas.

Uso: python3 verificar_ats.py curriculo.pdf [--palavras "Excel avançado,Power BI"] [--paginas 2]
Código de saída 0 = tudo certo, 1 = pelo menos uma falha.

Adaptado de ats_check.py do projeto job-hunt-copilot (MIT, (c) 2026 Omkar Chavan).
"""
import argparse
import re
import subprocess
import sys
import unicodedata

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("Falta a biblioteca pypdf. Instale com:  sudo pacman -S python-pypdf")

# frases cortadas no meio costumam terminar numa dessas palavras
SOLTAS = r"\b(de|da|do|das|dos|em|com|para|por|e|a|o|ao|na|no)\s*$"
SECOES = ["RESUMO", "EXPERIENCIA", "FORMACAO", "HABILIDADES|COMPETENCIAS"]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def extrair(caminho):
    textos = {"pypdf": "\n".join(p.extract_text() or "" for p in PdfReader(caminho).pages)}
    try:
        textos["pdftotext"] = subprocess.run(["pdftotext", caminho, "-"], capture_output=True,
                                             text=True, timeout=60).stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return textos


def verificar(caminho, palavras, max_paginas):
    res = []

    def reg(ok, nome, detalhe=""):
        res.append(("OK  " if ok else "FALHA", nome, detalhe))

    n = len(PdfReader(caminho).pages)
    reg(n <= max_paginas, "número de páginas", f"{n} página(s), limite {max_paginas}")

    for ferramenta, t in extrair(caminho).items():
        plano = " ".join(t.split())
        lixo = sum(1 for c in t if 0xE000 <= ord(c) <= 0xF8FF)
        reg(lixo == 0, f"[{ferramenta}] sem caracteres inválidos", f"{lixo} encontrados")

        hifens = sum(t.count(c) for c in "‐‑­")
        reg(hifens == 0, f"[{ferramenta}] hífens normais (sem hífen especial/inquebrável)",
            f"{hifens} encontrados; o ATS não acha 'back-end' escrito com eles")

        quebradas = re.findall(r"\b\w+- \w+", plano)
        reg(not quebradas, f"[{ferramenta}] nenhuma palavra quebrada no fim da linha",
            ", ".join(quebradas[:5]))

        vazios = len(re.findall(r"^\s*[•\-\*]\s*$", t, re.M))
        reg(vazios == 0, f"[{ferramenta}] sem marcadores vazios", f"{vazios} encontrados")

        soltas = [l.strip()[-50:] for l in t.splitlines()
                  if re.search(SOLTAS, l.strip(), re.I) and len(l.strip()) < 25]
        reg(not soltas, f"[{ferramenta}] sem pedaços de frase soltos", " | ".join(soltas[:3]))

        maiusc = sem_acento(plano).upper()
        faltam = [s for s in SECOES if not re.search(s, maiusc)]
        reg(not faltam, f"[{ferramenta}] seções padrão presentes", ", ".join(faltam))

        reg(bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", plano)), f"[{ferramenta}] e-mail legível")
        digitos = re.sub(r"\D", "", plano)
        reg(bool(re.search(r"(55)?[1-9]{2}9?\d{8}", digitos)),
            f"[{ferramenta}] telefone com DDD legível")

        if palavras:
            faltando = [p for p in palavras if p.lower() not in plano.lower()]
            reg(not faltando, f"[{ferramenta}] palavras-chave presentes e inteiras", ", ".join(faltando))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--palavras", default="")
    ap.add_argument("--paginas", type=int, default=2)
    a = ap.parse_args()
    palavras = [p.strip() for p in a.palavras.split(",") if p.strip()]
    res = verificar(a.pdf, palavras, a.paginas)
    for status, nome, detalhe in res:
        print(f"{status}  {nome}" + (f"  ({detalhe})" if detalhe and status != "OK  " else ""))
    falhas = sum(1 for r in res if r[0] == "FALHA")
    print(f"\n{len(res) - falhas}/{len(res)} verificações passaram")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
