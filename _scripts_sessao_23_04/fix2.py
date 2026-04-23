path = r'C:\Users\carlo\BRASIL_LIMPO\Scripts\campo-geo\index.html'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

lf = content.replace('\r\n', '\n')

# Inspeciona os logs que falharam
import re
for m in re.finditer(r'auto-publicado', lf):
    print('P1d ctx:', repr(lf[m.start()-10:m.start()+120]))
for m in re.finditer(r'KMZ remoto carregado', lf):
    print('P2b ctx:', repr(lf[m.start()-10:m.start()+120]))
