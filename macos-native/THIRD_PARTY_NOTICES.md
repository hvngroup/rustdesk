# Third-party software

## MacViewer

HVN Remote Hub is based on [MacViewer](https://github.com/hvngroup/macviewer)
(commit `f8d1b6529e673df3fe35fccdd4b65f7474e354b7`), copyright 2026 MacViewer
contributors, under the MIT License. The protocol engine
(`Sources/UltraViewerProtocol`), the application code it was derived from and
their tests keep that notice in `LICENSE`. The packaging script copies
`LICENSE` and this file into
`HVN Remote Hub.app/Contents/Resources/Licenses/HVN Remote Hub/`.

## Zstandard

HVN Remote Hub statically includes compression and decompression portions of
[Zstandard 1.5.7](https://github.com/facebook/zstd/tree/v1.5.7), copyright Meta
Platforms, Inc. and affiliates, under its BSD license. The source's alternative
GPLv2 license is also preserved. Original notices are in
`ThirdParty/zstd/LICENSE` and `ThirdParty/zstd/COPYING`, and the packaging script
copies both into `Contents/Resources/Licenses/Zstandard/`.

Upstream source files are unmodified. `ThirdParty/zstd/provenance.json` records
the exact release, acquisition URL, archive digest and selected files. The local
module entry point is `ThirdParty/zstd/include/CZstd.h`. The build includes
compression, decompression and legacy formats 4–7 and disables
architecture-specific assembly.

## G.722

Computer audio decoding includes the WebRTC G.722 decoder from revision
`4fdd50a57b79826ea87cc5170be78b6444d9cdf9`. Its original public-domain notice
and WebRTC BSD license are preserved in `ThirdParty/g722/LICENSE` and
`ThirdParty/g722/WEBRTC_LICENSE`, and copied into the app's
`Contents/Resources/Licenses/G722/` folder. `ThirdParty/g722/provenance.json`
records the upstream source URLs and digests. `MacViewerG722.c` is MacViewer's
allocation-checked wrapper.

## UltraViewer screen dictionary

The application includes the UltraViewer-supplied `8bit.dat` Zstandard decoding
dictionary as data at `Contents/Resources/8bit.dat`. It is 112,640 bytes with
SHA-256 `9aa45789d9ff9d329a623a685d57b67e33c777019de9ce1f273f21860e4bfe6b`
and dictionary ID `0x3da0bd10`. It is not an independently authored or
open-source dictionary, and no redistribution license for it has been
established. It is not covered by the MIT License. No Windows executable code
is embedded in or executed by the application.

"UltraViewer" is a trademark of its respective owner and is used only to
describe compatibility.
