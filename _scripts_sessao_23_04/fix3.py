path = r'C:\Users\carlo\BRASIL_LIMPO\Scripts\campo-geo\index.html'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()
lf = content.replace('\r\n', '\n')

# P1d: emojis sao stored como \u escapes literais no arquivo
old_p1d = r'if (res && res.success) log("\ud83d\udce4 KMZ auto-publicado \u2014 operadores receberao ao abrir o projeto", "ok");'
new_p1d = r'if (res && res.success) log("\ud83d\udce4 " + allB64.length + " KMZ publicado(s) \u2014 operadores receberao ao abrir o projeto", "ok");'
print('P1d OK' if old_p1d in lf else 'P1d FALHOU')
if old_p1d in lf: lf = lf.replace(old_p1d, new_p1d)

# P2b
old_p2b = r'log("\u2705 KMZ remoto carregado! Publicado por " + who + " em " + when, "ok");'
new_p2b = r'log("\u2705 " + contents.length + " KMZ remoto(s) carregado(s)! Publicado por " + who + " em " + when, "ok");'
print('P2b OK' if old_p2b in lf else 'P2b FALHOU')
if old_p2b in lf: lf = lf.replace(old_p2b, new_p2b)

final = lf.replace('\n', '\r\n')
with open(path, 'w', encoding='utf-8-sig', newline='') as f:
    f.write(final)
print('Salvo')
