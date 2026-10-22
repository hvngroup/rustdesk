# Phát triển HVN Remote Hub

## Cấu trúc

```
Package.swift                 Swift package: app, engine, 2 thư viện C, 2 bộ test
version.conf                  APP_VERSION / APP_BUILD — nguồn phiên bản duy nhất
Sources/
  HVNRemoteHub/             App SwiftUI/AppKit: giao diện, chụp/nhận màn hình, nhập liệu, chia sẻ Mac, cập nhật
    Resources/{vi,en}.lproj/  Chuỗi giao diện (khoá tiếng Anh, bản dịch tiếng Việt)
  UltraViewerProtocol/        Engine giao thức: mã hoá, relay, codec màn hình, âm thanh, clipboard, chat
ThirdParty/
  zstd/                       Zstandard 1.5.7 (BSD / GPLv2), không sửa
  g722/                       Bộ giải mã G.722 của WebRTC + lớp bọc MacViewerG722.c
Resources/
  AppIcon.iconset/            Icon app (sinh bằng scripts/make-app-icon.py)
  Brand/                      Logo HVN GROUP: SVG chuẩn + PNG render sẵn
  InfoPlist/{vi,en}.lproj/    Lời nhắc quyền riêng tư trong Info.plist
Tests/
  UltraViewerProtocolTests/   Test engine (giao thức, codec, mã hoá)
  HVNRemoteHubTests/        Test logic app (ngôn ngữ, cập nhật, nhập liệu, kết nối)
scripts/                      Đóng gói, kiểm tra bundle, DMG, release notes, icon, logo, kiểm tra bản dịch
docs/                         Tài liệu người dùng và nhà phát triển
plans/                        Kế hoạch và báo cáo (phạm vi, review)
```

Engine được chuyển nguyên trạng từ MacViewer (MIT); phần HVN viết lại là vỏ app (khởi chạy, menu, Giới thiệu, Trợ
giúp, Cài đặt, tiếng Việt mặc định, brand), kênh cập nhật, đóng gói và CI.

## Build và test

Cần macOS 14+ và Xcode 16+ (Swift 6, chế độ ngôn ngữ Swift 6 — kiểm tra concurrency nghiêm ngặt).

```sh
swift test --parallel               # toàn bộ test
scripts/package-app.sh release      # "release/HVN Remote Hub.app", ký ad-hoc hoặc Apple Development
HVN_UNIVERSAL=1 scripts/package-app.sh release   # arm64 + x86_64 như CI
scripts/verify-bundle.sh "release/HVN Remote Hub.app" arm64
open "release/HVN Remote Hub.app"
```

`scripts/package-app.sh` giữ một danh tính ký cố định giữa các lần build (file `release/.signing-identity`) để macOS
không đòi cấp lại quyền Ghi màn hình/Trợ năng. Có đúng một chứng chỉ "Apple Development" thì dùng nó, không thì ký ad-hoc.

Chạy được trên Linux (không cần Xcode):

```sh
python3 scripts/check-localizations.py   # khoá vi/en khớp, đối số định dạng khớp
python3 scripts/make-app-icon.py         # vẽ lại icon (cần Pillow)
node scripts/render-brand-logos.mjs      # render lại logo PNG từ SVG (cần Playwright)
scripts/release-notes.sh 1.0.0           # in mục CHANGELOG của một phiên bản
```

## Quy ước

- **Chuỗi giao diện:** viết tiếng Anh trong code; thêm khoá vào **cả hai** `Localizable.strings` (`vi` dịch, `en`
  giữ nguyên hoặc chỉnh câu). Menu và chuỗi ngoài SwiftUI dùng `L("…")` / `LF("…", …)`; `Text("…")` tự tra theo
  locale môi trường. CI chạy `check-localizations.py` và test `AppLocalizationTests`.
- **Tên riêng** (HVN Remote Hub, HVN GROUP, hvn.vn) dùng `Text(verbatim:)` hoặc hằng trong `Brand`.
- **Khoá UserDefaults** có tiền tố `HVNRemoteHub.`; Keychain service `vn.hvn.remotehub.partner`.
- **Tài nguyên trong app:** đọc từ `Bundle.main` (script đóng gói chép vào `Contents/Resources`). Không gọi
  `Bundle.module` trong app đã đóng gói.
- **Concurrency:** lớp chạm AppKit/SwiftUI đánh dấu `@MainActor`; callback hệ thống quay về main bằng
  `Task { @MainActor in … }`.
- **Bảo mật (ATTT HVN 01-01/11/2024):** không commit chứng chỉ, khoá, mật khẩu, ID đối tác, token phiên, file
  `registration*.json` hay ảnh chụp giao thức. Bật ghi khung giao thức (`HVNRemoteHub.captureProtocolFrames`) chỉ
  trên máy phát triển.
- Một PR một mục đích; thay đổi người dùng thấy được ghi vào mục `[Unreleased]` của `CHANGELOG.md`.

## CI

Workflow **Build** (`.github/workflows/build.yml`):

1. `checks` (Ubuntu): bản dịch khớp, script shell hợp lệ.
2. `app` (macOS 26, Xcode mới nhất): `swift test` → đóng gói universal → (tag: ký Developer ID + notarize nếu có
   secrets) → `verify-bundle.sh` → DMG, zip, SHA-256 → artifact → (tag) đăng Release với mô tả từ CHANGELOG.

Agent làm việc trong container Linux không có Xcode: lỗi biên dịch chỉ lộ ra trên CI. Đọc log job, sửa đúng gốc, rà
các chỗ cùng mẫu trước khi đẩy lại.

---

HVN GROUP · hvn.vn
