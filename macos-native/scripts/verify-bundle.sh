#!/usr/bin/env bash
# Check every packaging assumption of "HVN Remote Hub.app", one line each, so
# a wrong path or a missing resource fails CI instead of a user's Mac.
#
# Usage: scripts/verify-bundle.sh "release/HVN Remote Hub.app" [arm64 x86_64]
set -euo pipefail

app="${1:?usage: $0 <app> [architectures…]}"
shift
architectures=("$@")
[ ${#architectures[@]} -gt 0 ] || architectures=(arm64)

root="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=../version.conf
. "$root/version.conf"
plist="$app/Contents/Info.plist"
resources="$app/Contents/Resources"
binary="$app/Contents/MacOS/HVNRemoteHub"

value() { /usr/libexec/PlistBuddy -c "Print :$1" "$plist"; }
check() { if "$@"; then echo "ok   $*"; else echo "FAIL $*" >&2; exit 1; fi; }

check codesign --verify --deep --strict "$app"
check test -x "$binary"
check test "$(value CFBundleIdentifier)" = "vn.hvn.remotehub"
check test "$(value CFBundleDisplayName)" = "HVN Remote Hub"
check test "$(value CFBundleShortVersionString)" = "$APP_VERSION"
check test "$(value CFBundleVersion)" = "$APP_BUILD"
check test "$(value CFBundleDevelopmentRegion)" = "vi"
check test "$(value LSMinimumSystemVersion)" = "14.0"
for architecture in "${architectures[@]}"; do
  check grep -qw "$architecture" <<<"$(lipo -archs "$binary")"
done
check test -f "$resources/AppIcon.icns"
for language in vi en; do
  check test -f "$resources/$language.lproj/Localizable.strings"
  check test -f "$resources/$language.lproj/InfoPlist.strings"
done
check test -d "$resources/HVNRemoteHub_HVNRemoteHub.bundle"
check test "$(shasum -a 256 "$resources/8bit.dat" | cut -d' ' -f1)" = \
  "9aa45789d9ff9d329a623a685d57b67e33c777019de9ce1f273f21860e4bfe6b"
check test -f "$resources/hvn-logo-color.png"
check test -f "$resources/hvn-logo-white.png"
check test -f "$resources/user-guide.md"
check test -f "$resources/Licenses/HVN Remote Hub/LICENSE"
check test -f "$resources/Licenses/HVN Remote Hub/THIRD_PARTY_NOTICES.md"
check test -f "$resources/Licenses/Zstandard/LICENSE"
check test -f "$resources/Licenses/G722/WEBRTC_LICENSE"
du -sh "$app"
