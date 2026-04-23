
import base64, json, os, io, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── PARTE 1: MERGE KMZ ─────────────────────────────────────────────────────
sandbox = r"\\wsl.localhost\Ubuntu\sessions\clever-tender-heisenberg\mnt\uploads"
if not os.path.exists(sandbox):
    # Tenta path alternativo (Linux sandbox via rede)
    sandbox = "C:\Users\carlo\AppData\Roaming\Claude\local-agent-mode-sessions\17f18a35-cc2a-426e-823f-0e3eec6c8ced\23024e89-2e3d-437d-b54e-853347be4ee9\local_e7dc73a9-5d4b-47ed-bd13-efe085f8f722\uploads"

kmz_files = [
    "cantro-423237a8.kmz",
    "cajueiros-350a0806.kmz",
    "imbetiba-83465d90.kmz",
    "alto dos cajueiros-bbf470df.kmz",
    "praia do campista-bdaeb224.kmz",
    "cavaleiros-e0d5ccf5.kmz",
    "morada das garças-ebbf4100.kmz",
]

b64_list = []
for kmz_name in kmz_files:
    kmz_path = os.path.join(sandbox, kmz_name)
    if os.path.exists(kmz_path):
        with open(kmz_path, "rb") as f:
            data = f.read()
        b64_list.append(base64.b64encode(data).decode("utf-8"))
        print(f"  ✅ {kmz_name} ({len(data)} bytes → {len(b64_list[-1])} b64)")
    else:
        print(f"  ❌ NÃO ENCONTRADO: {kmz_path}")

if len(b64_list) == 0:
    print("ERRO: nenhum KMZ encontrado. Verifique o caminho do sandbox.")
    sys.exit(1)

payload = json.dumps(b64_list)
drive_config = r"G:\Meu Drive\CEREBRO_CLAUDE_BRASIL_LIMPO\04_PROJETOS\MACAE_RJ\_config\area_atuacao.kmz.b64"
with open(drive_config, "w", encoding="utf-8") as f:
    f.write(payload)
print(f"\n🗺️  {len(b64_list)} KMZ mesclados → {drive_config}")
print(f"   Tamanho total: {len(payload)} chars\n")

# ── PARTE 2: WATERMARK LOGO NAS FOTOS ─────────────────────────────────────
logo_path = os.path.join(sandbox, "cantro-423237a8.kmz")  # placeholder — será substituído
# Logo é a imagem PNG enviada
logo_candidates = [
    os.path.join(sandbox, f) for f in os.listdir(sandbox) if f.lower().endswith(".png")
]
if not logo_candidates:
    print("⚠️  Logo PNG não encontrado no sandbox. Pulando watermark.")
    sys.exit(0)

logo_src = logo_candidates[0]
print(f"🖼️  Logo: {logo_src}")

# Carrega logo e reduz para tamanho de stamp
logo_orig = Image.open(logo_src).convert("RGBA")
STAMP_SIZE = 160  # px — largura do stamp na foto
ratio = STAMP_SIZE / logo_orig.width
logo_stamp = logo_orig.resize(
    (STAMP_SIZE, int(logo_orig.height * ratio)), Image.LANCZOS
)

# Adiciona transparência ao stamp (50%)
r, g, b, a = logo_stamp.split()
a = a.point(lambda x: int(x * 0.55))
logo_stamp.putalpha(a)

# Processa todos os pontos JSON de Macaé
base_dir = Path(r"G:\Meu Drive\CEREBRO_CLAUDE_BRASIL_LIMPO\04_PROJETOS\MACAE_RJ\cadernos_campo")
json_files = list(base_dir.rglob("*.json"))
print(f"\n📍 {len(json_files)} arquivos de ponto encontrados")

ok = 0; skip = 0; err = 0
for jf in json_files:
    try:
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Suporte a objeto único ou array (pega o primeiro com imagem)
        if isinstance(data, list):
            items = data
        else:
            items = [data]

        modified = False
        for item in items:
            if not isinstance(item, dict) or not item.get("image_b64"):
                skip += 1
                continue

            # Decodifica imagem
            img_bytes = base64.b64decode(item["image_b64"])
            img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

            # Posiciona stamp no canto inferior direito com margem 12px
            margin = 12
            x = img.width - logo_stamp.width - margin
            y = img.height - logo_stamp.height - margin
            composite = Image.new("RGBA", img.size)
            composite.paste(img, (0, 0))
            composite.paste(logo_stamp, (x, y), logo_stamp)

            # Converte de volta para JPEG
            final = composite.convert("RGB")
            buf = io.BytesIO()
            final.save(buf, format="JPEG", quality=82)
            item["image_b64"] = base64.b64encode(buf.getvalue()).decode("utf-8")
            modified = True
            ok += 1

        if modified:
            with open(jf, "w", encoding="utf-8") as f:
                if isinstance(data, list):
                    json.dump(items, f, ensure_ascii=False)
                else:
                    json.dump(items[0], f, ensure_ascii=False)

    except Exception as e:
        print(f"  ⚠️  Erro em {jf.name}: {e}")
        err += 1

print(f"\n✅ Watermark concluído:")
print(f"   Fotos marcadas: {ok}")
print(f"   Sem imagem (puladas): {skip}")
print(f"   Erros: {err}")
