#!/usr/bin/env python3
"""Monta um currículo amigável a ATS (DOCX + PDF) a partir de um JSON.

Uso:
  python3 montar_curriculo.py conteudo.json saida/Nome_Empresa_Cargo
  python3 montar_curriculo.py --checar      # só verifica as dependências

Gera saida/Nome_Empresa_Cargo.docx e, se o LibreOffice estiver instalado, o .pdf.
Formato do JSON: veja estrutura.md nesta mesma pasta.

Adaptado de build_resume.py do projeto job-hunt-copilot (MIT, (c) 2026 Omkar Chavan).
"""
import json
import os
import re
import shutil
import subprocess
import sys

INSTALAR = "sudo pacman -S python-docx python-pypdf"


def checar():
    ok = True
    try:
        import docx  # noqa: F401
        print("OK    python-docx")
    except ImportError:
        print("FALTA python-docx")
        ok = False
    try:
        import pypdf  # noqa: F401
        print("OK    python-pypdf")
    except ImportError:
        print("FALTA python-pypdf")
        ok = False
    print("OK    pdftotext" if shutil.which("pdftotext") else "FALTA pdftotext (pacote poppler)")
    if shutil.which("soffice") or shutil.which("libreoffice"):
        print("OK    LibreOffice (gera PDF)")
    else:
        print("AVISO LibreOffice não encontrado: só o DOCX será gerado "
              "(para PDF automático: sudo pacman -S libreoffice-fresh)")
    if not ok:
        print(f"\nInstale com:  {INSTALAR}")
    return ok


if len(sys.argv) == 2 and sys.argv[1] == "--checar":
    sys.exit(0 if checar() else 1)

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Mm, Pt, RGBColor
except ImportError:
    sys.exit(f"Falta a biblioteca python-docx. Instale com:  {INSTALAR}")

FONTE = "Calibri"
CORPO = Pt(10.5)
COMPACTO = False
LARGURA = None

TITULOS = {
    "resumo": "Resumo Profissional",
    "experiencia": "Experiência Profissional",
    "formacao": "Formação Acadêmica",
    "habilidades": "Habilidades",
    "idiomas": "Idiomas",
    "cursos": "Cursos e Certificações",
    "projetos": "Projetos",
    "conquistas": "Conquistas",
}
ORDEM_PADRAO = ["resumo", "experiencia", "formacao", "habilidades", "idiomas",
                "cursos", "projetos", "conquistas"]


def fonte(run, tamanho=None, negrito=False, italico=False):
    run.font.name = FONTE
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONTE)
    run.font.size = tamanho or CORPO
    run.bold = negrito
    run.italic = italico
    run.font.color.rgb = RGBColor(0, 0, 0)


def texto(p, conteudo, **fmt):
    """Escreve o texto com o hífen comum (U+002D).

    Não use o "hífen inquebrável" do Word (w:noBreakHyphen): no PDF ele vira U+2011, e o ATS
    deixa de achar palavras como "back-end" ou "e-commerce". Se uma palavra com hífen quebrar no
    fim da linha, o verificar_ats.py acusa, e aí é só reescrever a frase."""
    fonte(p.add_run(conteudo), **fmt)


def espaco(p, antes=0, depois=2):
    pf = p.paragraph_format
    pf.space_before = Pt(antes)
    pf.space_after = Pt(depois)
    pf.line_spacing = 1.0 if COMPACTO else 1.05


def linha_inferior(p):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "1"), ("w:color", "000000")):
        b.set(qn(k), v)
    bdr.append(b)
    pPr.append(bdr)


def titulo_secao(doc, t):
    p = doc.add_paragraph()
    espaco(p, antes=4 if COMPACTO else 8, depois=1 if COMPACTO else 3)
    texto(p, t.upper(), tamanho=Pt(11 if COMPACTO else 12), negrito=True)
    linha_inferior(p)


def paragrafo(doc, t, negrito=False, italico=False, depois=2):
    p = doc.add_paragraph()
    espaco(p, depois=depois)
    texto(p, t, negrito=negrito, italico=italico)
    return p


def topico(doc, t):
    # "•" literal: marcadores de lista do Word viram caracteres inválidos (U+F0B7) no ATS
    p = doc.add_paragraph()
    espaco(p, depois=0 if COMPACTO else 1)
    pf = p.paragraph_format
    pf.left_indent = Inches(0.2)
    pf.first_line_indent = Inches(-0.15)
    pf.tab_stops.add_tab_stop(Inches(0.2))
    texto(p, "•\t" + t)


def cabe_numa_linha(esquerda, direita):
    # estimativa: largura útil em pontos ÷ largura média de um caractere em negrito
    caracteres = (LARGURA / 12700) / (CORPO.pt * 0.55)
    return len(esquerda) + len(direita) + 4 <= caracteres


def linha_com_data(doc, esquerda, direita, antes):
    p = doc.add_paragraph()
    espaco(p, antes=antes, depois=0 if COMPACTO else 1)
    texto(p, esquerda, negrito=True)
    if not direita:
        return
    if cabe_numa_linha(esquerda, direita):
        p.paragraph_format.tab_stops.add_tab_stop(LARGURA, WD_TAB_ALIGNMENT.RIGHT)
        texto(p, "\t" + direita, negrito=True)
    else:
        # não cabe: local e período vão para a linha de baixo, em vez de quebrar torto
        p2 = doc.add_paragraph()
        espaco(p2, depois=0 if COMPACTO else 1)
        texto(p2, direita, italico=True)


def secao_resumo(doc, d, t):
    titulo_secao(doc, t)
    paragrafo(doc, d["resumo"])


def secao_experiencia(doc, d, t):
    titulo_secao(doc, t)
    for e in d["experiencia"]:
        direita = " | ".join(x for x in (e.get("local"), e.get("periodo")) if x)
        linha_com_data(doc, f"{e['cargo']} | {e['empresa']}", direita, 2 if COMPACTO else 4)
        for b in e.get("topicos", []):
            topico(doc, b)


def secao_formacao(doc, d, t):
    titulo_secao(doc, t)
    for f in d["formacao"]:
        if isinstance(f, str):
            topico(doc, f)
            continue
        linha_com_data(doc, f"{f['curso']} | {f['instituicao']}", f.get("periodo", ""), 1)
        if f.get("detalhes"):
            paragrafo(doc, f["detalhes"], depois=2)


def secao_habilidades(doc, d, t):
    titulo_secao(doc, t)
    for h in d["habilidades"]:
        if isinstance(h, str):
            topico(doc, h)
            continue
        p = doc.add_paragraph()
        espaco(p, depois=1)
        texto(p, f"{h['rotulo']}: ", negrito=True)
        texto(p, h["itens"])


def secao_projetos(doc, d, t):
    titulo_secao(doc, t)
    for pr in d["projetos"]:
        p = doc.add_paragraph()
        espaco(p, antes=1 if COMPACTO else 3, depois=0)
        texto(p, pr["nome"], negrito=True)
        if pr.get("tecnologias"):
            texto(p, f" | {pr['tecnologias']}", italico=True)
        if pr.get("link"):
            # URL escrita por extenso: o ATS perde links "escondidos" atrás de palavras
            texto(p, f" | {pr['link']}")
        for b in pr.get("topicos", []):
            topico(doc, b)


def secao_lista(chave):
    def f(doc, d, t):
        titulo_secao(doc, t)
        for item in d[chave]:
            topico(doc, item)
    return f


SECOES = {
    "resumo": secao_resumo,
    "experiencia": secao_experiencia,
    "formacao": secao_formacao,
    "habilidades": secao_habilidades,
    "idiomas": secao_lista("idiomas"),
    "cursos": secao_lista("cursos"),
    "projetos": secao_projetos,
    "conquistas": secao_lista("conquistas"),
}


def montar(d, base):
    global CORPO, COMPACTO, LARGURA
    titulos = {**TITULOS, **d.get("titulos_secoes", {})}
    COMPACTO = bool(d.get("compacto"))
    CORPO = Pt(d.get("tamanho_fonte", 9.5 if COMPACTO else 10.5))

    doc = Document()
    for s in doc.sections:
        s.page_width, s.page_height = Mm(210), Mm(297)  # A4
        s.top_margin = s.bottom_margin = Inches(0.35 if COMPACTO else 0.6)
        s.left_margin = s.right_margin = Inches(0.5 if COMPACTO else 0.7)
    s = doc.sections[0]
    LARGURA = s.page_width - s.left_margin - s.right_margin
    doc.styles["Normal"].font.name = FONTE
    doc.styles["Normal"].font.size = CORPO

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    espaco(p, depois=1)
    texto(p, d["nome"], tamanho=Pt(17), negrito=True)
    if d.get("titulo"):
        p = paragrafo(doc, d["titulo"], negrito=True, depois=1)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = paragrafo(doc, " | ".join(d.get("contato", [])), depois=4)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    ordem = d.get("ordem") or ORDEM_PADRAO
    ordem = ordem + [k for k in ORDEM_PADRAO if k not in ordem]
    for chave in ordem:
        if chave in SECOES and d.get(chave):
            SECOES[chave](doc, d, titulos[chave])

    pasta = os.path.dirname(os.path.abspath(base))
    os.makedirs(pasta, exist_ok=True)
    caminho_docx = base + ".docx"
    doc.save(caminho_docx)
    print(f"DOCX: {caminho_docx}")

    office = shutil.which("soffice") or shutil.which("libreoffice")
    if not office:
        print("PDF: LibreOffice não encontrado. Abra o DOCX e exporte como PDF, "
              "ou instale com: sudo pacman -S libreoffice-fresh")
        return
    subprocess.run([office, "--headless", "--convert-to", "pdf", "--outdir", pasta, caminho_docx],
                   check=False, capture_output=True, timeout=180)
    caminho_pdf = base + ".pdf"
    print(f"PDF: {caminho_pdf}" if os.path.exists(caminho_pdf) else "PDF: a conversão falhou")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as arq:
        montar(json.load(arq), sys.argv[2])
