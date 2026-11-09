import json, re, os, html, subprocess, tempfile, urllib.request, concurrent.futures as cf, glob
S="https://splegisconsulta.saopaulo.sp.leg.br"
def get(u, binario=False):
    for i in range(4):
        try:
            with urllib.request.urlopen(S+u, timeout=180) as r:
                b=r.read(); return b if binario else b.decode("utf-8","replace")
        except Exception as e: err=e
    raise err
r=json.load(open("resultado.json"))
alvo=[x for x in r["incluidos"] if x["Situação"]=="Em tramitação"]
os.makedirs("ocr",exist_ok=True)
def docs(id_):
    h=get(f"/Pesquisa/DetailsDetalhado/{id_}")
    return [(m.group(1), html.unescape(re.sub(r"<[^>]+>","",m.group(2))).strip())
            for m in re.finditer(r'href="/Home/AbrirDocumento\?pI[Dd]=(\d+)"[^>]*>(.*?)</a>', h, re.S)]
def ocr_pdf(pdf, maxp=15):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm","-r","200","-gray","-png","-l",str(maxp),pdf,f"{d}/p"],stderr=subprocess.DEVNULL)
        out=[]
        for png in sorted(glob.glob(f"{d}/p-*.png"), key=lambda s:int(re.findall(r"-(\d+)\.png",s)[0])):
            # recorta cabeçalho de autuação (topo) e carimbo de assinatura (margem direita)
            from PIL import Image
            im=Image.open(png); w,hh=im.size
            im.crop((0,int(hh*0.055),int(w*0.905),hh)).save(png)
            t=subprocess.run(["tesseract",png,"-","-l","por","--psm","4"],capture_output=True,text=True).stdout
            out.append(t)
        return out
def proc(x):
    n,a=x["Projeto"].split()[1].split("/")
    dest=f"ocr/{a}-{n}.json"
    if os.path.exists(dest): return
    f=json.load(open(f"fichas/{a}-{n}.json"))
    res={"projeto":x["Projeto"]}
    try:
        ds=docs(f["id"]); res["documentos"]=ds
        NAO=r"^(PEDIDO DE INFORMA|PUBLICA|DESIGNA|Termo de convers|PESQUISA E AN|RECEBIMENTO|Despacho)"
        ti=[d for d in ds if not re.search(NAO,d[1],re.I)]
        res["substitutivos"]=[d for d in ds if re.search(r"substitutivo",d[1],re.I)]
        if not ti: res["erro"]="texto inicial não encontrado"
        else:
            pid=ti[0][0]; res["pid"]=pid
            pdf=f"pdf/{a}-{n}.pdf"
            open(pdf,"wb").write(get(f"/Home/TransmitirDocumento?pId={pid}&digital=1",True))
            res["inicial"]=not re.match(r"^PL\d{5}-\d{4}\.PDF$",ti[0][1],re.I); res["paginas"]=ocr_pdf(pdf, 15 if res["inicial"] else 7)
            # se o documento escolhido não contém o texto do projeto, tenta os próximos
            for alt in ti[1:3]:
                if "DECRETA" in "\n".join(res["paginas"]).upper(): break
                pdf2=f"pdf/{a}-{n}-{alt[0]}.pdf"
                open(pdf2,"wb").write(get(f"/Home/TransmitirDocumento?pId={alt[0]}&digital=1",True))
                pg=ocr_pdf(pdf2, 15)
                if "DECRETA" in "\n".join(pg).upper():
                    res["pid"]=alt[0]; res["paginas"]=pg; res["inicial"]=not re.match(r"^PL\d{5}-\d{4}\.PDF$",alt[1],re.I)
    except Exception as e: res["erro"]=str(e)
    json.dump(res,open(dest,"w"),ensure_ascii=False)
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(proc, alvo))
print("ok", len(alvo))
