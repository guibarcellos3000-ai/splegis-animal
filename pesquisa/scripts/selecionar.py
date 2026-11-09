import json,re,unicodedata
def norm(t): return unicodedata.normalize("NFD", t or "").encode("ascii","ignore").decode().upper()
c=json.load(open("candidatos.json"))
FORTE=re.compile(r"\b(ANIMA(L|IS)|CAES|CACHORR|GATOS\b|FELIN|CANINOS?\b|ZOONOS|CASTRACAO|MAUS[- ]TRATOS|FAUNA|CANIL|GATIL|TRACAO ANIMAL|CARROCEIR|RODEIO|VAQUEJADA|VIVISSEC|EQUIDEO|EQUINO|PROTETOR)")
excl_forte={16,51,53,57,52,112,175,210,218,234,247,303,469,476,507,542,572,573,610,816,838,14,81,86,87,151,154,252,415,445,493,671,390,236,295,135,124}
weak_keep={38,39,46,129,131,182,184,195,200,208,255,257,261,285,294,296,298,308,309,313,314,333,337,340,341,360,361,365,370,374,379,380,387,392,403,408,411,412,414,416,431,435,436,437,439,448,455,459,462,471,472,496,497,499,501,517,529,536,538,545,546,547,558,560,575,579,580,583,585,595,602,603,605,626,627,629,630,634,642,651,674,676,678,688,697,713,727,738,743,750,756,759,766,773,774,784}
sel=[]
for i,x in enumerate(c):
    forte=bool(FORTE.search(norm(x["ementa"])))
    if (forte and i not in excl_forte) or (not forte and i in weak_keep):
        x["idx"]=i; sel.append(x)
json.dump(sel,open("selecionados.json","w"),ensure_ascii=False)
print(len(sel))
