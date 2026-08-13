# BT Charge — contexto do plugin

> Contexto para continuar o trabalho neste repositório (Orca / agentes).
> Última atualização: 2026-08-13 (v1.0.1-2 publicada).

## O que é

**BT Charge** — monitor de bateria de **headsets Bluetooth** na bandeja do
sistema (Linux/GNOME). Consulta o nível de bateria dos fones pareados via
**D-Bus/BlueZ** (assíncrono, não bloqueia a UI) e mostra ao lado do ícone 🎧:

| Estado | Bandeja |
|---|---|
| Um fone conectado | `[🎧] 87%` |
| Vários conectados | `[🎧] 64%` *(menor percentual)* |
| Nenhum conectado | `[🎧]` *(só o ícone)* |
| Conectado sem bateria | `[🎧] --` |

## Arquitetura

- **`bt-charge`** — script Python único (~560 linhas), sem dependências além de:
  `python3-gi`, `python3-dbus`, `gir1.2-ayatanaappindicator3-0.1`,
  `gir1.2-gtk-3.0` (BlueZ 5.5+, Ubuntu 24.04/GNOME).
- **Bandeja** = `AyatanaAppIndicator3` (StatusNotifierItem). O GNOME exige a
  extensão "Ubuntu AppIndicators" (padrão no Ubuntu).
- **Ícones**:
  - `bt-charge-emoji` (22/44px, fone branco) = **ícone da bandeja** (não mudar).
  - `bt-charge` (32–128px, fone branco + rune Bluetooth azul, fundo slate) =
    ícone do **app** (.desktop / lista de apps), gerado por
    `packaging/gen-icon.py` (PIL).
- **Modelo**: coleção `Device[]` (MAC = identidade; nome = exibição). Config em
  `~/.config/bt-charge/config.json`: `devices` (mac+name), `poll_interval`
  (30s), `auto_add_devices`. Auto-descoberta de fones pareados (classifica por
  UUIDs: Audio Sink + HFP/AVRCP-Target; caixas de som/mouse/teclado ignorados).
- **Consultas**: `GetManagedObjects` assíncrono + eventos
  `PropertiesChanged`/`InterfacesAdded`/`InterfacesRemoved` (conexão,
  desconexão, bateria em tempo real); poll de segurança a cada 30s.
- **Instância única**: `flock` em `$XDG_RUNTIME_DIR/bt-charge.lock`.

## Files (repositório)

```
bt-charge                 # script principal
icons/                    # ícones: hicolor/ (bandeja) + <tam>x<tam>/ (app)
packaging/
  control                 # metadados do .deb (Depends)
  postinst                # gtk-update-icon-cache
  bt-charge.desktop       # menu de apps (Icon=bt-charge)
  autostart.desktop       # /etc/xdg/autostart
  build-deb.sh            # gera dist/bt-charge_<ver>_all.deb
  gen-icon.py             # gera o ícone do app
dist/                     # .deb gerados (não versionado)
README.md  LICENSE  .gitignore
```

## Empacotar / publicar

```bash
packaging/build-deb.sh                    # gera dist/bt-charge_1.0.1-2_all.deb
sudo apt install ./dist/bt-charge_1.0.1-2_all.deb
git add -A && git commit -m "..." && git push origin main
gh release create v1.0.2 dist/bt-charge_<ver>_all.deb --title "..." --notes "..."
```

Publicado: repo `wirlleym/bt-charge` (GitHub, público); releases v1.0.0 e
v1.0.1 (com o .deb).

## Pitfalls já mapeados (não repetir o processo de investigação)

1. **Label da bandeja não aparecia** — `XAyatanaLabel` é propriedade
   OPCIONAL do SNI; a extensão só sincroniza quando o label **muda após a
   conexão**. Solução no código: `_labels_ready` — o label só é setado
   ~3s após o start (`GLib.timeout_add_seconds(3, self._enable_labels)`).
2. **Ícone da bandeja virava "…"** — a extensão mostra fallback
   `image-loading-symbolic` (3 pontinhos) quando o item fica sem ícone.
   Nunca deixar `IconName` vazio; usar tema próprio via
   `set_icon_theme_path` + `set_icon`.
3. **Tema de ícones** — `set_search_path` do Gtk/St.IconTheme procura
   `<path>/<tema>/...`; o diretório do app precisa da estrutura
   `hicolor/22x22|44x44/` com `index.theme`.
4. **Icons do .deb** — o `index.theme` do hicolor declara os diretórios
   `apps/`; ícones de app vão em `/usr/share/icons/hicolor/<size>x<size>/apps/`
   (1.0.1-1 instalou errado → corrigido na 1.0.1-2).
5. **Ícone antigo na lista de apps** — o GNOME Shell cacheia ícones em
   memória; `touch` no .desktop + `gtk-update-icon-cache` ajudam, mas o
   definitivo é **logout/login**.
6. **Bateria "sumida"** — após reconexão o BlueZ às vezes não expõe
   `org.bluez.Battery1` (AVRCP); o app mostra `--` (correto) e uma
   reconexão restaura a leitura.
7. **apt com caminho relativo** — `apt install ./dist/foo.deb` falha com
   "Arquivo sem suporte"; usar caminho absoluto.
8. **`-1` como argumento do busctl** — busctl interpreta como opção; usar
   profundidade positiva no GetLayout do menu.

## Estado atual (2026-08-13)

- v1.0.1-2 instalado via apt em /usr/bin/bt-charge (instância rodando,
  bandeja OK, bateria 100% após reconexão).
- Artefatos de instalação manual removidos (`~/.local/bin`, `~/.local/share`).
- Config/log do usuário: `~/.config/bt-charge/config.json` e
  `~/.local/state/bt-charge/bt-charge.log`.
- **Pendente**: confirmar com o usuário se o ícone novo apareceu na lista de
  apps (após o reload; senão, logout/login resolve).
