# Campo GEO v4.2 — Changelog

**Data:** 17/abr/2026
**Objetivo:** Correções definitivas dos bugs reportados + features solicitadas para próxima cidade.

## 🐛 Bugs corrigidos

### EXIF GPS não estava sendo lido
- **Causa raiz:** parser manual tinha 2 bugs sutis de byte-order (IFD pointer) e não suportava HEIC do iPhone 13+.
- **Correção:** substituído por biblioteca `exifr@7.1.3` (via CDN jsdelivr). Agora lê JPEG, HEIC, RAW e TIFF com precisão. Extrai também `DateTimeOriginal` (timestamp da foto) e `GPSHPositioningError` (precisão real).
- **Efeito:** fotos uploaded agora aparecem corretamente no mapa e no contador.

### Check-points verdes tampando nomes das ruas
- **Causa raiz:** ícones em emoji 28px.
- **Correção:** `makeDot(color)` com dots CSS de 14px (círculo branco com borda), cores distintas:
  - 🟠 Laranja `#f59e0b` — foto na fila
  - 🟢 Verde `#10b981` — foto já enviada
  - 🔴 Vermelho `#ef4444` — foto rejeitada (fora do KMZ)
- **Efeito:** nomes de ruas ficam legíveis no mapa mesmo com dezenas de pontos.

## 🆕 Features novas

### Watermark nas fotos (padrão IMPLURB — fiscalização TCE)
Canvas overlay aplicado na compressão, replicando o padrão já usado nas fotos do IMPLURB:
- **Badge superior esquerdo:** "EVIDÊNCIA GEORREFERENCIADA" (fundo âmbar)
- **Logo Brasil Limpo** superior direito (fundo branco semi-transparente)
- **Faixa inferior** com:
  - Rua completa
  - Bairro — Cidade — UF
  - GPS (6 casas decimais) + precisão em metros
  - Data/hora (formato pt-BR)
  - Operador | Projeto
- Tipografia responsiva (2.2% da largura da imagem)
- Sombra preta para legibilidade em qualquer fundo

### Suporte a arquivo KMZ (área de atuação)
Substituição do mapa desenhado por arquivo KMZ real:
- **Botão 📐 KMZ** na aba Mapa — upload de `.kmz` ou `.kml`
- **JSZip** extrai o KML do KMZ (é um zip)
- **DOMParser** lê `<Polygon><outerBoundaryIs><LinearRing><coordinates>`
- Desenha polígono destacado no Leaflet (âmbar, borda 3px, fill 8%)
- **Ray casting** (`pointInPolygon`) valida cada foto:
  - 📸 dentro do polígono → aceita normalmente
  - 🚫 fora → rejeita com marcador vermelho temporário (8s) + log
- Polígono persiste no localStorage por projeto (`cg_kmz_[FOLDER]`)
- Ajusta viewport do mapa automaticamente ao carregar

### Autenticação Google (OAuth 2.0)
- Gate de autenticação antes do app abrir
- **Google Sign-In** via `accounts.google.com/gsi/client`
- **Allowlist configurável** de e-mails autorizados (via localStorage, botão admin)
- Session persistida em `sessionStorage` (expira ao fechar o browser)
- Exibe avatar + nome + e-mail no topo
- Botão "Sair" disponível
- **Primeira configuração:** admin cola o Client ID do Google Cloud Console (`Authorized JavaScript origins: https://carloskaiketavares-droid.github.io`)

### Encerramento de projeto
- Botão **🔒 ENCERRAR PROJETO** na aba Enviar
- Exige digitar "ENCERRAR" para confirmar (dupla proteção)
- Grava flag `cg_closed_[FOLDER]` no localStorage
- Cria arquivo `PROJETO_ENCERRADO.md` no vault em `04_PROJETOS/[FOLDER]/`
- A partir daí, o projeto só abre em **modo leitura** (capturas e uploads bloqueados)
- Protege o projeto durante a fase de depuração documental (fiscalização do TCE)

## 🔧 Melhorias técnicas

- Geocoder agora retorna `uf` (short_name do Google / state_code do Nominatim)
- `processPhoto` reordenado: **validação KMZ → geocode → compress+watermark** (ordem correta para watermark ter endereço)
- CSS: stack vertical de FABs no mapa (Sincronizar / KMZ / Limpar KMZ)

## 📋 Checklist pós-deploy (admin)

1. [ ] No Google Cloud Console: criar OAuth Client ID Web
   - Authorized origins: `(https://carloskaiketavares-droid.github.io)`
2. [ ] Abrir o app no browser → clicar "⚙️ Configurar Google OAuth" → colar Client ID
3. [ ] (Opcional) Clicar "Allowlist" → colar e-mails autorizados separados por vírgula
4. [ ] Para próxima cidade: gerar KMZ no Google Earth → enviar para operador → operador carrega via 📐 KMZ na aba Mapa
5. [ ] Ao fim da depuração documental: clicar 🔒 ENCERRAR PROJETO

---

**Commit:** v4.2 — EXIF robusto + watermark IMPLURB + KMZ + Google Login + ícones menores + encerramento de projeto
