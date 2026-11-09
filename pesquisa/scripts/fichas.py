import json, os, concurrent.futures as cf
from ficha import ficha
sel=json.load(open("selecionados.json"))
os.makedirs("fichas",exist_ok=True)
def f(x):
    out=f"fichas/{x['ano']}-{x['numero']}.json"
    if os.path.exists(out): return
    try: r=ficha(x["numero"],x["ano"])
    except Exception as e: r={"erro":str(e)}
    json.dump(r,open(out,"w"),ensure_ascii=False)
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(f, sel))
print("ok")
