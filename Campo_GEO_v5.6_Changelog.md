# Campo GEO v5.6 — Changelog

**Data:** 19/abr/2026
**Objetivo:** Suporte a múltiplos KMZ/KML carregados simultaneamente no mesmo mapa (projeto com várias áreas de atuação não contíguas).

---

## 🆕 Feature: MULTI-KMZ

### Problema
A v5.4 permitia apenas **1 KMZ por projeto**. Cada novo upload **substituía** o anterior. Projetos como Rio das Ostras, que têm várias áreas de atuação distintas (bairros, setores, quadras), precisavam ser divididos em "projetos falsos" ou ter o KMZ unificado manualmente — o que é inviável quando cada setor vem de uma fonte diferente.

### Solução
- **FAB 📐 KMZ+** agora abre seletor com `multiple` — seleciona vários arquivos de uma vez.
- Cada novo upload **acumula** no mapa em vez de substituir.
- Paleta rotativa de 8 cores distingue visualmente cada KMZ (âmbar → azul → verde → rosa → violeta → ciano → laranja → lima).
- Tooltip de cada polígono mostra o **nome do arquivo de origem**.
- **Geo-fence segue funcionando** — a validação `fora_area` checa o ponto GPS contra **todos os polígonos acumulados** (já era o comportamento desde v5.2; só o loader estava limitado).

### Modelo de dados
Nova estrutura de persistência (localStorage `cg_kmz_<folder>`):
```json
{
  "v": 2,
  "polys": [[[lat,lng],...], ...],         // array flat de todos os polígonos
  "sources": [                              // rastreia origem de cada grupo
    {"name": "Admin central (remoto)",             "count": 2, "startIdx": 0},
    {"name": "Rio das Ostras - Jardim Marilea.kmz","count": 1, "startIdx": 2},
    {"name": "Rio das Ostras - Bosque.kmz",         "count": 3, "startIdx": 3}
  ]
}
```
Formato legado (array flat) continua sendo lido pelo `restoreKMZ` — migração transparente ao primeiro save.

### KMZ central do admin preserva KMZs locais
Antes: `fetchRemoteKMZ()` (chamado 500ms após abrir o projeto) **apagava tudo** e punha o KMZ publicado pelo admin no lugar.
Agora: remove apenas a source `"Admin central (remoto)"` e re-adiciona a versão fresca — **KMZs que o operador carregou localmente permanecem no mapa**. Se o admin publicar um novo KMZ central, ele é atualizado silenciosamente sem impactar os extras do operador.

---

## 🔧 Mudanças técnicas

| Função | Antes | Depois |
|---|---|---|
| `<input id="kmz-input">` | aceita 1 arquivo | aceita **N arquivos** (`multiple`) |
| `loadKMZFile(file)` | substitui `S.kmzAllPolygons` | `loadKMZFile(file, opts)` com `opts.append` — acumula ou substitui |
| `drawKMZPolygons(polys)` | limpa tudo e redesenha | `drawKMZPolygons(polys, opts)` — modo append preserva camadas |
| `onKMZSelected(ev)` | processava `ev.target.files[0]` | itera **todos** os arquivos em série com `append:true` |
| `restoreKMZ()` | lia array flat | lê formato v2 (com sources) e legado v1 |
| `clearKMZ()` | removia 1 polígono | remove **todos** os KMZ + sources, confirma quantos |
| `fetchRemoteKMZ()` | substitui tudo | remove só a source `"Admin central (remoto)"` e re-adiciona |
| `removeKMZSourceByName(name)` | — | **nova** — remove source específica e recalcula `startIdx` dos demais |

### State novo
- `S.kmzSources[]` — array de `{name, count, startIdx}` paralelo a `S.kmzAllPolygons`.
- `KMZ_PALETTE[]` — paleta de 8 cores para sources distintas.
- `KMZ_ADMIN_SOURCE_NAME` — constante `"Admin central (remoto)"` usada pelo `fetchRemoteKMZ`.

### Compatibilidade
- **Retrocompat v1 total:** localStorage antigo (array flat) é lido pelo `restoreKMZ` e convertido para v2 no primeiro save.
- **Validação geo-fence:** inalterada — já usava `S.kmzAllPolygons` como array desde v5.2.
- **Backend Apps Script:** inalterado — a action `getKMZ` ainda retorna um único KMZ central por projeto.

---

## 🎯 Uso no Rio das Ostras (cenário real)

1. Admin publica no backend o KMZ do **município inteiro** (perímetro oficial).
2. Operador abre o app → `fetchRemoteKMZ` carrega o perímetro municipal (source "Admin central (remoto)", cor âmbar).
3. No FAB 📐 KMZ+, operador seleciona **múltiplos** arquivos locais dos bairros daquela jornada (`Jardim Mariléa.kmz`, `Extensão do Bosque.kmz`, `Cidade Praiana.kmz`).
4. Cada bairro aparece em cor distinta com tooltip nomeado.
5. Ao fotografar, geo-fence checa se o ponto cai em **qualquer** polígono ativo — se cair fora de todos, marca `fora_area: true` para auditoria (não bloqueia).
6. Tudo persiste no localStorage — no próximo login o mapa é restaurado exatamente como estava.

---

## ✅ Testes executados

- Parser JS validado (`new Function(code)` sobre o script inline do index.html — sem erros).
- Teste unitário isolado da lógica `removeKMZSourceByName` — `startIdx` recalcula corretamente após remoções, re-adições e ciclo completo clear → add → remove → vazio.
- Retrocompatibilidade de formato v1 validada pelo `restoreKMZ`.

---

## 🔜 Próximos passos (não incluídos nesta versão)

- Listar as sources ativas em um mini-painel na UI (hoje só aparecem no log).
- Botão "remover este KMZ" por source (hoje `clearKMZ` limpa tudo).
- Publicação de múltiplos KMZ centrais pelo admin (hoje backend suporta 1 por projeto).
