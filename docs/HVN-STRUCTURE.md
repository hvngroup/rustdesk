# Cấu trúc dự án HVN Remote Hub

Repo `hvngroup/universal-remote-hub` chứa cả hai thế hệ của HVN Remote Hub:

| | HVN Remote Hub 2.0 | HVN Remote Hub for Mac 1.x |
|---|---|---|
| Thư mục | Gốc repo (`src/`, `libs/`, `flutter/`, …) | `macos-native/` |
| Nguồn gốc | Fork của RustDesk 1.5.1 | MacViewer (MIT) và phần HVN viết thêm |
| Kết nối tới | Máy chạy HVN Remote Hub qua máy chủ `connect.hvn.vn` | Máy chạy UltraViewer |
| Nền tảng | Windows, macOS, Linux, Android, iOS | macOS 14 trở lên |
| Công nghệ | Lõi Rust + giao diện Flutter | Swift 6, SwiftUI + AppKit, engine Swift/C |
| Giấy phép | AGPL-3.0 (`LICENCE`) | MIT (`macos-native/LICENSE`) |
| Tag phát hành | `v1.5.1-1`, `v1.5.1-2`, … | `mac-v1.0.2`, … |
| Hướng dẫn phát hành | [docs/HVN-RELEASE.md](HVN-RELEASE.md) | [macos-native/docs/release.md](../macos-native/docs/release.md) |

Theo kế hoạch 2.0 ([macos-native/plans/261020-1227-hvn-protocol-multiplatform](../macos-native/plans/261020-1227-hvn-protocol-multiplatform/plan.md), hướng A1), bản Flutter 2.0 sẽ là HVN Remote Hub trên mọi nền tảng. App Swift sẽ thu về thành mô-đun UltraViewer chỉ dùng trên macOS. Mã MIT gộp được vào dự án AGPL; chiều ngược lại thì không.

## Cây thư mục gốc

```
universal-remote-hub/
├── src/                    Lõi Rust của app 2.0 (client + phần bị điều khiển)
├── libs/                   Các crate Rust dùng chung
├── flutter/                Giao diện Flutter và project từng nền tảng
├── res/                    Icon, gói Linux, bộ cài Windows (MSI), script phụ trợ
├── appimage/  flatpak/     Công thức đóng gói Linux AppImage và Flatpak
├── fastlane/               Metadata cho F-Droid (vẫn của RustDesk)
├── examples/               Ví dụ dùng thư viện
├── macos-native/           App Mac 1.x (Swift), độc lập với phần còn lại
├── docs/                   Tài liệu (HVN-*.md là của HVN, phần còn lại của RustDesk)
├── .github/workflows/      CI/CD cho cả hai app
├── build.py  build.rs      Script build của RustDesk (Python) và build script của Cargo
├── Cargo.toml  Cargo.lock  Workspace Rust; version = 1.5.1
├── vcpkg.json              Thư viện C/C++ (libvpx, libyuv, opus, aom) cài qua vcpkg
├── AGENTS.md  CLAUDE.md    Quy tắc viết mã cho người và agent
└── LICENCE                 AGPL-3.0
```

## HVN Remote Hub 2.0

### Lõi Rust (`src/`)

| Đường dẫn | Vai trò |
|---|---|
| `main.rs`, `core_main.rs` | Điểm vào: đọc tham số dòng lệnh (`--server`, `--service`, `--install`, …), khởi động đúng tiến trình |
| `hvn.rs` | **Danh tính HVN**: tên nội bộ `HVNRemoteHub`, tên hiển thị "HVN Remote Hub", máy chủ `connect.hvn.vn` và khoá công khai của máy chủ (đổi lúc build bằng biến `HVN_RENDEZVOUS_SERVER` và `HVN_RS_PUB_KEY`), tiếng Việt mặc định. `apply()` chạy lúc khởi động |
| `flutter_ffi.rs`, `flutter.rs` | Cầu nối Rust ↔ Dart. Các hàm `main_*`/`session_*` là API mà giao diện gọi |
| `ui_interface.rs`, `ui_session_interface.rs`, `ui_cm_interface.rs` | Logic dùng chung cho giao diện: cài đặt, phiên điều khiển, cửa sổ quản lý kết nối |
| `client.rs`, `client/` | Phía điều khiển: kết nối, giải mã video, gửi chuột và bàn phím, truyền file |
| `server.rs`, `server/` | Phía bị điều khiển: `connection.rs` (phiên), `video_service` (chụp màn hình), `audio_service`, `input_service`, `clipboard_service`, `printer_service`, `terminal_service`, Wayland/DRM |
| `rendezvous_mediator.rs` | Đăng ký ID và giữ kết nối với máy chủ rendezvous (`hbbs`), hole punching, relay (`hbbr`) |
| `platform/` | Mã riêng từng hệ điều hành: `windows.rs`, `macos.rs`/`macos.mm`, `linux.rs`, quyền, dịch vụ, cài đặt |
| `ipc.rs`, `ipc/` | Giao tiếp giữa các tiến trình (giao diện ↔ dịch vụ nền) |
| `keyboard.rs`, `keyboard/` | Ánh xạ bàn phím giữa các hệ điều hành |
| `privacy_mode.rs`, `virtual_display_manager.rs`, `whiteboard/` | Chế độ riêng tư, màn hình ảo, bảng vẽ |
| `updater.rs`, `update_metadata.rs`, `manual_update.rs` | Cơ chế cập nhật của RustDesk. **Đã tắt** cho bản HVN, vì nó chỉ biết bản RustDesk gốc |
| `lang.rs`, `lang/*.rs` | Bản dịch giao diện. `vi.rs` đã điền đủ chuỗi; `template.rs` là danh sách khoá gốc |
| `custom_server.rs` | Đọc cấu hình máy chủ từ tên file `.exe` (kiểu `…-host=…,key=….exe`) |
| `ui/`, `ui.rs` | Giao diện Sciter cũ (đã ngừng phát triển), chỉ còn dùng cho bản 32-bit |

### Thư viện (`libs/`)

| Crate | Vai trò |
|---|---|
| `hbb_common` | **Git submodule dùng chung với máy chủ.** Gồm protobuf (`rendezvous.proto`, `message.proto`), socket, mã hoá, `Config`. Hạn chế sửa ở đây |
| `base` | Phần chỉ client dùng: khoá tuỳ chọn (`config/keys.rs`), message proto, truyền file |
| `scrap` | Chụp màn hình và codec (VP8/VP9/AV1, mã hoá phần cứng) |
| `enigo` | Giả lập chuột và bàn phím |
| `clipboard` | Clipboard và copy/paste file |
| `virtual_display`, `remote_printer` | Driver màn hình ảo và máy in từ xa (Windows) |
| `portable` | Trình đóng gói file `.exe` chạy ngay không cần cài |

### Giao diện Flutter (`flutter/`)

| Đường dẫn | Vai trò |
|---|---|
| `lib/main.dart` | Điểm vào, khởi tạo cửa sổ |
| `lib/desktop/` | Màn hình desktop: `pages/` (trang chính, cài đặt, phiên điều khiển, truyền file, cài đặt Windows), `widgets/` |
| `lib/mobile/` | Màn hình Android/iOS |
| `lib/common/`, `lib/models/` | Widget và model dùng chung (sổ địa chỉ, chat, phiên, file) |
| `lib/web/bridge.dart` | Cầu nối cho bản web; bản này viết tay vì không chạy Rust |
| `windows/`, `macos/`, `linux/`, `android/`, `ios/` | Project của từng nền tảng. Đây là nơi đặt danh tính HVN: tên `HVNRemoteHub`, bundle ID/applicationId `vn.hvn.remotehub`, scheme `hvnremotehub://`, team Apple `TVZNQ5W8NG` |
| `test/` | Test Dart, chạy bằng `flutter test` |

`flutter/lib/generated_bridge.dart` và `src/bridge_generated*.rs` do CI sinh tự động, không nằm trong repo.

### Đóng gói (`res/`, `appimage/`, `flatpak/`)

| Đường dẫn | Vai trò |
|---|---|
| `res/hvn_icons.py` | Sinh mọi icon HVN (app, tray, installer, Android) từ logo HVN GROUP |
| `res/msi/` | Bộ cài Windows (WiX). `preprocess.py` đặt tên app, nhà phát hành "HVN GROUP" và liên kết trong Apps & Features |
| `res/DEBIAN/`, `res/*.spec`, `res/PKGBUILD` | Gói Linux deb, rpm và Arch: tên gói `hvnremotehub`, dịch vụ `hvnremotehub.service` |
| `appimage/`, `flatpak/` | AppImage (`app_info.name: HVNRemoteHub`) và Flatpak (`vn.hvn.remotehub`) |
| `build.py` | Build Rust và Flutter rồi đóng gói theo từng nền tảng. CI gọi script này |

## HVN Remote Hub for Mac 1.x (`macos-native/`)

```
macos-native/
├── Package.swift            SwiftPM: target UltraViewerProtocol, HVNRemoteHub và 2 target test
├── version.conf             APP_VERSION / APP_BUILD, nơi duy nhất ghi phiên bản
├── CHANGELOG.md             Workflow lấy mô tả Release từ đây
├── Sources/
│   ├── UltraViewerProtocol/ Engine giao thức: tra cứu ID, đăng nhập mã hoá, relay TLS,
│   │                        kết nối LAN, giải mã màn hình (zstd), âm thanh G.722, chat, clipboard
│   └── HVNRemoteHub/        App SwiftUI/AppKit: cửa sổ kết nối, màn hình điều khiển, chia sẻ Mac,
│                            quyền hệ thống, giới thiệu/trợ giúp, UpdateChecker (đọc tag mac-v…)
├── ThirdParty/              zstd, g722 (mã C, kèm giấy phép)
├── Resources/               Icon, logo, InfoPlist, bản dịch vi/en
├── Tests/                   Test Swift Testing
├── scripts/                 package-app.sh, make-dmg.sh, verify-bundle.sh, release-notes.sh,
│                            check-localizations.py, make-app-icon.py
├── docs/                    development.md, user-guide.md, release.md, manual-test-checklist.md
└── plans/                   Kế hoạch: viết lại UltraViewer, giao thức HVN đa nền tảng (2.0)
```

## CI/CD (`.github/workflows/`)

| Workflow | Khi nào chạy | Làm gì |
|---|---|---|
| `ci.yml` | PR và push lên `master` (bỏ qua `macos-native/**`) | Build và chạy test Rust (`cargo test`) trên Linux |
| `flutter-ci.yml` | PR và push lên `master` (bỏ qua `macos-native/**`) | Gọi `flutter-build.yml` để build đủ nền tảng, không phát hành |
| `flutter-tag.yml` | Tag `v1.5.1-N` | Build và đính `HVNRemoteHub-<phiên bản>-<kiến trúc>.*` vào Release (Pre-release) |
| `flutter-nightly.yml` | Hằng ngày (cần bật trong tab Actions) hoặc chạy tay | Build vào tag `nightly` |
| `flutter-build.yml` | Được 3 workflow trên gọi | Build Windows, macOS, Linux, Android; iOS, AppImage, Flatpak chỉ build khi phát hành, và file IPA của iOS chưa được đăng |
| `macos-native.yml` | PR/push chạm `macos-native/**`, tag `mac-v*`, chạy tay | Test Swift, đóng gói, ký Developer ID và notarize, đính DMG/zip vào Release "HVN Remote Hub for Mac X.Y.Z" |
| `bridge.yml` | Được gọi | Sinh cầu nối Rust ↔ Dart |
| `fdroid.yml`, `playground.yml`, `update-webpki-roots.yml`, `clear-cache.yml` | Theo tag, theo lịch hoặc chạy tay | Tiện ích của RustDesk |

**Secrets:**

- App 2.0 dùng `SIGN_BASE_URL` và `SIGN_SECRET_KEY` (Windows), `MACOS_P12_BASE64` cùng các secret Apple (macOS), và `ANDROID_SIGNING_KEY` cùng các secret đi kèm (Android).
- App Mac 1.x dùng `MACOS_CERTIFICATE_P12`, `MACOS_CERTIFICATE_PASSWORD` và `APPSTORE_API_KEY_*`.
- Cả hai nhóm phải được thêm vào repo này. Secrets không đi theo khi gộp repo.

## Máy chủ

App 2.0 kết nối tới `connect.hvn.vn`, gồm `hbbs` để đăng ký ID và `hbbr` để relay, lấy từ `rustdesk-server` (AGPL). Máy chủ không nằm trong repo này. Khoá công khai của máy chủ được đưa vào lúc build qua biến `HVN_RS_PUB_KEY`.

## Lưu ý đã biết

- **Hai app Mac trùng bundle ID `vn.hvn.remotehub`.** Bản 1.x ("HVN Remote Hub.app") và bản 2.0 ("HVNRemoteHub.app") dùng chung cài đặt và chung quyền Ghi màn hình/Trợ năng, và macOS coi chúng là một app. Cần đổi bundle ID của một trong hai trước khi phát hành bản 2.0 cho macOS.
- Trang Giới thiệu, chính sách quyền riêng tư và metadata F-Droid trong app 2.0 vẫn trỏ về RustDesk.
- App 2.0 không tự cập nhật. Muốn có, cần dựng dịch vụ phiên bản và khoá ký riêng của HVN.
