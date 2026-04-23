
import re

path = r"C:\Users\carlo\BRASIL_LIMPO\Scripts\campo-geo\index.html"

with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# --- Patch 1: titulo v5.9.8 -> v5.9.9 ---
html = html.replace("<title>Campo GEO v5.9.8</title>", "<title>Campo GEO v5.9.9</title>", 1)

# --- Patch 2: substituir bloco de auto-publish por bloco com append ---
OLD_BLOCK = '''    // v5.9.8: Admin auto-publica TODOS os KMZ
    if (isAdm && allB64.length > 0 && S.project) {
        try {
            var payload = allB64.length === 1 ? allB64[0] : JSON.stringify(allB64);
            var res = await apiPost({ action: "saveKMZ", project: S.project.folder, content: payload });
            if (res && res.success) log("\\ud83d\\udce4 " + allB64.length + " KMZ publicado(s) \\u2014 operadores receberao ao abrir o projeto", "ok");
            else log("\\u26a0\\ufe0f Auto-publish KMZ falhou: " + ((res&&res.error)||"?"), "err");
        } catch(e) { log("\\u26a0\\ufe0f Auto-publish KMZ falhou: " + e.message, "err"); }
    }'''

NEW_BLOCK = '''    // v5.9.9: Admin auto-publica com APPEND — KMZ anteriores sao preservados
    if (isAdm && allB64.length > 0 && S.project) {
        try {
            // Busca KMZs ja existentes no backend para acumular
            var existingB64 = [];
            try {
                var existRes = await apiPost({ action: "getKMZ", project: S.project.folder });
                if (existRes && existRes.success && existRes.content) {
                    try { var ep = JSON.parse(existRes.content); existingB64 = Array.isArray(ep) ? ep : [existRes.content]; }
                    catch(e2) { existingB64 = [existRes.content]; }
                }
            } catch(e3) { /* sem KMZ previo */ }
            // Mescla: existentes + novos
            var merged = existingB64.concat(allB64);
            var payload = merged.length === 1 ? merged[0] : JSON.stringify(merged);
            var res = await apiPost({ action: "saveKMZ", project: S.project.folder, content: payload });
            if (res && res.success) {
                var msg = "\\ud83d\\udce4 " + merged.length + " KMZ(s) publicado(s)";
                if (existingB64.length > 0) msg += " (" + existingB64.length + " anteriores + " + allB64.length + " novo(s))";
                log(msg + " \\u2014 operadores receberao ao sincronizar", "ok");
            } else log("\\u26a0\\ufe0f Auto-publish KMZ falhou: " + ((res&&res.error)||"?"), "err");
        } catch(e) { log("\\u26a0\\ufe0f Auto-publish KMZ falhou: " + e.message, "err"); }
    }'''

if OLD_BLOCK in html:
    html = html.replace(OLD_BLOCK, NEW_BLOCK, 1)
    print("OK: bloco de publish substituido com logica de APPEND")
else:
    print("ERRO: bloco OLD_BLOCK nao encontrado — verificar manualmente")
    # Mostra contexto para debug
    idx = html.find("v5.9.8: Admin auto-publica")
    if idx >= 0:
        print("Encontrou referencia em:", idx)
        print(repr(html[idx:idx+400]))
    import sys; sys.exit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("Arquivo salvo:", path)
