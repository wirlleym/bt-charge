# BT Charge 🎧

Monitor de bateria de **headsets Bluetooth** na bandeja do sistema (Linux/GNOME).
Consulta o nível de bateria dos fones pareados via **D-Bus/BlueZ** e mostra ao
lado do ícone 🎧:

| Estado | Bandeja |
|---|---|
| Um fone conectado | `[🎧] 87%` |
| Vários conectados | `[🎧] 64%` *(menor percentual)* |
| Nenhum conectado | `[🎧]` *(só o ícone)* |
| Conectado sem bateria | `[🎧] --` |

## Instalação (Ubuntu/Debian)

Baixe o `.deb` da página de [Releases](https://github.com/wirlleym/bt-charge/releases) e:

```bash
sudo apt install ./bt-charge_1.0.0-1_all.deb
```

O pacote instala as dependências automaticamente (`python3-gi`,
`python3-dbus`, `gir1.2-ayatanaappindicator3-0.1`), o ícone no tema do
sistema e o autostart (`/etc/xdg/autostart`) — inicia junto com a sessão.

### Sem sudo (alternativa)

```bash
install -m 0755 bt-charge ~/.local/bin/bt-charge
mkdir -p ~/.local/share/bt-charge/icons
cp -r icons/hicolor ~/.local/share/bt-charge/icons/
cp packaging/autostart.desktop ~/.config/autostart/bt-charge.desktop
```

## Uso

```text
bt-charge             executa o indicador na bandeja
bt-charge --check     consulta o estado uma vez e sai
bt-charge --discover  lista os fones pareados classificados e sai
```

- **Menu**: clique no indicador → cada fone conectado (nome, estado,
  bateria) + `Atualizar agora` + `Sair`.
- **Config**: `~/.config/bt-charge/config.json` — lista de fones
  (`mac` + `name`), `poll_interval` (padrão 30 s) e `auto_add_devices`.
  Novos fones de áudio pareados são detectados e adicionados
  automaticamente. Caixas de som, mouses, teclados etc. são ignorados.
- **Log**: `~/.local/state/bt-charge/bt-charge.log`.

## Requisitos

- Ubuntu 24.04+ / GNOME (extensão "Ubuntu AppIndicators" ativa — padrão)
- BlueZ 5.5+ (`bluetoothctl`)
- Python 3.9+

## Desenvolvimento

```bash
packaging/build-deb.sh   # gera dist/bt-charge_1.0.0-1_all.deb
```

## Licença

MIT
