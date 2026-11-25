#!/bin/bash
# Nouvelle version TrouveTaMusique : git tag + copie archive.
# usage : ./scripts/nouvelle_version.sh 1.1 "ce qui change"
set -e
V="${1:?numéro de version}"
MSG="${2:?description}"
cd "$(dirname "$0")/.."
git add -A
git commit -m "v${V} — ${MSG}" || echo "(rien de neuf)"
git tag -f "v${V}"
DEST="$HOME/trouvemusique-versions/trouvemusique-v${V}"
mkdir -p "$DEST"
rsync -a --exclude '.venv' --exclude '__pycache__' --exclude '.git' --delete "${PWD}/" "$DEST/"
echo "✔ Version v${V} archivée : $DEST"
