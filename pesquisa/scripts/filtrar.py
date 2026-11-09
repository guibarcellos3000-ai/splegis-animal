import json, glob, re, unicodedata
def norm(t): return unicodedata.normalize("NFD", t or "").encode("ascii","ignore").decode().upper()
POS = re.compile(r"\b(ANIMA(L|IS)|FAUNA|CAES|(?<=DO )CAO|(?<=UM )CAO|CAO[- ]GUIA|CACHORR\w*|GAT[OA]S?|FELIN\w*|CANINOS?|CANINAS?|PETS?|VETERINAR\w*|ZOONOS\w*|CASTRAC\w*|ESTERILIZAC\w* (DE|DOS|EM) (CAES|GATOS|ANIMAIS)|EQUIN\w*|EQUIDEOS?|CAVALOS?|CARROCAS?|CARROCEIROS?|TRACAO ANIMAL|RODEIOS?|VAQUEJADA|MAUS[- ]TRATOS|PROTETOR(ES|A|AS)? (DE|DOS) ANIMAIS|AVES|PASSAROS?|PASSERIFORMES|SILVESTRES?|BIOTERIO|VIVISSECCAO|COBAIAS?|FOIE GRAS|CRUELDADE|BEM[- ]ESTAR ANIMAL|TUTOR(ES)? DE|MICROCHIP\w*|CANIL|GATIL|ABRIGO(S)? DE ANIMAIS|ABELHAS?|POMBOS?|PRIMATAS?|MACACOS?|CAPIVARAS?|ZOOLOGIC\w*|AQUARIOS?|CIRCOS? (COM|DE) ANIMAIS)\b")
NEG = re.compile(r"\b(ANIMAC\w*|ANIMADOR\w*)\b")
def tema(x):
    ementa, ass = norm(x["ementa"]), norm(" | ".join(x.get("assuntos") or []))
    hits = set(m.group(0) for m in POS.finditer(ementa + " | " + ass))
    return sorted(hits)
res=[]
for f in sorted(glob.glob("dados/*.json")):
    for x in json.load(open(f)):
        h=tema(x)
        if h: x["termos"]=h; res.append(x)
json.dump(res,open("candidatos.json","w"),ensure_ascii=False,indent=0)
print(len(res))
import collections; print(collections.Counter(t for x in res for t in x["termos"]).most_common(60))
