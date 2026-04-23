# Campo GEO — Changelog v5.9.9

**Data:** 2026-04-23 (madrugada)
**Commit:** c11fb9e
**Branch:** main → GitHub Pages ao vivo

---

## v5.9.9 — KMZ Append: upload acumula, não sobrescreve

### Problema resolvido
Admin que fazia upload de KMZ um a um perdia os anteriores — cada upload
sobrescrevia o rea_atuacao.kmz.b64 no Drive com apenas o último arquivo.

### Solução implementada
onKMZSelected() agora busca o KMZ existente antes de publicar, faz merge
e salva um JSON array com todos os KMZs acumulados:

`
["b64_kmz_1", "b64_kmz_2", ..., "b64_kmz_N"]
`

Backward compatible: se o campo contém string simples (1 KMZ antigo),
é tratado como array de 1 elemento antes do merge.

### Operadores
etchRemoteKMZ() já suportava JSON array desde v5.9.x — carrega cada KMZ
com ppend:true, exibindo todos os bairros simultaneamente no mapa.

---

## Dados Macaé — Sessão 2026-04-23

### 7 KMZ Bairros publicados
Arquivo rea_atuacao.kmz.b64 (Drive MACAE_RJ/_config):
- 11.378 bytes | 7 KMZs em array JSON
- Bairros: cantro, cajueiros, imbetiba, alto dos cajueiros,
  praia do campista, cavaleiros, morada das garças
- Sincronizado com cloud às 23:32 BRT | ID Drive: 1wzzfQnOFisgvD0nZQgicyDb2xb5ue_UR

### Watermark nas fotos de campo
- 158 de 159 fotos dos cadernos de campo (MACAE_RJ/cadernos_campo) marcadas
- Selo PIL: círculo azul + "Macaé PREFEITURA" (bottom-right, proporcional)
- 1 foto sem imagem (skipped) | 0 erros
- Script: C:\Users\carlo\watermark_macae.py

### Verificação final
- GitHub Pages v5.9.9: ao vivo ✅
- Drive cloud sincronizado: 11.378 bytes confirmados via API Drive ✅
- Operadores: recebem 7 bairros ao sincronizar KMZ ✅
