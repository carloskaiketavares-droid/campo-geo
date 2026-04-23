import re

path = r'C:\Users\carlo\BRASIL_LIMPO\Scripts\campo-geo\index.html'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content_lf = content.replace('\r\n', '\n')

# P1a
old1 = '    var lastB64 = null;\n    if (isAdm && S.project) {\n        try { var buf = await files[files.length - 1].arrayBuffer(); lastB64 = arrayBufferToBase64(buf); } catch(e) {}\n    }'
new1 = '    var allB64 = []; // v5.9.8: coleta TODOS os KMZ\n    if (isAdm && S.project) {\n        for (var ai = 0; ai < files.length; ai++) {\n            try { var bufAi = await files[ai].arrayBuffer(); allB64.push(arrayBufferToBase64(bufAi)); } catch(e) {}\n        }\n    }'
print('P1a OK' if old1 in content_lf else 'P1a FALHOU idx=' + str(content_lf.find('var lastB64 = null;')))
if old1 in content_lf: content_lf = content_lf.replace(old1, new1)

# P1b
old2 = '    // v5.8: Admin auto-publica KMZ no backend p/ todos operadores receberem\n    if (isAdm && lastB64 && S.project) {'
new2 = '    // v5.9.8: Admin auto-publica TODOS os KMZ\n    if (isAdm && allB64.length > 0 && S.project) {'
print('P1b OK' if old2 in content_lf else 'P1b FALHOU idx=' + str(content_lf.find('v5.8: Admin auto-publica')))
if old2 in content_lf: content_lf = content_lf.replace(old2, new2)

# P1c: substituir content: lastB64 -> content: payload (com linha de payload antes)
old3 = '            var res = await apiPost({ action: "saveKMZ", project: S.project.folder, content: lastB64 });'
new3 = '            var payload = allB64.length === 1 ? allB64[0] : JSON.stringify(allB64);\n            var res = await apiPost({ action: "saveKMZ", project: S.project.folder, content: payload });'
print('P1c OK' if old3 in content_lf else 'P1c FALHOU')
if old3 in content_lf: content_lf = content_lf.replace(old3, new3)

# P1d: fix log message (allB64.length em vez de texto fixo)
old4 = 'if (res && res.success) log("' + '\U0001f4e4' + ' KMZ auto-publicado \u2014 operadores receberao ao abrir o projeto", "ok");'
new4 = 'if (res && res.success) log("' + '\U0001f4e4' + ' " + allB64.length + " KMZ publicado(s) \u2014 operadores receberao ao abrir o projeto", "ok");'
print('P1d OK' if old4 in content_lf else 'P1d FALHOU')
if old4 in content_lf: content_lf = content_lf.replace(old4, new4)

# P2: fetchRemoteKMZ multi-kmz
old5 = '        var blob = base64ToBlob(res.content, "application/vnd.google-earth.kmz");\n        var fakeFile = new File([blob], "area_atuacao.kmz", { type: "application/vnd.google-earth.kmz" });\n        removeKMZSourceByName(KMZ_ADMIN_SOURCE_NAME);\n        await loadKMZFile(fakeFile, { append: true, sourceName: KMZ_ADMIN_SOURCE_NAME, fitBounds: true });'
new5 = '        var contents = [];\n        try { var parsed = JSON.parse(res.content); contents = Array.isArray(parsed) ? parsed : [res.content]; }\n        catch(e) { contents = [res.content]; }\n        removeAllAdminKMZSources();\n        for (var ci = 0; ci < contents.length; ci++) {\n            var blobCi = base64ToBlob(contents[ci], "application/vnd.google-earth.kmz");\n            var srcName = KMZ_ADMIN_SOURCE_NAME + (contents.length > 1 ? " (" + (ci+1) + "/" + contents.length + ")" : "");\n            var fakeFileCi = new File([blobCi], "area_atuacao_" + ci + ".kmz", { type: "application/vnd.google-earth.kmz" });\n            await loadKMZFile(fakeFileCi, { append: true, sourceName: srcName, fitBounds: ci === contents.length - 1 });\n        }'
print('P2 OK' if old5 in content_lf else 'P2 FALHOU idx=' + str(content_lf.find('removeKMZSourceByName(KMZ_ADMIN_SOURCE_NAME)')))
if old5 in content_lf: content_lf = content_lf.replace(old5, new5)

# P2b: fix log KMZ remoto
old6 = 'log("\u2705 KMZ remoto carregado! Publicado por " + who + " em " + when, "ok");'
new6 = 'log("\u2705 " + contents.length + " KMZ remoto(s) carregado(s)! Publicado por " + who + " em " + when, "ok");'
print('P2b OK' if old6 in content_lf else 'P2b FALHOU')
if old6 in content_lf: content_lf = content_lf.replace(old6, new6)

# P3: adicionar removeAllAdminKMZSources antes de KMZ_ADMIN_SOURCE_NAME
anchor = 'var KMZ_ADMIN_SOURCE_NAME = "Admin central (remoto)";'
new_func = 'function removeAllAdminKMZSources() {\n  var found = true;\n  while (found) {\n    found = false;\n    if (!Array.isArray(S.kmzSources)) break;\n    for (var i = 0; i < S.kmzSources.length; i++) {\n      if (S.kmzSources[i].name && S.kmzSources[i].name.indexOf(KMZ_ADMIN_SOURCE_NAME) === 0) {\n        removeKMZSourceByName(S.kmzSources[i].name);\n        found = true; break;\n      }\n    }\n  }\n}\n\n'
print('P3 OK' if anchor in content_lf else 'P3 FALHOU')
if anchor in content_lf: content_lf = content_lf.replace(anchor, new_func + anchor)

# title
content_lf = content_lf.replace('<title>Campo GEO v5.9.7</title>', '<title>Campo GEO v5.9.8</title>')

final = content_lf.replace('\n', '\r\n')
with open(path, 'w', encoding='utf-8-sig', newline='') as f:
    f.write(final)
print('Salvo OK')
