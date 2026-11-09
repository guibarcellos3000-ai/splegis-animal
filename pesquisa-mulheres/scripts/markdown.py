import json, re, os, glob
r=json.load(open("resultado.json"))
alvo=[x for x in r["incluidos"] if x["Situação"]=="Em tramitação"]
OUT="/home/user/splegis-animal/pesquisa-mulheres/inteiro-teor"
os.makedirs(OUT,exist_ok=True)
S="https://splegisconsulta.saopaulo.sp.leg.br"
RUIDO=re.compile(r"^(fls?\.?|fis\.?)\s*\d+$|^autuado por|^Matéria PL|^Documento assinado|^https?://|^[\W_\d]{0,4}$|^[A-Za-zÀ-ú]{1,2}$", re.I)
INICIO=re.compile(r"^(Art\.|§|Parágrafo|[IVXL]+\s*[-–—]|[a-z]\)|JUSTIFICATIVA|Sala das Sess|A CÂMARA MUNICIPAL|PROJETO DE LEI)", re.I)
def limpa_linha(l):
    l=l.strip().replace("—","—")
    l=re.sub(r"^\|\s*[-–—]", "I -", l); l=re.sub(r"^\|\s+", "I ", l)
    l=re.sub(r"^Il(?=\s*[-–—])","II",l); l=re.sub(r"^Ill(?=\s*[-–—])","III",l); l=re.sub(r"^lV(?=\s*[-–—])","IV",l)
    l=re.sub(r"(^|\s)\$\s?(\d)", r"\1§\2", l)
    l=re.sub(r"\s+[|]\s*$","",l)
    return l
def limpa_antigo(txt):
    out=[]
    for l in txt.split("\n"):
        l=re.sub(r"^(?:[^\wÀ-ú§]+|\b[\wÀ-ú]{1,2}\b[^\wÀ-ú§]*){1,4}(?=[A-ZÀ-Ú§][\wÀ-ú]{2,})","",l.strip()) if l.strip() else ""
        letras=sum(ch.isalpha() for ch in l)
        if l and (letras < 0.6*len(l.replace(" ","")) or letras<4): continue
        out.append(l)
    return "\n".join(out)
def paragrafos(txt):
    blocos=[]; atual=[]
    for l in txt.split("\n"):
        l=limpa_linha(l)
        if not l:
            if atual: blocos.append(atual); atual=[]
            continue
        if RUIDO.search(l): continue
        if atual and INICIO.search(l): blocos.append(atual); atual=[]
        atual.append(l)
    if atual: blocos.append(atual)
    juntos=[]
    for b in blocos:
        prev=juntos[-1][-1] if juntos else ""
        if juntos and not re.search(r"[.:;!?]$|DECRETA:?$", prev) and (re.match(r"^[a-zà-ú(]", b[0]) or (re.search(r"[a-zà-ú,]$", prev) and not INICIO.search(b[0]) and not re.match(r"^[A-ZÀ-Ú\s\W\d]+$", b[0]))):
            juntos[-1]+=b
        else: juntos.append(b)
    blocos=juntos
    out=[]
    for b in blocos:
        s=""
        for l in b:
            if s.endswith("-") and not s.endswith(" -"): s+=l       # palavra hifenizada (ex.: somando-se)
            else: s=(s+" "+l).strip()
        out.append(s)
    return out
def formata(p):
    p=re.sub(r"^(Art\.\s*\d+[º°o]?[-A-Z]*)", r"**\1**", p)
    p=re.sub(r"^(§\s*\d+[º°]?|Parágrafo único\.?)", r"**\1**", p, flags=re.I)
    if re.match(r"^JUSTIFICATIVA", p, re.I): return "### Justificativa"
    if re.match(r"^A CÂMARA MUNICIPAL DE SÃO PAULO DECRETA", p, re.I): return "**A CÂMARA MUNICIPAL DE SÃO PAULO DECRETA:**"
    return p
indice=[]; tudo=[]
for x in alvo:
    n,a=x["Projeto"].split()[1].split("/")
    fn=f"PL-{int(n):04d}-{a}.md"
    d=json.load(open(f"ocr/{a}-{n}.json")) if os.path.exists(f"ocr/{a}-{n}.json") else {"erro":"não processado"}
    linhas=[f"# {x['Projeto']}", "", f"**Ementa:** {x['Ementa']}", "",
      "| Campo | Informação |","|---|---|",
      f"| Autor(es) | {x['Autor(es)']} |", f"| Apresentação | {x['Apresentação']} |", f"| Tema | {x['Tema']} |",
      f"| Parecer CCJ | {x['Parecer CCJ']} |", f"| Fase atual | {x['Fase / última tramitação']} |",
      f"| Ficha oficial | [SPLegis]({x['Link SPLegis']}) |"]
    if d.get("pid"): linhas.append(f"| Documento transcrito | [{'Texto inicial' if d.get('inicial') else 'Processo digitalizado'} (PDF)]({S}/Home/AbrirDocumento?pID={d['pid']}) |")
    subs=d.get("substitutivos") or []
    if subs: linhas.append("| Substitutivos | "+" · ".join(f"[{t}]({S}/Home/AbrirDocumento?pID={p})" for p,t in subs)+" |")
    linhas+=["",""]
    aviso="> **Atenção:** transcrição automática (OCR) do texto inicial do projeto. Pode conter erros de reconhecimento e não reflete emendas ou substitutivos posteriores. Confira sempre o PDF oficial antes de citar."
    if d.get("pid") and not d.get("inicial"):
        aviso="> **Atenção:** projeto antigo, disponível apenas como processo digitalizado. A transcrição (OCR) das primeiras páginas tem qualidade limitada e pode incluir capa, carimbos e despachos. Confira sempre o PDF oficial."
    if d.get("paginas"):
        bruto="\n\n".join(d["paginas"]); bruto=bruto if d.get("inicial") else limpa_antigo(bruto)
        ps=paragrafos(bruto)
        if not d.get("inicial"):
            k=next((i for i,p in enumerate(ps) if re.search(r"DECRETA",p,re.I)),None)
            if k is not None:
                ini=max(0,k-3)
                for j in range(k,max(-1,k-6),-1):
                    if re.match(r"^PROJETO DE LEI",ps[j],re.I): ini=j; break
                ps=ps[ini:]
        corpo=[formata(p) for p in ps]
        linhas+=[aviso,"","## Inteiro teor","",*[c+"\n" for c in corpo]]
        status="Transcrito" if d.get("inicial") else "Transcrito (digitalização antiga)"
    else:
        linhas+=[f"> Texto não disponível para transcrição automática ({d.get('erro','sem documento')}). Consulte a ficha oficial."]
        status="Não disponível"
    md="\n".join(linhas).rstrip()+"\n"
    open(f"{OUT}/{fn}","w").write(md)
    tudo.append(md)
    indice.append(f"| [{x['Projeto']}]({fn}) | {x['Ementa'][:140]}{'…' if len(x['Ementa'])>140 else ''} | {x['Tema']} | {status} |")
cab=["# Inteiro teor — Projetos de Lei sobre proteção às mulheres em tramitação (Município de São Paulo)","",
 f"{len(alvo)} projetos em tramitação na Câmara Municipal de São Paulo, segundo o levantamento de 09/11/2026 (ver `../SPLegis-Mulheres-Projetos-de-Lei.xlsx`).","",
 "- Cada projeto tem um arquivo próprio, com dados de tramitação, link para a ficha oficial e o inteiro teor transcrito do PDF do **texto inicial**.",
 "- O arquivo [`todos-os-projetos.md`](todos-os-projetos.md) reúne todos os textos em um só documento.",
 "- A transcrição foi feita por OCR (os PDFs da Câmara não permitem copiar o texto diretamente). Pode haver erros pontuais: **confira o PDF oficial antes de citar** em parecer, projeto ou artigo.",
 "- Textos de projetos de lei são atos oficiais e não são protegidos por direito autoral (Lei nº 9.610/1998, art. 8º, IV).","",
 "| Projeto | Ementa | Tema | Transcrição |","|---|---|---|---|",*indice]
open(f"{OUT}/README.md","w").write("\n".join(cab)+"\n")
open(f"{OUT}/todos-os-projetos.md","w").write("# Inteiro teor — Projetos de Lei sobre proteção às mulheres em tramitação (São Paulo/SP)\n\n"+"\n\n---\n\n".join(tudo))
import collections; print(collections.Counter(l.rsplit("|",2)[-2].strip() for l in indice))
