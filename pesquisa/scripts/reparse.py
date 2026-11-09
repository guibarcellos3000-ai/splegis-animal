import json, glob, re, concurrent.futures as cf
from ficha import get, txt
alvo=[]
for f in glob.glob("fichas/*.json"):
    d=json.load(open(f))
    if any(re.search(r"ILEGAL|INCONST|APENS", p["resultado"]) for p in d.get("pareceres",[])): alvo.append(f)
def proc(f):
    d=json.load(open(f))
    t=txt(get("/Pesquisa/DetailsDetalhado/"+d["id"]))
    blocos=[]
    for p in re.split(r"Encaminhamento \([\d.]+\) Comissão ", t)[1:]:
        sig=p.split(" ")[0]
        par=re.findall(r"Parecer Número (\d+ / \d+) , apresentado em: ([\d/]+).*?Conclusão (.*?) (?=Publicação|Votos|Observação|Relatório|Parecer Número|$)", p)
        rel=re.findall(r"Relatório( Retirado)?(?: do\(a\) Relator\(a\))?(?: - Voto Vencedor)? Relatório Número (\d+ / \d+).*?Conclusão (.*?) (?=Publicação|Votos|Observação|Relatório|Parecer Número|$)", p)
        blocos.append({"comissao":sig,"pareceres":[{"numero":a,"data":b,"conclusao":c} for a,b,c in par],
                       "relatorios":[{"retirado":bool(r),"numero":n,"conclusao":c} for r,n,c in rel]})
    d["ccj_detalhe"]=[b for b in blocos if b["comissao"]=="CCJ"]
    json.dump(d,open(f,"w"),ensure_ascii=False)
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(proc, alvo))
print(len(alvo))
