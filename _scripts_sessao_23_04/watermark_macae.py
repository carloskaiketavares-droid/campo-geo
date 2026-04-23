
import base64, json, io, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Logo Macae Prefeitura (PNG inline do chat — copiado como base64) ───────
# Como o logo nao ficou disponivel como arquivo, vamos criar um stamp
# profissional com PIL: brasao circular + "PREFEITURA DE MACAE" em azul.
# Quando quiser usar o PNG real, basta trocar logo_img abaixo.

def create_macae_stamp(size=180):
    """Cria stamp SVG-style: circulo azul com texto 'Prefeitura / Macae'."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Circulo externo azul
    margin = 4
    draw.ellipse([margin, margin, size-margin, size-margin],
                 outline=(0, 102, 179, 230), width=6)
    
    # Circulo interno
    draw.ellipse([margin+8, margin+8, size-margin-8, size-margin-8],
                 outline=(0, 102, 179, 150), width=2)
    
    # Texto central
    cx, cy = size // 2, size // 2
    
    try:
        font_lg = ImageFont.truetype("arial.ttf", 22)
        font_sm = ImageFont.truetype("arial.ttf", 14)
    except:
        font_lg = ImageFont.load_default()
        font_sm = font_lg
    
    # "Macaé" grande
    draw.text((cx, cy - 14), "Macaé", fill=(0, 102, 179, 220),
              font=font_lg, anchor="mm")
    # "PREFEITURA" menor
    draw.text((cx, cy + 14), "PREFEITURA", fill=(90, 90, 90, 200),
              font=font_sm, anchor="mm")
    # Linha separadora
    draw.line([(cx - 38, cy + 2), (cx + 38, cy + 2)], fill=(0, 102, 179, 120), width=1)
    
    return img

logo_stamp = create_macae_stamp(180)

# ── Processa fotos ─────────────────────────────────────────────────────────
base_dir = Path(r"G:\Meu Drive\CEREBRO_CLAUDE_BRASIL_LIMPO\04_PROJETOS\MACAE_RJ\cadernos_campo")
json_files = list(base_dir.rglob("*.json"))
print(f"Encontrados: {len(json_files)} arquivos de ponto")

ok = 0; skip = 0; err = 0
STAMP_W = 180  # px na foto final

for jf in json_files:
    try:
        with open(jf, "r", encoding="utf-8") as f:
            raw = f.read()
        data = json.loads(raw)
        
        item = data if isinstance(data, dict) else (data[0] if data else None)
        if not item or not item.get("image_b64"):
            skip += 1
            continue
        
        # Decodifica imagem
        img_bytes = base64.b64decode(item["image_b64"])
        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        
        # Redimensiona stamp proporcional ao tamanho da foto
        stamp_size = max(120, min(STAMP_W, img.width // 5))
        ratio = stamp_size / logo_stamp.width
        stamp = logo_stamp.resize(
            (stamp_size, int(logo_stamp.height * ratio)), Image.LANCZOS
        )
        
        # Posiciona no canto inferior direito com margem
        margin = 14
        x = img.width - stamp.width - margin
        y = img.height - stamp.height - margin
        
        composite = Image.new("RGBA", img.size)
        composite.paste(img, (0, 0))
        composite.paste(stamp, (x, y), stamp)
        
        # Salva como JPEG
        final = composite.convert("RGB")
        buf = io.BytesIO()
        final.save(buf, format="JPEG", quality=83)
        item["image_b64"] = base64.b64encode(buf.getvalue()).decode("utf-8")
        
        # Grava de volta
        if isinstance(data, list):
            data[0] = item
            out = data
        else:
            out = item
        
        with open(jf, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False)
        
        ok += 1
        if ok % 20 == 0:
            print(f"  Progresso: {ok}/{len(json_files)}...")
    
    except Exception as e:
        print(f"  ERRO em {jf.name}: {e}")
        err += 1

print(f"\n=== WATERMARK CONCLUIDO ===")
print(f"Fotos marcadas : {ok}")
print(f"Sem foto (skip): {skip}")
print(f"Erros          : {err}")
