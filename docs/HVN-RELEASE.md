# Phát hành HVN Remote Hub

Bản HVN Remote Hub được phát hành qua [GitHub Releases của hvngroup/rustdesk](https://github.com/hvngroup/rustdesk/releases).
Workflow `Flutter Tag Build` (`.github/workflows/flutter-tag.yml`) build mọi nền tảng và tự đính file vào Release khi có tag mới.

## Cách ra một bản

1. Kiểm tra phiên bản. `VERSION` trong `.github/workflows/flutter-build.yml` phải trùng `version` trong `Cargo.toml`.
   Đây là phiên bản RustDesk mà bản fork dựa trên. Máy hai đầu dùng số này để biết bên kia hỗ trợ tính năng nào, nên không đổi tuỳ ý.
2. Đặt tag theo dạng `v<phiên bản>-<số bản HVN>`, ví dụ `v1.5.1-1`, rồi `v1.5.1-2` cho lần build lại trên cùng phiên bản đó.
   Workflow chỉ nhận các dạng `1.5.1`, `v1.5.1`, `1.5.1-1` và `v1.5.1-1`.
3. Tạo Release trên GitHub với tag mới, target `master`. Workflow sẽ chạy khoảng 1 giờ rồi đính các file vào Release.
4. Workflow đánh dấu Release là *Pre-release*. Sau khi kiểm tra file cài trên máy thật, bỏ dấu Pre-release để thành bản chính thức.

## Tên file

Mọi file tải về có dạng `HVNRemoteHub-<phiên bản>-<kiến trúc>.<đuôi>`:

| Nền tảng | File |
|---|---|
| Windows | `HVNRemoteHub-1.5.1-x86_64.exe` (chạy ngay hoặc cài), `HVNRemoteHub-1.5.1-x86_64.msi`, bản `aarch64` tương tự; `HVNRemoteHub-1.5.1-x86-sciter.exe` là bản 32-bit giao diện cũ (Sciter) |
| macOS | `HVNRemoteHub-1.5.1-aarch64.dmg`, `HVNRemoteHub-1.5.1-x86_64.dmg` |
| Android | `HVNRemoteHub-1.5.1-aarch64.apk`, `-armv7.apk`, `-x86_64.apk`, `-universal.apk` |
| Linux | `.deb`, `.rpm` (Fedora và `-suse`), `.pkg.tar.zst` (Arch), `.AppImage`, `.flatpak` |
| Linux, bản cho Wayland không cần xác nhận | `hvnremotehub-unattended-wayland-1.5.1-x86_64.deb`, mang đúng tên gói người dùng đồng ý khi cài |

Kèm theo là `HVNRemoteHub.sbom.json` (danh sách thành phần phần mềm) và mã nguồn GitHub tự tạo, đáp ứng AGPL-3.0.

## Cập nhật trong app

App không tự cập nhật. Dịch vụ cập nhật của RustDesk chỉ biết các bản RustDesk gốc, nên bản HVN tắt cả việc kiểm tra lẫn ô *Tự động cập nhật*.
Người dùng tải bản mới từ trang Releases. Muốn có cập nhật tự động, HVN cần dựng dịch vụ phiên bản và khoá ký riêng.

## Bản nightly

`Flutter Nightly Build` build hằng ngày lúc 0:00 UTC vào tag `nightly`. GitHub tắt lịch chạy của repo fork cho đến khi bật trong tab Actions.
Có thể chạy tay bằng *Run workflow*.

## Ký số

Thiếu secret thì CI vẫn build và phát hành, nhưng file chưa được ký:

- Windows ký qua `SIGN_BASE_URL` và `SIGN_SECRET_KEY`.
- macOS ký và notarize qua `MACOS_P12_BASE64` và các secret Apple đi kèm.
- Android ký qua `ANDROID_SIGNING_KEY`, `ANDROID_ALIAS`, `ANDROID_KEY_STORE_PASSWORD` và `ANDROID_KEY_PASSWORD`.

Bản chưa ký sẽ bị Windows SmartScreen và macOS Gatekeeper cảnh báo.
