#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <lang> <lang_name>"
    echo "Example: $0 fr French"
    exit 1
fi

if [ ! -d "./translations_$1" ]; then
    echo "The directory ./translations_$1 does not exist."
    exit 1
fi

if [ ! -f "./translations_$1/translations_$1.ts" ]; then
    echo "The file ./translations_$1/translations_$1.ts does not exist."
    exit 1
fi

if [ ! -f "./translations_$1/encyclopedia_$1.json" ]; then
    echo "The file ./translations_$1/encyclopedia_$1.qm does not exist."
    exit 1
fi

cd "$(dirname "$0")/translations_$1"
mkdir compile
cp translations_$1.ts ./compile/language.ts
cp encyclopedia_$1.json ./compile/encyclopedia.json
cd compile
lrelease language.ts
zip ../$2.tmpts *
cd ..
rm -rf compile