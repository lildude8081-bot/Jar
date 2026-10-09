#!/usr/bin/env bash

echo "🚀 Pornim crearea pachetului instalator .deb pentru Linux Jar File Manager..."

# 1. Creăm structura temporară de directoare Debian
CALE_PACHET="linux-jar-file-manager_1.5.0_amd64"
mkdir -p "$CALE_PACHET/DEBIAN"
mkdir -p "$CALE_PACHET/usr/share/linux-jar-manager"
mkdir -p "$CALE_PACHET/usr/share/applications"
mkdir -p "$CALE_PACHET/usr/share/pixmaps"
mkdir -p "$CALE_PACHET/usr/bin"

# 2. Copiem toate modulele noastre în folderul de sistem dedicat al aplicației
cp -r gui core assets readme main_window.py "$CALE_PACHET/usr/share/linux-jar-manager/"

# Copiem iconița cu borcanul în galeria de pixmaps a sistemului ca să o vadă meniul Mint
cp assets/icons/borcan.png "$CALE_PACHET/usr/share/pixmaps/linux-jar-manager.png"

# 3. Creăm scriptul executabil rapid în /usr/bin/ care va lansa aplicația din meniu
cat << 'EOF' > "$CALE_PACHET/usr/bin/jar-manager"
#!/usr/bin/env bash
python3 /usr/share/linux-jar-manager/main_window.py "$@"
EOF
chmod +x "$CALE_PACHET/usr/bin/jar-manager"

# ===============================================================================
# LUSTRUIRE AUTOMATIZARE ALIAS ÎN CONFIGURAREA GLOBALĂ A TERMINALULUI
# ===============================================================================
# Creăm scriptul postinst (rulează automat imediat după instalarea pachetului)
cat << 'EOF' > "$CALE_PACHET/DEBIAN/postinst"
#!/usr/bin/env bash
echo "✨ Configurăm alias-ul global 'jar' pentru terminal..."
# Adăugăm alias-ul în /etc/bash.bashrc pentru ca TOȚI utilizatorii de pe sistem să îl aibă disponibil
if ! grep -q "alias jar=" /etc/bash.bashrc; then
    echo "alias jar='jar-manager'" >> /etc/bash.bashrc
fi
EOF
chmod +x "$CALE_PACHET/DEBIAN/postinst"

# Creăm scriptul postrm (rulează automat la dezinstalare pentru a curăța sistemul)
cat << 'EOF' > "$CALE_PACHET/DEBIAN/postrm"
#!/usr/bin/env bash
echo "🗑️ Curățăm alias-ul 'jar' din configurația de sistem..."
if [ -f /etc/bash.bashrc ]; then
    sed -i '/alias jar=/d' /etc/bash.bashrc
fi
EOF
chmod +x "$CALE_PACHET/DEBIAN/postrm"
# ===============================================================================

# 4. Creăm fișierul CONTROL (Informațiile pachetului pentru managerul de aplicații)
cat << 'EOF' > "$CALE_PACHET/DEBIAN/control"
Package: linux-jar-file-manager
Version: 1.5.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Mihai <mihai@aura.local>
Depends: python3, python3-pyqt6
Description: A unique visual twin-layer file manager for Linux.
 Features a responsive storage monitor, multi-language support,
 instant filter search and a creative jar metaphor.
EOF

# 5. Creăm comanda rapidă (Scurtătura pentru meniul de aplicații de tip Start)
cat << 'EOF' > "$CALE_PACHET/usr/share/applications/linux-jar-manager.desktop"
[Desktop Entry]
Version=1.5.0
Type=Application
Name=Linux Jar Manager
Name[ro]=Manager Fișiere Borcan
Comment=Creative visual file manager for Linux
Exec=jar-manager
Icon=linux-jar-manager
Terminal=false
Categories=System;Utility;
EOF

# 6. Împachetarea finală nativă
dpkg-deb --build "$CALE_PACHET"

# Curățăm folderele temporare, lăsând doar instalatorul curat
rm -rf "$CALE_PACHET"

echo "✅ CONFIGURARE COMPLETĂ! Fișierul tau instalator este gata: linux-jar-file-manager_1.5.0_amd64.deb"
