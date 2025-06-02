#!/bin/bash

MARKER="/var/data/.deps_installed"

if [ ! -f "$MARKER" ]; then
    echo "[Flatpak] Installation des dépendances utilisateur..."
    /app/bin/python3.11 /app/bin/TrackMyPrompt-installer.py
    if [ $? -eq 0 ]; then
        touch "$MARKER"
    else
        echo "[Flatpak] Installation échouée."
        exit 1
    fi
else
    echo "[Flatpak] Dépendances déjà installées. On continue."
fi

cd /app
/app/bin/python3.11 -m track_my_prompt "$@"
