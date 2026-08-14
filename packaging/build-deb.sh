#!/usr/bin/env bash
# Build do pacote .deb do BT Charge.
# Uso: ./build-deb.sh [versão]  (padrão: 1.0.1-2)
set -euo pipefail

cd "$(dirname "$0")/.."          # raiz do repositório
VERSION="${1:-1.0.1-2}"
PKG="bt-charge_${VERSION}_all"
BUILD="packaging/_build/${PKG}"
DEB="dist/${PKG}.deb"

echo "==> Montando ${DEB}"
rm -rf "${BUILD}" "dist/${PKG}.deb"
mkdir -p "${BUILD}/DEBIAN" \
         "${BUILD}/usr/bin" \
         "${BUILD}/usr/share/bt-charge/icons/hicolor/22x22" \
         "${BUILD}/usr/share/bt-charge/icons/hicolor/44x44" \
         "${BUILD}/usr/share/applications" \
         "${BUILD}/etc/xdg/autostart"

# binário principal
install -m 0755 bt-charge "${BUILD}/usr/bin/bt-charge"

# tema de ícones do app (fallback de caminho para o ícone da bandeja 🎧)
install -m 0644 icons/hicolor/index.theme \
    "${BUILD}/usr/share/bt-charge/icons/hicolor/index.theme"
install -m 0644 icons/hicolor/22x22/bt-charge-emoji.png \
    "${BUILD}/usr/share/bt-charge/icons/hicolor/22x22/"
install -m 0644 icons/hicolor/44x44/bt-charge-emoji.png \
    "${BUILD}/usr/share/bt-charge/icons/hicolor/44x44/"

# ícones do app no tema de sistema (hicolor) — dentro de <size>x<size>/apps/,
# que é o subdiretório declarado no index.theme do hicolor; o SVG escalável
# garante nitidez em qualquer resolução (grade do GNOME, dock, alt-tab).
for size in 16 22 24 32 44 48 64 96 128 192 256; do
    mkdir -p "${BUILD}/usr/share/icons/hicolor/${size}x${size}/apps"
    install -m 0644 "icons/${size}x${size}/bt-charge.png" \
        "${BUILD}/usr/share/icons/hicolor/${size}x${size}/apps/"
done
mkdir -p "${BUILD}/usr/share/icons/hicolor/scalable/apps"
install -m 0644 icons/scalable/bt-charge.svg \
    "${BUILD}/usr/share/icons/hicolor/scalable/apps/"

# .desktop: menu de aplicativos + autostart
install -m 0644 packaging/bt-charge.desktop \
    "${BUILD}/usr/share/applications/bt-charge.desktop"
install -m 0644 packaging/autostart.desktop \
    "${BUILD}/etc/xdg/autostart/bt-charge.desktop"

# metadados do pacote (Version do control segue o argumento do script)
install -m 0644 packaging/control "${BUILD}/DEBIAN/control"
sed -i "s/^Version: .*/Version: ${VERSION}/" "${BUILD}/DEBIAN/control"
install -m 0755 packaging/postinst "${BUILD}/DEBIAN/postinst"

dpkg-deb --build --root-owner-group "${BUILD}" "dist/${PKG}.deb" >/dev/null
rm -rf packaging/_build

echo "==> OK: ${DEB} ($(du -h "${DEB}" | cut -f1))"
