import json,re,unicodedata,collections
def norm(t): return unicodedata.normalize("NFD", t or "").encode("ascii","ignore").decode().upper()
c=json.load(open("candidatos.json"))
FORTE=re.compile(r"\b(MULHER(ES)?|FEMININ[OA]S?|FEMINICIDIO|FEMICIDIO|MARIA DA PENHA|VIOLENCIA DOMESTICA|VIOLENCIA DE GENERO|IGUALDADE DE GENERO|EQUIDADE DE GENERO|MISOGIN\w*|MACHIS\w*|SEXIS\w*|IMPORTUNACAO SEXUAL|VIOLENCIA OBSTETRICA|MENSTRU\w*|ABSORVENTES?|DELEGACIA DA MULHER|ASSEDIO SEXUAL|ESTUPRO\w*|GESTANTES?|PARTURIENTES?|PUERPER\w*|ALEITAMENTO|AMAMENTA\w*|LACTANTES?|DOULAS?|MAES? ATIPICAS?|MAES? SOLO|MAES|ABORT\w*|MENINAS)\b")
EXC=re.compile(r"^\W*(DENOMINA|ALTERA (A )?DENOMINACAO|DA DENOMINACAO|DISPOE SOBRE A DENOMINACAO|OFICIALIZA)|GENEROS? ALIMENTICIOS")
auto=[];rev=[];fora=[]
for i,x in enumerate(c):
    e=norm(x["ementa"])
    if EXC.search(e): fora.append(i); continue
    if FORTE.search(e): auto.append(i)
    else: rev.append(i)
print(len(auto),len(rev),len(fora))
json.dump({"auto":auto,"rev":rev},open("classes.json","w"))
with open("rev.txt","w") as f:
    for i in rev: f.write(f"{i} {c[i]['ano']} {norm(c[i]['ementa']).strip()[:115]} # {','.join(c[i]['termos'])[:30]}\n")
with open("auto.txt","w") as f:
    for i in auto: f.write(f"{i} {c[i]['ano']} {norm(c[i]['ementa']).strip()[:105]}\n")
