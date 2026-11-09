import json, collections, re
r=json.load(open("resultado.json"))
inc,exc=r["incluidos"],r["excluidos"]
def arq(p):
    n,a=p.split()[1].split("/"); return f"inteiro-teor/PL-{int(n):04d}-{a}.md"
def curta(e,n=170): e=re.sub(r"\s+"," ",e).strip(); return e if len(e)<=n else e[:n].rsplit(" ",1)[0]+"…"
temas=[t for t,_ in collections.Counter(x["Tema"] for x in inc+exc).most_common()]
L=["# Guia para produção legislativa — Proteção às mulheres (Município de São Paulo)","",
"Este guia cruza os **projetos em tramitação**, as **leis já aprovadas** e os **projetos barrados por ilegalidade/inconstitucionalidade** na Câmara Municipal de São Paulo, por tema. O objetivo é ajudar a redigir proposições novas que **não sejam apensadas** a projetos já existentes e que **não esbarrem na CCJ**.","",
"Fonte: SPLegis (dados abertos e fichas oficiais), levantamento de 09/11/2026. Os critérios estão na aba *Leia-me* da planilha `SPLegis-Mulheres-Projetos-de-Lei.xlsx`.","",
"## 1. Como evitar o apensamento","",
"- Projetos que tratam de matéria idêntica ou conexa à de outro já em tramitação costumam ser anexados (apensados) ao mais antigo. Antes de protocolar, **procure no tema correspondente abaixo** se já existe projeto em tramitação com o mesmo objeto e leia o inteiro teor na pasta `inteiro-teor/`.",
"- Se a ideia já existe, as alternativas são: (a) apresentar **emenda ou substitutivo** ao projeto em tramitação; (b) buscar **coautoria**; (c) delimitar um **objeto claramente distinto** (público, instrumento ou território diferentes) e explicitar essa diferença na justificativa.",
"- Se o tema já virou **lei**, prefira um projeto que **altere a lei existente** (\"Altera a Lei nº ...\") em vez de criar uma norma paralela.","",
"## 2. Como reduzir o risco de inconstitucionalidade","",
"Os motivos mais comuns de parecer contrário da CCJ em projetos de iniciativa parlamentar costumam ser:","",
"1. **Vício de iniciativa (reserva do Executivo).** A Lei Orgânica do Município (art. 37, § 2º) reserva ao Prefeito a iniciativa de leis sobre cargos e servidores, organização administrativa, serviços públicos e matéria orçamentária. Projetos que **criam órgãos, secretarias, cargos, programas com estrutura própria ou atribuições novas para órgãos do Executivo** tendem a ser barrados. *Confira a redação vigente da LOM.*",
"2. **Tema 917 do STF (ARE 878.911).** \"Não usurpa competência privativa do Chefe do Poder Executivo lei que, embora crie despesa para a Administração, não trata da sua estrutura ou da atribuição de seus órgãos nem do regime jurídico de servidores públicos.\" Redija **diretrizes, direitos e deveres gerais**, sem desenhar a estrutura administrativa nem atribuir tarefas a secretarias específicas.",
"3. **Competência da União (CF, art. 22).** Direito penal, civil, processual e do trabalho são privativos da União. Evite criar crimes ou penas, alterar regras da Lei Maria da Penha ou do Código Penal, ou impor obrigações trabalhistas a empregadores privados.",
"4. **Interesse local e competência suplementar (CF, art. 30, I e II).** Fundamente o projeto no interesse local e na suplementação da legislação federal e estadual, como a Lei nº 11.340/2006 (Maria da Penha) e a Lei nº 14.188/2021.",
"5. **Leis \"autorizativas\".** Projetos que apenas \"autorizam o Executivo\" a fazer algo que ele já pode fazer costumam ser considerados inócuos ou inconstitucionais. Prefira estabelecer diretrizes de política pública.",
"6. **Datas comemorativas e campanhas** costumam passar com mais facilidade, mas confira se a data já não consta da Lei nº 14.485/2007 (calendário oficial).","",
"> Estas orientações são gerais e não substituem a leitura dos pareceres da CCJ de cada caso, disponíveis nas fichas do SPLegis (links na planilha).","",
"## 3. Panorama por tema","",
"| Tema | Em tramitação | Viraram lei | Barrados (ilegalidade/inconst.) | Apensados |","|---|---|---|---|---|"]
def cnt(t):
    em=sum(1 for x in inc if x["Tema"]==t and x["Situação"]=="Em tramitação")
    lei=sum(1 for x in inc if x["Tema"]==t and x["Lei gerada"])
    il=sum(1 for x in exc if x["Tema"]==t and re.search("ilegal",x["Motivo da exclusão"],re.I))
    ap=sum(1 for x in exc if x["Tema"]==t and re.search("apens|igual teor",x["Motivo da exclusão"],re.I))
    return em,lei,il,ap
for t in temas: L.append(f"| [{t}](#{re.sub(r'[^a-z0-9à-ú -]','',t.lower()).replace(' ','-')}) | "+" | ".join(map(str,cnt(t)))+" |")
L.append("")
for t in temas:
    L+=[f"### {t}",""]
    em=[x for x in inc if x["Tema"]==t and x["Situação"]=="Em tramitação"]
    lei=[x for x in inc if x["Tema"]==t and x["Lei gerada"]]
    il=[x for x in exc if x["Tema"]==t and re.search("ilegal",x["Motivo da exclusão"],re.I)]
    if em:
        L+=["**Em tramitação (um projeto novo com o mesmo objeto seria apensado a estes):**",""]
        L+=[f"- [{x['Projeto']}]({arq(x['Projeto'])}) — {curta(x['Ementa'])} *(CCJ: {x['Parecer CCJ']})*" for x in em]; L.append("")
    if lei:
        L+=["**Já viraram lei (prefira propor alteração da lei existente):**",""]
        L+=[f"- {x['Projeto']} → **{x['Lei gerada']}** — {curta(x['Ementa'])}" for x in lei]; L.append("")
    if il:
        L+=["**Barrados por ilegalidade/inconstitucionalidade (evite repetir o modelo; leia o parecer na ficha):**",""]
        L+=[f"- [{x['Projeto']}]({x['Link SPLegis']}) — {curta(x['Ementa'])}" for x in il]; L.append("")
open("/home/user/splegis-animal/pesquisa-mulheres/GUIA-PRODUCAO-LEGISLATIVA.md","w").write("\n".join(L)+"\n")
print(len(L))
