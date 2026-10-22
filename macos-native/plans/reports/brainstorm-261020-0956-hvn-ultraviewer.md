# Brainstorm — HVN UltraViewer for Mac

- Ngày: 2026-10-20
- Repo: `hvngroup/mac-ultra-viewer` (trống khi bắt đầu)
- Trạng thái: **Đã chốt** (Cổng ① Phạm vi — chủ sản phẩm trả lời ngày 2026-10-20)
- Quy trình: HVN App Builder Suite 1.0.2 (`ab-app-sop` → `ab-macos-native` → `ab-app-release`)
- Nguồn tham khảo: `hvngroup/macviewer` (bản sao của MacViewer, MIT, commit `f8d1b65`, 17/10/2026)

## Kết quả cần đạt (Outcome)

Nhân viên và khách hàng của HVN GROUP cài **HVN UltraViewer** trên Mac (macOS 14+, Apple silicon và Intel) từ GitHub
Releases của `hvngroup/mac-ultra-viewer`, rồi:

- điều khiển một máy đang chạy UltraViewer bằng ID và mật khẩu của máy đó;
- chia sẻ màn hình Mac của mình cho một máy UltraViewer khác, sau khi tự duyệt từng kết nối.

App mang nhận diện HVN GROUP (icon nền `#EA4445`, logo chuẩn, tiếng Việt mặc định, About/Help trỏ về hvn.vn và
kythuat@hvn.vn) và tự kiểm tra bản mới trên Releases của HVN.

## Ràng buộc (Constraints)

- **Nền tảng:** Swift 6 / SwiftUI + AppKit gốc, macOS 14 Sonoma trở lên (ScreenCaptureKit, `onChange` hai tham số mà
  mã nguồn tham khảo đang dùng). Bản phát hành là universal binary (arm64 + x86_64) như bản gốc.
- **Phân phối & ký số:** ký ad-hoc cho nội bộ (mặc định). Workflow phát hành tự ký Developer ID + notarize khi repo có
  secrets; không có secrets thì vẫn phát hành bản ad-hoc.
- **Môi trường phát triển:** agent làm việc trong container Linux không có Swift/Xcode → mọi khẳng định "build được"
  phải đến từ CI macOS trên commit hiện tại; "chạy được" phải do chủ sản phẩm xác nhận trên Mac thật (Cổng ③).
- **Giấy phép:** mã MacViewer là MIT — giữ nguyên thông báo bản quyền gốc trong `LICENSE` và `THIRD_PARTY_NOTICES.md`.
  zstd (BSD/GPLv2) và G.722 (WebRTC) giữ giấy phép riêng. `8bit.dat` là dữ liệu của UltraViewer, **không** thuộc MIT.
- **ATTT HVN 01-01/11/2024:** không commit secret, ID đối tác, mật khẩu, token phiên. Mật khẩu đối tác chỉ lưu trong
  Keychain khi người dùng bật.

## Ngoài phạm vi (Non-goals)

- Viết lại engine giao thức UltraViewer từ đầu: giao thức là dịch ngược, viết lại đồng nghĩa với sao chép lại cùng
  một hành vi. Engine được **chuyển nguyên trạng** từ tham khảo (chỉ đổi định danh nội bộ), có test đi kèm.
- Các tính năng bản gốc chưa có: truyền file, micro/voice chat, âm thanh từ Mac, chia sẻ nhiều màn hình, truy cập
  không cần duyệt (unattended).
- Sparkle: app đã có bộ cập nhật riêng (GitHub Releases + kiểm chữ ký Developer ID) đã chạy trên bản gốc; thêm
  Sparkle là trùng chức năng.
- Phát hành Mac App Store.

## Tiêu chí nghiệm thu (Acceptance criteria)

1. Kết nối tới máy UltraViewer bằng ID + mật khẩu; xem màn hình; bật **Điều khiển** để gửi bàn phím, chuột, cuộn.
2. Chia sẻ máy Mac: hướng dẫn cấp quyền Screen Recording và Accessibility; duyệt hoặc từ chối từng yêu cầu; dừng bất
   kỳ lúc nào.
3. Thanh công cụ phiên: chọn màn hình, tỉ lệ, chất lượng, hình nền, con trỏ, âm thanh máy xa, chụp vùng + chú thích,
   quay video, chat, chia sẻ clipboard (bật/tắt).
4. Giao diện tiếng Việt mặc định; đổi English / Theo hệ thống trong Cài đặt (⌘,).
5. Cửa sổ **Giới thiệu** có icon, phiên bản, logo HVN GROUP, hvn.vn, kythuat@hvn.vn và câu miễn trừ "không phải sản
   phẩm chính thức của UltraViewer"; menu **Trợ giúp** mở hướng dẫn đóng gói trong app, website, email hỗ trợ.
6. **Kiểm tra cập nhật…** đọc Releases của `hvngroup/mac-ultra-viewer`.
7. CI xanh trên commit hiện tại: toàn bộ `swift test`, đóng gói app, kiểm tra bundle, xuất `.dmg` + `.zip` + `.sha256`.
8. Chủ sản phẩm chạy checklist (`docs/manual-test-checklist.md`) trên Mac thật và xác nhận.

## Hướng đã chọn

| Thành phần | Lựa chọn |
|---|---|
| Tên hiển thị | **HVN UltraViewer** (bundle `HVN UltraViewer.app`) |
| Bundle ID | `vn.hvn.ultraviewer` |
| Module Swift | `HVNUltraViewer` (app) + `UltraViewerProtocol` (engine) + `CZstd`, `CG722` (C) |
| Build | **Swift Package Manager** + `scripts/package-app.sh` lắp `.app` (giữ cách đã chạy xanh của bản gốc) |
| Phiên bản | `version.conf` (`APP_VERSION`, `APP_BUILD`) — nguồn duy nhất; tag `vX.Y.Z` phải khớp |
| CI / phát hành | Một workflow **Build** theo `ab-app-release`: test → đóng gói → kiểm tra bundle → DMG/zip/SHA-256 → Release từ CHANGELOG |
| Cập nhật | `UpdateChecker` của bản gốc, trỏ về Releases của HVN; tự cài khi app ký Developer ID, bản ad-hoc mở DMG |
| Brand | Icon vẽ bằng script từ hình học logo HVN chuẩn; logo trong app render từ SVG chuẩn (không để AI vẽ) |

### Vì sao không dùng XcodeGen (lệch chuẩn `ab-macos-native`)

Chuẩn nhà dùng XcodeGen vì cần app extension (Quick Look) và tránh sửa `project.pbxproj` tay. App này **không có
extension**, còn bản gốc đã build + test xanh bằng SwiftPM trên runner macOS với 2 target C (zstd, G.722) và tài nguyên
`Bundle.module`. Chuyển sang Xcode project sẽ phải đổi cách nạp tài nguyên và cách chạy test của ~16.500 dòng mã mà
agent không build thử được tại chỗ. Giữ SwiftPM giảm rủi ro mà vẫn đáp ứng mọi cổng của suite (Info.plist đầy đủ, bản
dịch `vi.lproj`, kiểm tra bundle trên CI, DMG, release notes từ CHANGELOG).

## Trade-offs

| Hướng | Phụ thuộc lớn nhất | Hỏng đầu tiên khi |
|---|---|---|
| A (chọn) — chuyển mã + dựng lại vỏ app theo chuẩn HVN trên SwiftPM | Giao thức UltraViewer giữ ổn định | UltraViewer đổi giao thức/máy chủ relay |
| B — XcodeGen + Xcode project | Agent không build được tại chỗ | Lỗi cấu hình tài nguyên/test chỉ lộ trên CI, nhiều vòng sửa |
| C — viết lại engine từ đầu | Tài liệu giao thức (không có) | Ngay từ đầu |

Better approaches: none — B và C tốn hơn mà không thêm giá trị cho người dùng (bằng chứng: bản gốc đã phát hành bằng SwiftPM).

## Rủi ro cần kiểm chứng

1. **Thương hiệu "UltraViewer":** tên app chứa thương hiệu của bên thứ ba (chủ sản phẩm đã chọn tên này). Giảm rủi ro
   bằng câu miễn trừ ở About, README, Cài đặt. Nên tham vấn pháp chế trước khi phát hành cho khách hàng bên ngoài.
2. **`8bit.dat`** là dữ liệu do UltraViewer cung cấp, không thuộc MIT; phân phối lại trong app HVN cần đánh giá pháp lý.
3. Giao thức dịch ngược có thể hỏng khi UltraViewer cập nhật; chỉ kiểm được trên máy thật.
4. Quyền Screen Recording/Accessibility gắn với chữ ký: bản ad-hoc mỗi lần build có chữ ký khác → macOS có thể đòi cấp
   lại quyền sau khi cập nhật.

## Câu hỏi còn mở

- Ý kiến pháp chế về tên "UltraViewer" và việc phân phối `8bit.dat` (rủi ro 1–2).
- HVN có tài khoản Apple Developer để ký Developer ID chưa? (Khi có: thêm secrets, workflow tự ký + notarize.)

---

HVN GROUP · hvn.vn

## Nhật ký quyết định

- **2026-10-20 — đổi tên trước khi phát hành 1.0.0.** Sau báo cáo
  [research-261020-1221-universal-remote-feasibility.md](research-261020-1221-universal-remote-feasibility.md), chủ sản
  phẩm chọn tên **HVN Remote Hub** (bundle ID `vn.hvn.remotehub`, module `HVNRemoteHub`, file phát hành
  `HVNRemoteHub-*.dmg`), thay cho "HVN UltraViewer". Tên mới không chứa thương hiệu bên thứ ba (giảm rủi ro 1 ở trên) và
  hợp với hướng đa nền tảng. Phạm vi 1.0.0 giữ nguyên; phần hub (danh bạ đa nền, mở TeamViewer/AnyDesk/RDP/VNC) để
  sang 1.1.0. Giao thức riêng của HVN (tham khảo RustDesk) và các bản Windows/iOS/Android lập kế hoạch tại
  [../261020-1227-hvn-protocol-multiplatform/plan.md](../261020-1227-hvn-protocol-multiplatform/plan.md).
- **2026-10-20 — bỏ bản 1.1.0.** Đã chọn Flutter cho mọi nền tảng ở 2.0, nên phần hub làm thẳng trong app Flutter thay
  vì viết bằng Swift rồi viết lại. App Swift dừng ở dòng 1.0.x (bản vá lỗi) cho đến khi 2.0 thay thế.
