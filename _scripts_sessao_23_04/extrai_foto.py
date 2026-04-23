import json, base64, os, glob

# Procura JSONs com image_b64
base = r"G:\Meu Drive\CEREBRO_CLAUDE_BRASIL_LIMPO\04_PROJETOS\MACAE_RJ\cadernos_campo"
found = None
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".json") and f != "pontos_enviados.json":
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                if isinstance(data, list):
                    for item in data:
                        if item.get("image_b64"):
                            found = (path, item)
                            break
                elif isinstance(data, dict) and data.get("image_b64"):
                    found = (path, data)
                if found:
                    break
            except:
                pass
    if found:
        break

if found:
    path, item = found
    b64 = item["image_b64"]
    if "," in b64:
        b64 = b64.split(",", 1)[1]
    img_bytes = base64.b64decode(b64)
    out = r"C:\Users\carlo\exemplo_macae.jpg"
    with open(out, "wb") as fh:
        fh.write(img_bytes)
    print(f"OK: {item.get('name','?')} | bairro={item.get('bairro','?')} | {len(img_bytes)} bytes -> {out}")
else:
    print("Nenhuma foto encontrada")
