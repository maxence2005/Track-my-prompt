#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <lang>"
    echo "Example: $0 fr"
    exit 1
fi

cd "$(dirname "$0")"
mkdir -p ./translations_$1
# Create the translation file (e.g., translations_fr.ts) or update it
# Find all .qml files in qtquickdetect/views/ recursively and store them in a variable
qml_files=$(find ../qtquickdetect/views/ -name "*.qml")
lupdate $qml_files -ts ./translations_$1/translations_$1.ts -locations none
cp default_encyclopedia.json ./translations_$1/encyclopedia_${1}.json