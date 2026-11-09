import json, re, unicodedata, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

def norm(t): return unicodedata.normalize("NFD", t or "").encode("ascii","ignore").decode().upper()
sel=json.load(open("selecionados.json"))
LINK="https://splegisconsulta.saopaulo.sp.leg.br/Pesquisa/DetailsMateriaTramitacaoLegislativa?tipo=1&numero={n}&ano={a}"

TEMAS=[
 ("Feminicídio e violência doméstica e familiar", r"FEMINICID|FEMICID|MARIA DA PENHA|VIOLENCIA DOMESTICA|VIOLENCIA CONTRA A MULHER|VIOLENCIA CONTRA AS MULHERES|AGRESSOR|MEDIDA PROTETIVA|CASA[S]?[- ]ABRIGO|VICARIA|ORFAOS|SALA LILAS|VITIMAS? DE VIOLENCIA|SITUACAO DE VIOLENCIA|AUXILIO[- ]ALUGUEL|BATEU, PAGOU|LUANA BARBOSA"),
 ("Assédio, importunação e violência sexual", r"ASSEDIO|IMPORTUNACAO|ESTUPRO|VIOLENCIA SEXUAL|ABUSO SEXUAL|MOLESTAMENTO|AGRESSAO SEXUAL|DIGNIDADE SEXUAL|NAO SE CALE|CORPO DE DELITO"),
 ("Segurança no transporte e no espaço urbano", r"TRANSPORTE|ONIBUS|METRO|DESEMBARQUE|PONTO|TAXI|APLICATIVO|ROTAS?|CAMINHOS SEGUROS|CIDADE PARA TODAS|ILUMINAC|BOTAO|SPRAY|DEFESA PESSOAL|PATRULHA|RONDA|GUARDA CIVIL|BARES|RESTAURANTES|CASAS NOTURNAS|ESTADIO|TORCIDA"),
 ("Violência política de gênero e participação", r"VIOLENCIA POLITICA|POLITICA DE GENERO|MULHER NA POLITICA|MANDATO FEMININO|CONSELHOS?|PARTICIPACAO|RESERVA DE VAGAS PARA MULHERES|CARGOS COMISSIONADOS|DIRECAO E CHEFIA|COMPOSICAO"),
 ("Aborto legal, gestação indesejada e nascituro", r"ABORT|INTERRUPCAO DE GRAVIDEZ|INTERRUPCAO DE GESTACAO|GESTACAO INDESEJADA|NASCITURO|PRO-VIDA|VALORIZACAO DA VIDA|ROTA DA VIDA|ENTREGA (VOLUNTARIA|LEGAL)|CRIANCA NAO E MAE"),
 ("Gestação, parto e puerpério", r"GESTANTE|PARTURIENTE|PARTO|PUERPER|PRE-NATAL|OBSTETRIC|DOULA|MATERNIDADE|MORTALIDADE MATERNA|GRAVIDEZ|GRAVIDAS|SAUDE MENTAL MATERNA|LUTO (MATERNO|PERINATAL)|POS-PARTO|LACTANTE|ALEITAMENTO|AMAMENTA|LICENCA[- ]MATERNIDADE|LICENCA GESTANTE|OBSTETRA"),
 ("Saúde da mulher", r"SAUDE DA MULHER|SAUDE INTEGRAL|CANCER|MAMA|MAMOGRAFIA|COLO DO UTERO|CITOPATOLOG|OVARIO|HPV|CLIMATERIO|LIPEDEMA|PLANEJAMENTO FAMILIAR|CONTRACEP|ANTICONCEP|DIU|LAQUEADURA|SAUDE MENTAL|ALCOOLISMO|EXAME|MASTECTOMIA|AREOLA|TROMBOFILIA"),
 ("Dignidade menstrual", r"MENSTRU|ABSORVENTE"),
 ("Mães solo, mães atípicas e cuidado", r"MAES? SOLO|MAES? SOLTEIRA|MAES? ATIPICA|MAE CUIDADORA|CUIDADOS|CRECHE|CHEFES DE FAMILIA|MAES"),
 ("Trabalho, renda e autonomia econômica", r"EMPREG|TRABALH|RENDA|SALARIAL|EQUIDADE DE GENERO NO MERCADO|EMPREENDE|QUALIFICACAO|CAPACITACAO|AUTONOMIA FINANCEIRA|INCENTIVO FISCAL|ISENCAO|IPTU|HABITAC|MORADIA|UNIDADES HABITACIONAIS"),
 ("Equidade de gênero, educação e combate ao machismo", r"EQUIDADE|IGUALDADE|MACHIS|MISOGIN|SEXIS|GENERO|ESCOLA|EDUCAC|ENSINO|MASCULINIDADES|PUBLICIDADE"),
 ("Estrutura institucional (centros, coordenadorias, fundos, conselhos)", r"CENTRO|COORDENADORIA|CASA (DA|DE) MULHER|FUNDO|SECRETARIA|POLITICA MUNICIPAL|PROGRAMA|REDE|OBSERVATORIO|CADASTRO|DOSSIE|ESTATUTO"),
 ("Datas comemorativas e campanhas", r"CALENDARIO|DIA |SEMANA|MES |CAMPANHA|FERIADO"),
]
def tema(e):
    n=norm(e)
    for nome,rx in TEMAS:
        if re.search(rx,n): return nome
    return "Outros temas da proteção às mulheres"

def limpa_par(r):
    r=r or ""
    if r.startswith("Sem parecer"): return "Sem parecer"
    return r.strip()

def ccj(f):
    if "ccj_detalhe" in f:
        pars=[p["conclusao"] for b in f["ccj_detalhe"] for p in b["pareceres"]]
        rels=[r["conclusao"] for b in f["ccj_detalhe"] for r in b["relatorios"] if not r["retirado"]]
        if pars: return pars[-1], pars
        if rels: return "Relatório do relator: "+rels[-1]+" (parecer ainda não votado)", rels
        return "Sem parecer (relatório retirado)", []
    ps=[limpa_par(p["resultado"]) for p in f.get("pareceres",[]) if p["comissao"]=="CCJ"]
    merito=[p for p in ps if re.search(r"LEGALIDADE|INCONSTITUC|FAVOR|CONTR", p) and "VETO" not in p]
    return (merito[-1] if merito else (ps[-1] if ps else "")), ps

def veto(f):
    v=f.get("veto","")
    m=re.findall(r"Veto (Total|Parcial)", v)
    return ("Veto "+m[-1]) if m else ""

def data_br(s):
    try: return datetime.date.fromisoformat(s[:10]).strftime("%d/%m/%Y")
    except: return s or ""

incl=[]; excl=[]
for x in sel:
    f=json.load(open(f"fichas/{x['ano']}-{x['numero']}.json"))
    motivo=(f.get("encerramento_motivo") or ((x.get("encerramento") or {}).get("motivo","")).replace("Encerrado-","")).strip()
    par, todos=ccj(f)
    lei=f.get("lei","").strip()
    row={
      "Projeto": f"PL {x['numero']}/{x['ano']}",
      "Número": x["numero"], "Ano": x["ano"],
      "Apresentação": data_br(x["data"]),
      "Autor(es)": re.sub(r"\s+"," ",f.get("autores","")).strip(),
      "Ementa": re.sub(r"\s+"," ",x["ementa"]).strip(),
      "Tema": tema(x["ementa"]+" "+" ".join(x.get("assuntos") or [])[:0]),
      "Situação": "",
      "Lei gerada": ("Lei nº "+lei.split(" - ")[0]+(" ("+lei.split(" - ")[1]+")" if " - " in lei else "")) if lei else "",
      "Parecer CCJ": par or "Sem parecer",
      "Veto": veto(f),
      "Fase / última tramitação": f.get("fase","") or "",
      "Encerramento": (motivo+(" em "+f.get("encerramento_data") if f.get("encerramento_data") else "")) if motivo else "",
      "Link SPLegis": LINK.format(n=x["numero"],a=x["ano"]),
    }
    nm=norm(motivo); np_=norm(par)
    if "ILEGALIDADE" in nm:
        row["Motivo da exclusão"]="Encerrado por ilegalidade/inconstitucionalidade (art. 79 do Regimento Interno)"; excl.append(row); continue
    if "APENSADO" in nm:
        row["Motivo da exclusão"]="Apensado a outro projeto"; excl.append(row); continue
    if "IGUAL TEOR" in nm:
        row["Motivo da exclusão"]="Igual teor a outro projeto (art. 212 do RI) – tramita anexado ao principal"; excl.append(row); continue
    if "RELATORIO DO RELATOR: APENSAMENTO" in np_:
        row["Motivo da exclusão"]="Relator da CCJ propôs o apensamento a outro projeto"; excl.append(row); continue
    if re.search(r"ILEGALIDADE|INCONSTITUC", np_) and not np_.startswith("RELATORIO") and not lei:
        row["Motivo da exclusão"]="Parecer da CCJ pela ilegalidade/inconstitucionalidade"; excl.append(row); continue
    if lei: sit="Aprovado – virou lei"
    elif "TERMINO DE LEGISLATURA" in nm: sit="Arquivado – fim de legislatura"
    elif "RETIRADO" in nm: sit="Retirado pelo autor"
    elif "VETO TOTAL" in nm: sit="Vetado totalmente (veto mantido)"
    elif "REJEITADO" in nm or "CONTRARIO" in nm: sit="Rejeitado no mérito"
    elif motivo: sit="Encerrado – "+motivo.title()
    else: sit="Em tramitação"
    row["Situação"]=sit
    incl.append(row)

incl.sort(key=lambda r:(-r["Ano"],-r["Número"])); excl.sort(key=lambda r:(-r["Ano"],-r["Número"]))
json.dump({"incluidos":incl,"excluidos":excl},open("resultado.json","w"),ensure_ascii=False,indent=1)

# ---------- Excel ----------
wb=Workbook()
verde="1F6F50"; claro="E6F2EC"
thin=Side(style="thin",color="DFE5E1")
def planilha(ws, linhas, cols, larg, nome_tab):
    ws.append(cols)
    for r in linhas: ws.append([r.get(c,"") for c in cols])
    for i,c in enumerate(cols,1):
        cel=ws.cell(row=1,column=i); cel.font=Font(bold=True,color="FFFFFF"); cel.fill=PatternFill("solid",fgColor=verde)
        cel.alignment=Alignment(vertical="center",wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width=larg.get(c,15)
    li=cols.index("Link SPLegis")+1
    for r in range(2,len(linhas)+2):
        for i in range(1,len(cols)+1):
            ws.cell(row=r,column=i).alignment=Alignment(vertical="top",wrap_text=True)
        cl=ws.cell(row=r,column=li); url=cl.value
        cl.value="Abrir ficha"; cl.hyperlink=url; cl.font=Font(color="1D4B8F",underline="single")
    ws.freeze_panes="B2"
    if linhas:
        t=Table(displayName=nome_tab, ref=f"A1:{get_column_letter(len(cols))}{len(linhas)+1}")
        t.tableStyleInfo=TableStyleInfo(name="TableStyleLight9",showRowStripes=True); ws.add_table(t)
    ws.row_dimensions[1].height=32

larg={"Projeto":13,"Número":8,"Ano":7,"Apresentação":12,"Autor(es)":28,"Ementa":70,"Tema":28,"Situação":24,"Lei gerada":22,"Parecer CCJ":22,"Veto":12,"Fase / última tramitação":28,"Encerramento":28,"Link SPLegis":12,"Motivo da exclusão":40}
cols=["Projeto","Ano","Apresentação","Autor(es)","Ementa","Tema","Situação","Lei gerada","Parecer CCJ","Veto","Fase / última tramitação","Link SPLegis"]

ws=wb.active; ws.title="Leia-me"
import collections
sitc=collections.Counter(r["Situação"] for r in incl); tc=collections.Counter(r["Tema"] for r in incl); ec=collections.Counter(r["Motivo da exclusão"] for r in excl)
L=[["Projetos de Lei sobre proteção às mulheres no Município de São Paulo"],[""],
 ["Fonte","Câmara Municipal de São Paulo – SPLegis (dados abertos splegisws.saopaulo.sp.leg.br e fichas em splegisconsulta.saopaulo.sp.leg.br)"],
 ["Data da coleta",datetime.date.today().strftime("%d/%m/%Y")],
 ["Período pesquisado","Projetos de Lei (PL) apresentados de 1991 a 2026 (todos os disponíveis no SPLegis)"],
 ["Seleção temática","Busca por palavras-chave na ementa e nos assuntos indexados pela Câmara (mulher, feminicídio, Maria da Penha, violência doméstica, assédio, importunação sexual, estupro, gestante, parto, maternidade, aborto, menstruação, gênero, machismo etc.), seguida de revisão manual dos resultados para retirar falsos positivos (ex.: 'gênero alimentício', 'Rua Maestro', nomes de logradouros e projetos só sobre crianças)."],
 ["Fora do recorte temático","Denominação de logradouros, declarações de utilidade pública, projetos voltados apenas a crianças/recém-nascidos (testes neonatais, berçários), pauta LGBTQIA+ sem recorte específico de mulheres, e medidas gerais de acessibilidade em que a gestante é apenas um entre vários grupos citados apenas nos assuntos."],
 ["Critérios de exclusão","1) Encerrados por ilegalidade/inconstitucionalidade (art. 79 do RI); 2) com parecer da CCJ aprovado pela ilegalidade ou inconstitucionalidade (vale o último parecer da CCJ), salvo se viraram lei; 3) apensados a outro projeto ou com proposta de apensamento do relator da CCJ; 4) de igual teor a outro (art. 212 do RI), que tramitam anexados ao principal. Quando há apenas relatório do relator pela ilegalidade, ainda não votado na CCJ, o projeto foi MANTIDO e a situação aparece na coluna 'Parecer CCJ'."],
 ["Observação","Projetos arquivados por fim de legislatura, retirados, vetados ou rejeitados NÃO foram excluídos (não se enquadram nos critérios pedidos), mas estão identificados na coluna 'Situação' – use o filtro para vê-los ou escondê-los."],
 [""],["RESUMO"],["Projetos incluídos",len(incl)],["Projetos excluídos",len(excl)],[""],["Incluídos por situação"]]
L+= [[k,v] for k,v in sitc.most_common()]
L+= [[""],["Incluídos por tema"]]+[[k,v] for k,v in tc.most_common()]
L+= [[""],["Excluídos por motivo"]]+[[k,v] for k,v in ec.most_common()]
L+= [[""],["Como usar","Na aba 'Projetos', clique nas setinhas do cabeçalho para filtrar por Situação, Tema, Ano etc. O link 'Abrir ficha' leva à página oficial do projeto."]]
for l in L: ws.append(l)
ws["A1"].font=Font(bold=True,size=14,color=verde)
for r in ws.iter_rows():
    if r[0].value in ("RESUMO","Incluídos por situação","Incluídos por tema","Excluídos por motivo") or (len(r)>1 and r[1].value not in (None,"") and isinstance(r[1].value,str)):
        r[0].font=Font(bold=True)
    for c in r: c.alignment=Alignment(wrap_text=True,vertical="top")
ws.column_dimensions["A"].width=34; ws.column_dimensions["B"].width=110

planilha(wb.create_sheet("Projetos"), incl, cols, larg, "Projetos")
planilha(wb.create_sheet("Em tramitação"), [r for r in incl if r["Situação"]=="Em tramitação"], cols, larg, "EmTramitacao")
planilha(wb.create_sheet("Excluídos"), excl, ["Projeto","Ano","Autor(es)","Ementa","Motivo da exclusão","Parecer CCJ","Encerramento","Link SPLegis"], larg, "Excluidos")
wb.save("SPLegis-Mulheres-Projetos-de-Lei.xlsx")
print(len(incl), len(excl)); print(sitc); print(ec); print(tc)
