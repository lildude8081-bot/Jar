#!/usr/bin/env bash

echo "🫙 Pregătim urcarea Borcanului pe GitHub pentru contul lildude8081-bot..."

# Inițializăm depozitul local Git dacă nu este deja făcut
if [ ! -d ".git" ]; then
    git init
    git branch -M main
fi

# Configurăm identitatea locală pentru a se potrivi cu profilul tău
git config user.name "lildude8081-bot"
git config user.email "lildude8081@gmail.com"

# Adăugăm fișierele și creăm un commit (un stadiu salvat)
git add assets core gui readme main_window.py README.md ghid_instalare.txt construieste_installer.sh
git commit -m "Initial release v1.5.0 - Fully modular jar manager for elementary OS"

# Conectăm folderul tău local cu repository-ul de pe internet
git remote remove origin 2>/dev/null
git remote add origin https://github.com

echo "🚀 Trimitem fișierele pe GitHub..."
echo "⚠️ NOTĂ: Când îți cere Username-ul, tastează: lildude8081-bot"
echo "⚠️ NOTĂ: La Password, GitHub cere acum un Token Special în loc de parola ta veche!"

git push -u origin main
