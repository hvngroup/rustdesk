#!/usr/bin/env bash
# Package an app into a compressed disk image with an Applications shortcut.
#
# Usage: scripts/make-dmg.sh "release/HVN Remote Hub.app" release/HVNRemoteHub-1.0.0.dmg
set -euo pipefail

app="${1:?usage: $0 <app> <output.dmg>}"
output="${2:?usage: $0 <app> <output.dmg>}"
name="$(basename "$app" .app)"

staging="$(mktemp -d)"
trap 'rm -rf "$staging"' EXIT
# ditto keeps the signature, extended attributes and resource forks.
ditto "$app" "$staging/$name.app"
ln -s /Applications "$staging/Applications"
rm -f "$output"
hdiutil create -volname "$name" -srcfolder "$staging" -ov -format UDZO "$output"
echo "Disk image ready: $output"
