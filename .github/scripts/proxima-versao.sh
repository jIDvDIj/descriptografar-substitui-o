#!/usr/bin/env bash
# Calcula a próxima versão (SemVer) a partir da última tag vX.Y.Z e dos commits
# feitos depois dela, seguindo Conventional Commits:
#   "tipo!:" ou "BREAKING CHANGE" no corpo -> major
#   feat                                   -> minor
#   qualquer outro tipo                    -> patch
# Sem nenhuma tag, a primeira versão é 1.0.0.
# Imprime "versao=X.Y.Z" e "anterior=vA.B.C" (vazio na primeira); sem commits
# novos desde a última tag, imprime "versao=" vazio.
set -euo pipefail

anterior=$(git describe --tags --abbrev=0 --match 'v[0-9]*.[0-9]*.[0-9]*' 2>/dev/null || true)

if [ -z "$anterior" ]; then
  echo "versao=1.0.0"
  echo "anterior="
  exit 0
fi

if [ -z "$(git rev-list "$anterior..HEAD")" ]; then
  echo "versao="
  echo "anterior=$anterior"
  exit 0
fi

IFS=. read -r major minor patch <<< "${anterior#v}"
titulos=$(git log --format=%s "$anterior..HEAD")
corpos=$(git log --format=%b "$anterior..HEAD")

if grep -qE '^[a-z]+(\([^)]*\))?!:' <<< "$titulos" || grep -q 'BREAKING CHANGE' <<< "$corpos"; then
  major=$((major + 1)); minor=0; patch=0
elif grep -qE '^feat(\([^)]*\))?:' <<< "$titulos"; then
  minor=$((minor + 1)); patch=0
else
  patch=$((patch + 1))
fi

echo "versao=$major.$minor.$patch"
echo "anterior=$anterior"
