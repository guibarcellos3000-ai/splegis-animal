import json, urllib.request, concurrent.futures as cf, os, sys
B="https://splegisws.saopaulo.sp.leg.br/ws/ws2.asmx"
def get(op, ano, extra=""):
    for t in range(4):
        try:
            with urllib.request.urlopen(f"{B}/{op}?{'Ano' if op=='ProjetosPorAnoJSON' else 'ano'}={ano}{extra}", timeout=300) as r:
                return json.load(r)
        except Exception as e:
            err=e
    print("FALHA",op,ano,err,flush=True); return []
def ano(y):
    out=f"dados/{y}.json"
    if os.path.exists(out): return
    pa=[x for x in get("ProjetosPorAnoJSON",y) if x.get("tipo")=="PL"]
    asx={x["chave"]:[s["texto"] for s in (x.get("assuntos") or [])] for x in get("ProjetosAssuntosJSON",y,"&tipo=1") if x.get("tipo")=="PL"}
    enc={x["numero"]:x for x in get("ProjetosEncerradosJSON",y) if x.get("tipo")=="PL"}
    for x in pa:
        x["assuntos"]=asx.get(x["chave"],[])
        e=enc.get(x["numero"]); x["encerramento"]=e and {"motivo":e["motivo"],"data":e["encerramento"]}
    json.dump(pa,open(out,"w"),ensure_ascii=False)
    print(y,len(pa),flush=True)
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(ano, range(int(sys.argv[1]),int(sys.argv[2])+1)))
