#!/usr/bin/env bash
# Build "release/HVN Remote Hub.app" from the Swift package. No Windows code
# is executed or bundled.
#
# Usage: scripts/package-app.sh [release|debug]
#
# Environment:
#   HVN_UNIVERSAL=1          build arm64 + x86_64 (CI and releases do)
#   HVN_SIGNING_IDENTITY=…   codesign identity; "-" signs ad-hoc
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
configuration="${1:-release}"
if [ "$configuration" != "release" ] && [ "$configuration" != "debug" ]; then
  echo "Usage: scripts/package-app.sh [release|debug]" >&2
  exit 2
fi

# shellcheck source=../version.conf
. "$root/version.conf"
: "${APP_VERSION:?version.conf must set APP_VERSION}"
: "${APP_BUILD:?version.conf must set APP_BUILD}"

product="HVNRemoteHub"
app_name="HVN Remote Hub"
output="$root/release"
app="$output/$app_name.app"
mkdir -p "$output"

# Keep one local signing identity across builds so macOS keeps the Screen
# Recording and Accessibility grants: a lone "Apple Development" identity if
# the Mac has one, otherwise ad-hoc. CI passes the identity explicitly.
identity_file="$output/.signing-identity"
signing_identity="${HVN_SIGNING_IDENTITY:-}"
if [ -z "$signing_identity" ] && [ -f "$identity_file" ]; then
  signing_identity="$(cat "$identity_file")"
fi
if [ -z "$signing_identity" ]; then
  identities="$(security find-identity -v -p codesigning 2>/dev/null | awk '/"Apple Development:/{print $2}' || true)"
  if [ "$(printf '%s\n' "$identities" | grep -c .)" = "1" ]; then
    signing_identity="$identities"
  else
    signing_identity="-"
  fi
fi

build_flags=(--configuration "$configuration")
if [ "${HVN_UNIVERSAL:-0}" = "1" ]; then
  build_flags+=(--arch arm64 --arch x86_64)
fi
swift build "${build_flags[@]}" --product "$product"
binaries="$(swift build "${build_flags[@]}" --show-bin-path)"

rm -rf "$app"
contents="$app/Contents"
resources="$contents/Resources"
mkdir -p "$contents/MacOS" "$resources"

cp "$binaries/$product" "$contents/MacOS/$product"
iconutil -c icns "$root/Resources/AppIcon.iconset" -o "$resources/AppIcon.icns"
for language in vi en; do
  mkdir -p "$resources/$language.lproj"
  cp "Sources/$product/Resources/$language.lproj/Localizable.strings" "$resources/$language.lproj/"
  cp "Resources/InfoPlist/$language.lproj/InfoPlist.strings" "$resources/$language.lproj/"
done
cp -R "$binaries/${product}_${product}.bundle" "$resources/"
cp Sources/UltraViewerProtocol/Resources/8bit.dat "$resources/8bit.dat"
cp Resources/Brand/hvn-logo-color.png Resources/Brand/hvn-logo-white.png "$resources/"
cp docs/user-guide.md "$resources/user-guide.md"

licenses="$resources/Licenses"
mkdir -p "$licenses/HVN Remote Hub" "$licenses/Zstandard" "$licenses/G722"
cp LICENSE THIRD_PARTY_NOTICES.md "$licenses/HVN Remote Hub/"
cp ThirdParty/zstd/LICENSE ThirdParty/zstd/COPYING "$licenses/Zstandard/"
cp ThirdParty/g722/LICENSE ThirdParty/g722/WEBRTC_LICENSE "$licenses/G722/"

cat > "$contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key><string>$product</string>
  <key>CFBundleIdentifier</key><string>vn.hvn.remotehub</string>
  <key>CFBundleName</key><string>$app_name</string>
  <key>CFBundleDisplayName</key><string>$app_name</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleIconFile</key><string>AppIcon</string>
  <key>CFBundleDevelopmentRegion</key><string>vi</string>
  <key>CFBundleLocalizations</key><array><string>vi</string><string>en</string></array>
  <key>CFBundleShortVersionString</key><string>$APP_VERSION</string>
  <key>CFBundleVersion</key><string>$APP_BUILD</string>
  <key>LSApplicationCategoryType</key><string>public.app-category.utilities</string>
  <key>LSMinimumSystemVersion</key><string>14.0</string>
  <key>NSHighResolutionCapable</key><true/>
  <key>NSPrincipalClass</key><string>NSApplication</string>
  <key>NSLocalNetworkUsageDescription</key><string>HVN Remote Hub connects directly to computers on your local network when that is faster than the relay.</string>
  <key>NSHumanReadableCopyright</key><string>© 2026 HVN GROUP · hvn.vn</string>
</dict>
</plist>
PLIST
plutil -lint "$contents/Info.plist"

codesign --force --sign "$signing_identity" --timestamp=none "$app"
codesign --verify --deep --strict "$app"
# Signing leaves the bundle folder's timestamp unchanged, so Finder can keep
# showing the first build's generic icon. Timestamps are not signed content.
touch "$contents" "$app"
lsregister="/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister"
if [ "${CI:-}" != "true" ] && [ -x "$lsregister" ]; then
  "$lsregister" -f "$app"
fi
printf '%s\n' "$signing_identity" > "$identity_file"
echo "App ready: $app ($APP_VERSION build $APP_BUILD, signed with '$signing_identity')"
