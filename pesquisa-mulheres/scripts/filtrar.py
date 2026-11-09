import json, glob, re, unicodedata, collections
def norm(t): return unicodedata.normalize("NFD", t or "").encode("ascii","ignore").decode().upper()
POS = re.compile(r"\b(MULHER(ES)?|FEMININ[OA]S?|FEMINICIDIO\w*|FEMICIDIO|MARIA DA PENHA|VIOLENCIA DOMESTICA|VIOLENCIA DE GENERO|GENERO|MISOGIN\w*|ASSEDIO\w*|IMPORTUNACAO SEXUAL|ESTUPRO\w*|VIOLENCIA SEXUAL|ABUSO SEXUAL|MENINAS?|GESTANTES?|PARTURIENTES?|PUERPER\w*|MATERN\w*|LACTANTES?|AMAMENTA\w*|ALEITAMENTO|ABORT\w*|VIOLENCIA OBSTETRICA|DOULAS?|MENSTRUA\w*|ABSORVENTES?|DIGNIDADE MENSTRUAL|MACHIS\w*|SEXIS\w*|EQUIDADE|IGUALDADE (DE GENERO|ENTRE HOMENS E MULHERES)|VITIMAS? DE VIOLENCIA|CASA ABRIGO|DELEGACIA DA MULHER|PATRULHA MARIA DA PENHA|SORORIDADE|EMPREENDEDORAS?|MAES|MAE ATIPICA|MAE SOLO)\b")
res=[]
for f in sorted(glob.glob("dados/*.json")):
    for x in json.load(open(f)):
        t=norm(x["ementa"])+" | "+norm(" | ".join(x.get("assuntos") or []))
        h=sorted(set(m.group(0) for m in POS.finditer(t)))
        if h: x["termos"]=h; res.append(x)
json.dump(res,open("candidatos.json","w"),ensure_ascii=False)
print(len(res)); print(collections.Counter(t for x in res for t in x["termos"]).most_common(50))
