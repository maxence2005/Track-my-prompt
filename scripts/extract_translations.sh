#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <lang>"
    echo "Exemple: $0 fr"
    exit 1
fi

cd "$(dirname "$0")"
mkdir -p ./translations
# Crée le fichier de traduction (ex. : translations_fr.ts) ou le met à jour
# Trouve tous les fichiers .qml dans qtquickdetect/views/ de manière récurvise et les stocke dans une variable
qml_files=$(find ../qtquickdetect/views/ -name "*.qml")
lupdate $qml_files -ts ./translations/translations_$1.ts
