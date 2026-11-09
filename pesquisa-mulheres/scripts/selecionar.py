# Seleção final dos PLs sobre proteção às mulheres (revisão manual documentada aqui)
import json
c=json.load(open("candidatos.json")); k=json.load(open("classes.json"))
# falsos positivos entre os automáticos (ementa com termo forte, mas fora do tema)
EXCL_AUTO={46,53,55,133,276,388,611,776,782,711,920,1089,1184,1394,1512,1523,1538,1412,1301,1338,1369}
# aprovados na revisão manual (termo só nos assuntos indexados)
REV_OK={7,9,11,16,22,23,28,39,41,51,59,61,67,95,104,137,151,167,188,198,203,205,208,215,232,248,253,271,273,274,286,290,298,317,333,
 363,364,371,374,381,383,385,408,447,469,473,477,510,517,579,580,582,590,634,638,666,686,690,727,816,819,823,824,825,848,861,880,883,
 982,996,997,1006,1013,1015,1018,1032,1044,1048,1049,1057,1071,1076,1078,1097,1103,1104,1115,1120,1130,1131,1132,1144,1157,1161,1181,
 1190,1192,1194,1199,1213,1223,1245,1251,1262,1282,1283,1284,1321,1353,1359,1374,1397,1398,1405,1408,1430,1434,1445,1458,1474,1476,1519}
sel=[]
for i in k["auto"]:
    if i not in EXCL_AUTO: c[i]["idx"]=i; sel.append(c[i])
for i in k["rev"]:
    if i in REV_OK: c[i]["idx"]=i; sel.append(c[i])
json.dump(sel,open("selecionados.json","w"),ensure_ascii=False)
print(len(sel))
