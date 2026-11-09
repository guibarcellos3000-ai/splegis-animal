import re, html, urllib.request, sys, json
S="https://splegisconsulta.saopaulo.sp.leg.br"
def get(u):
    for i in range(4):
        try:
            with urllib.request.urlopen(S+u, timeout=120) as r: return r.read().decode("utf-8","replace")
        except Exception as e: err=e
    raise err
def txt(h):
    h=re.sub(r"<script.*?</script>|<style.*?</style>","",h,flags=re.S)
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",h))).strip()
def campo(t, ini, fim):
    m=re.search(re.escape(ini)+r"\s*(.*?)\s*"+fim, t)
    return m.group(1).strip() if m else ""
def ficha(numero, ano):
    d=get(f"/Pesquisa/DetailsMateriaTramitacaoLegislativa?tipo=1&numero={numero}&ano={ano}")
    m=re.search(r"/Pesquisa/DetailsDetalhado/(\d+)", d)
    if not m: return {"erro":"sem ficha"}
    h=get(m.group(0)); t=txt(h)
    r={"id":m.group(1)}
    r["lei"]=campo(t,"Lei Municipal","Obs. promulgação")
    r["veto"]=campo(t,"Veto","Autores")
    r["autores"]=campo(t,"Autores","(Assinaturas de Apoiamento|Apresentado em)")
    r["encerramento_data"]=campo(t,"Data de Encerramento","Motivo do Encerramento")
    r["encerramento_motivo"]=campo(t,"Motivo do Encerramento","Histórico de Encerramento")
    r["fase"]=campo(t,"Fase inferida pelo SPLegis","Fase cadastrada")
    r["apensados_ao"]=campo(t,"Proc. apensados","Matérias Anexadas")
    # pareceres por comissão
    par=[]
    partes=re.split(r"Encaminhamento \([\d.]+\) Comissão ", t)[1:]
    for p in partes:
        sig=p.split(" ")[0]
        c=re.search(r"Conclusão (.*?) (Publicação|Votos|Observação|Autor)", p) or re.search(r"Resultado (.*?) Observação", p)
        par.append({"comissao":sig,"resultado":(c.group(1) if c else "")[:120]})
    r["pareceres"]=par
    r["ultima"]=campo(t,"Última Tramitação/Evento Data e hora Área/Ação Motivo Observação de envio Observação de recebimento","Histórico de Tramitações")[:200]
    return r
if __name__=="__main__":
    print(json.dumps(ficha(sys.argv[1],sys.argv[2]),ensure_ascii=False,indent=1))
