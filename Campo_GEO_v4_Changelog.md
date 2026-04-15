# Campo GEO v4.0 — Changelog

> **Projeto:** Campo GEO  
> **Versão:** v4.0  
> **Data:** 2026-04-14  
> **Status:** Deploy pendente no GitHub Pages  

---

## Problema Diagnosticado

### Varredura no CÉREBRO (Drive)
- **Pastas criadas corretamente:** cadernos_campo, book_imagens, e subpastas por bairro (Ouro_Verde, Bosque_DAreia, Recreio, Atlântica, Mar_y_Lago, Village_Rio_das_Ostras, etc.)
- **ZERO arquivos salvos:** Nenhum `.json` de foto, nenhum `.md` de caderno, nenhum `pontos_enviados.json`
- **Causa raiz:** O base64 das fotos capturadas pelo celular (3-10MB cada) excede o limite de payload do Apps Script POST (~6MB), causando falha silenciosa no salvamento

### Consequências
1. Fotos nunca chegavam ao Drive
2. `pontos_enviados.json` nunca era criado → pontos não apareciam no mapa
3. Cadernos `.md` não eram gerados
4. Sem estado compartilhado entre dispositivos

---

## Correções Implementadas

### 1. Compressão de Imagem via Canvas
- Redimensiona fotos para máximo 800px (maior dimensão)
- Qualidade JPEG 0.5
- Resultado: ~50-200KB por foto (vs 3-10MB original)
- Payload cabe confortavelmente no limite do Apps Script

### 2. Metadados sem Base64
- `pontos_enviados.json` salva APENAS metadados (lat, lng, acc, address, operator, timestamp)
- Arquivo leve (~1-5KB por ponto) — ideal para sync entre dispositivos
- Imagens comprimidas salvas em arquivos separados por bairro/rua

### 3. Auto-Sync (30 segundos)
- Todos os dispositivos logados no mesmo projeto sincronizam automaticamente
- Pull de `pontos_enviados.json` a cada 30s
- Pontos e contagens compartilhados entre todos os operadores

### 4. Marcadores Persistentes no Mapa
- Pontos na fila: 📸 (azul)
- Pontos enviados: ✅ (verde)
- Permanecem no mapa até fechamento do app
- Restaurados do cache local ao reabrir

### 5. Logo Brasil Limpo
- Adicionada na tela de setup (120x120px)
- Adicionada no header do app (28x28px)
- Arquivo: `logo.svg` (referência externa)

### 6. Caderno Markdown Automático
- Gerado por bairro no envio do lote
- Inclui: projeto, operador, lote, timestamp
- Cada foto com: rua, bairro, CEP, coordenadas, timestamp, operador, ID

---

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `index.html` | App completo v4.0 |
| `logo.svg` | Logo Brasil Limpo (fundo transparente) |
| `.nojekyll` | Flag GitHub Pages |
| `README.md` | Readme do repo |

## Deploy
- **Repo:** `carloskaiketavares-droid/campo-geo`
- **URL:** `carloskaiketavares-droid.github.io/campo-geo/`
- **Status:** Commit local pronto, aguardando push

---

## Wikilinks
- [[Regra de Liberacao Campo GEO]]
- [[02_MAPA_ATUACAO_SETORES]]
- [[Diretriz Operacional do Cerebro]]

