# Phase P2 — Đổi thương hiệu bản fork RustDesk thành HVN Remote Hub

- Repo: `hvngroup/rustdesk` (fork của `rustdesk/rustdesk`, bản 1.5.1 trên `master`, commit `4b92080`, 2026-10-20)
- Nhánh làm việc: `claude/clever-turing-ns95e6` → PR vào `master` của fork
- Quy tắc của repo: `AGENTS.md` (thay đổi tối thiểu, thêm mới thay vì sửa đường cũ, `hbb_common` là submodule — tránh sửa)

## Phát hiện khi rà mã (2026-10-20)

| Hạng mục | Hiện trạng | Cách đổi |
|---|---|---|
| Tên app, tổ chức | `APP_NAME = "RustDesk"`, `ORG = "com.carriez"` trong `hbb_common` (dạng `RwLock`, ghi được lúc chạy) | Ghi đè lúc khởi động bằng một mô-đun HVN trong `src/`, gọi ngay sau `load_custom_client()` ở `src/core_main.rs` và `src/flutter_ffi.rs` → **không cần sửa `hbb_common`** |
| Máy chủ, khoá | `RENDEZVOUS_SERVERS = ["rs-ny.rustdesk.com"]`, `RS_PUB_KEY` là hằng trong `hbb_common`; có sẵn các tuỳ chọn `custom-rendezvous-server`, `relay-server`, `key` và bảng `OVERWRITE_SETTINGS`/`BUILTIN_SETTINGS` | Cùng mô-đun HVN đặt `connect.hvn.vn` và khoá công khai lấy lúc build (biến môi trường, CI chặn bản phát hành khi thiếu) |
| Custom client của RustDesk | `custom.txt` phải có chữ ký của khoá RustDesk → **không dùng được** cho bản fork | Dùng mô-đun HVN ở trên |
| Bundle ID | macOS `com.carriez.rustdesk`, iOS `com.carriez.flutterHbb`, Android `com.carriez.flutter_hbb` | `vn.hvn.remotehub` trên cả ba (Android: `vn.hvn.remotehub`) |
| Icon, logo | `res/icon.png`, `res/mac-icon.png`, `res/icon.ico`, `res/logo*.svg`, icon trong `flutter/*` | Bộ icon HVN (đỏ `#EA4445`, dấu HVN GROUP) từ `scripts/make-app-icon.py` của app Mac |
| Chữ "RustDesk" | Khoảng 170 file ngoài bản dịch (Flutter UI, platform, installer MSI/DEB, fastlane, workflow) | Đổi chữ người dùng thấy; giữ ghi công và thông báo AGPL ở màn Giới thiệu |
| Tiếng Việt | `src/lang/vi.rs` đã dịch 777/812 khoá (35 khoá trống) | Dịch nốt 35 khoá; đặt tiếng Việt mặc định |
| Cập nhật, link ngoài | Kiểm tra bản mới, tài trợ, tài liệu trỏ về rustdesk.com | Trỏ về Releases của HVN, hvn.vn, kythuat@hvn.vn |
| CI | `flutter-build.yml` (~2.900 dòng, nhiều runner, 23 chỗ dùng secrets), `flutter-ci.yml` chạy trên PR | Bật Actions trên fork; giữ CI gốc, thêm bước ký số HVN ở P3 |

## Chia nhỏ thành các PR

1. **P2a — Danh tính và máy chủ:** mô-đun HVN (tên app, `ORG`, `connect.hvn.vn`, khoá), bundle ID ba nền tảng, icon. Test
   Rust cho phần ghi đè cài đặt.
2. **P2b — Chữ và ngôn ngữ:** đổi "RustDesk" trong giao diện, tiếng Việt mặc định, dịch 35 khoá còn thiếu, màn Giới thiệu có
   ghi công RustDesk + AGPL + liên hệ HVN.
3. **P2c — Kênh cập nhật và link:** trỏ về Releases của HVN, gỡ link tài trợ/tài liệu của RustDesk.

Mỗi PR phải có `flutter-ci.yml` xanh trước khi merge. Agent không build được trên Linux container (thiếu vcpkg/Flutter
toolchain đầy đủ), nên CI của fork là nơi chứng minh build.

## Điều kiện để bắt đầu

- [ ] **Bật GitHub Actions trên fork** (*Actions → I understand my workflows, go ahead and enable them*). Fork mặc định tắt
      Actions; không có CI thì không chứng minh được build.
- [ ] **Khoá công khai `id_ed25519.pub`** từ máy chủ P0 trên `connect.hvn.vn` (không bắt buộc cho P2a nếu CI chỉ build
      thử; bắt buộc trước khi phát hành).
- [x] Fork `rustdesk/rustdesk` → `hvngroup/rustdesk`, đã thêm vào phiên agent.
- [ ] Fork `hbb_common`, `rustdesk-server`: **chưa cần** nhờ cách ghi đè lúc chạy ở trên, và máy chủ thử nghiệm dùng image
      chính thức. Chỉ cần khi HVN muốn sửa giao thức hoặc máy chủ.

## Hoàn tác

Mỗi PR độc lập, đóng PR là hoàn tác; `master` của fork không đổi cho đến khi merge.

---

HVN GROUP · hvn.vn
