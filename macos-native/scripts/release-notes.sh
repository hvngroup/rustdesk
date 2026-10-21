#!/usr/bin/env bash
# Print the CHANGELOG.md section for one version, used as the GitHub Release body.
#
# Usage: scripts/release-notes.sh 1.0.0
# Exits non-zero when the version has no section, so a release cannot ship
# without its changelog entry.
set -euo pipefail

version="${1:?usage: $0 <version>}"
changelog="$(dirname "$0")/../CHANGELOG.md"

notes="$(awk -v version="$version" '
  /^## \[/ {
    if (found) exit
    if (index($0, "## [" version "]") == 1) { found = 1; next }
  }
  found && /^\[[^]]+\]: / { exit }
  found { print }
' "$changelog")"

if [ -z "${notes//[[:space:]]/}" ]; then
  echo "CHANGELOG.md has no section for version $version" >&2
  exit 1
fi

printf '%s\n' "$notes" | sed -e '/./,$!d'
