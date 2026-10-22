# Plan — Giao thức riêng của HVN và HVN Remote Hub đa nền tảng

- Trạng thái: **Cổng ① đã chốt** (2026-10-20) — hướng A1; chờ P0 (máy chủ thử nghiệm) và P1 (tạo repo fork)
- Yêu cầu (2026-10-20): đổi tên thành HVN Remote Hub; hub làm thẳng trong Flutter 2.0 (bỏ bản 1.1.0); tham khảo RustDesk để có giao thức riêng cho HVN;
  sau đó làm bản Windows, iOS, Android.
- Liên quan: [research-261020-1221-universal-remote-feasibility.md](../reports/research-261020-1221-universal-remote-feasibility.md)

## Lộ trình đề xuất

| Bản | Nội dung | Nền tảng |
|---|---|---|
| **1.0.0** | HVN Remote Hub for Mac: engine UltraViewer gốc, brand HVN, tiếng Việt mặc định | macOS |
| **2.0.0** | App Flutter (fork RustDesk): **HVN Connect** — máy chủ ID/relay của HVN trên `connect.hvn.vn`, mã hoá đầu-cuối — và **hub** (danh bạ đa nền, mở TeamViewer/AnyDesk/RDP/VNC, UltraViewer) | macOS, Windows, Android, iOS + máy chủ |
| 2.x | Hoàn thiện theo phản hồi nội bộ; cân nhắc bán như dịch vụ | Mọi nền tảng |

## RustDesk — những gì tham khảo được (đã kiểm tra mã nguồn 2026-10-20)

- **Giấy phép:** `rustdesk/rustdesk` và `rustdesk/rustdesk-server` đều **AGPL-3.0**. Phân phối bản sửa đổi, hoặc chạy
  máy chủ đã sửa cho người khác dùng qua mạng, thì phải công bố toàn bộ mã nguồn tương ứng theo AGPL. Thương hiệu
  "RustDesk" không đi kèm giấy phép mã nguồn.
- **Kiến trúc:** lõi Rust; giao diện **Flutter** cho cả desktop lẫn mobile (Windows, macOS, Linux, Android, iOS).
  - `libs/hbb_common`: codec, cấu hình, TCP/UDP, protobuf dùng chung với máy chủ.
  - `libs/scrap`: chụp màn hình. `libs/enigo`: bàn phím/chuột. `libs/clipboard`: clipboard và file.
  - `src/rendezvous_mediator.rs`: làm việc với máy chủ.
- **Giao thức:** protobuf (`rendezvous.proto`: `RegisterPeer`, `PunchHoleRequest`, `RequestRelay`, `KeyExchange`, …;
  `message.proto` cho phiên). Mã hoá bằng libsodium (`sodiumoxide`). Kết nối thẳng bằng TCP hole punching, không được thì
  qua relay.
- **Máy chủ:** `hbbs` (ID/rendezvous) + `hbbr` (relay), tự host được (bản OSS). Bản Server Pro (trả phí) có web console và
  công cụ tạo client mang thương hiệu riêng.

## Các hướng làm "giao thức riêng của HVN"

| | **A. Fork RustDesk (AGPL)** | **B. Tự viết HVN Connect (tham khảo thiết kế)** | **C. Mua RustDesk Server Pro** |
|---|---|---|---|
| Cách làm | Fork client + server, đổi thương hiệu, máy chủ đặt trên HVN Cloud, sửa/bổ sung giao thức | Lõi Rust mới (protobuf, Noise/libsodium, rendezvous/relay, codec phần cứng), viết sạch, không chép mã RustDesk | License Pro + công cụ tạo client mang thương hiệu HVN, máy chủ tự host |
| Có Windows/Android/iOS | **Ngay** (RustDesk đã chạy trên cả 5 nền tảng) | Phải tự làm từng nền tảng | Ngay |
| "Giao thức riêng" | Có: HVN kiểm soát mã và máy chủ; tương thích ngược với RustDesk nếu muốn | Có, hoàn toàn của HVN | Không: vẫn là giao thức và client của RustDesk |
| Giấy phép mã HVN | **Phải mở mã** (AGPL) cho app và máy chủ đã sửa | Tự chọn (có thể đóng) | Theo điều khoản thương mại của RustDesk |
| Công sức (ước lượng thô) | 1–2 tháng cho bản đổi thương hiệu đầu tiên trên các nền tảng; cập nhật theo upstream liên tục | 6–12 tháng cho mức tương đương; rủi ro kỹ thuật cao (NAT, codec, quyền hệ điều hành trên từng nền tảng) | Vài tuần |
| Rủi ro chính | Nghĩa vụ AGPL; theo kịp upstream | Thời gian, chất lượng, bảo mật tự làm | Phụ thuộc nhà cung cấp; không phải giao thức của HVN |

**Khuyến nghị: A.** Đây là cách duy nhất có giao thức và máy chủ của HVN trên cả 4 nền tảng trong vài tháng. Repo này đã
công khai, nên việc mở mã theo AGPL ít thay đổi so với hiện trạng. Phần đóng góp của HVN nằm ở máy chủ trên HVN Cloud, tích
hợp WHMCS/HVN Works, dịch vụ hỗ trợ và thương hiệu. B chỉ đáng làm khi HVN bắt buộc giữ mã nguồn đóng. C hợp nếu cần ra
mắt gấp và chấp nhận không có giao thức riêng.

### Hệ quả của A với app Mac hiện tại

- App Mac (Swift) giữ vai trò hub + engine UltraViewer (1.0–1.1).
- Ở 2.0.0, có hai cách đưa HVN Connect vào Mac:
  - **A1 (khuyến nghị):** bản fork Flutter trở thành HVN Remote Hub trên **mọi** nền tảng. App Swift hiện tại chuyển
    thành mô-đun UltraViewer chỉ dành cho macOS (trên Windows đã có UltraViewer chính hãng để hub mở). Một codebase giao
    diện cho 5 nền tảng.
  - **A2:** giữ app Swift trên Mac, gọi lõi Rust qua FFI; trên Windows/Android/iOS dùng bản fork Flutter. Trải nghiệm Mac
    gốc hơn, nhưng phải duy trì hai giao diện.
- Phần mã MIT hiện có (MacViewer, phần HVN viết) gộp được vào dự án AGPL (MIT tương thích một chiều với AGPL).

## Quyết định đã chốt (Cổng ① của 2.0.0)

| Câu hỏi | Trả lời của chủ sản phẩm (2026-10-20) |
|---|---|
| Giấy phép | **Chấp nhận AGPL-3.0**: công bố mã nguồn app và máy chủ đã sửa |
| Hướng kỹ thuật | **A — fork RustDesk** (client + server), đổi thương hiệu thành HVN Remote Hub |
| Hạ tầng | Máy chủ ID/relay trên **HVN Cloud tại Việt Nam** |
| Ký số Apple | HVN **đã có Apple Developer** → ký Developer ID + notarize cho macOS, phát hành iOS qua App Store/TestFlight |
| Khách hàng mục tiêu | **Nội bộ trước** (đội hỗ trợ HVN); bán như dịch vụ là quyết định sau, khi đó mới làm VAPT và mô hình tính phí |
| Giao diện từ 2.0.0 | **A1 — Flutter cho mọi nền tảng**, kể cả macOS |
| Tên miền máy chủ | **`connect.hvn.vn`** |
| Hub | **Bỏ bản 1.1.0 (Swift)**; hub làm thẳng trong app Flutter 2.0 |

## Các phase của 2.0.0

| Phase | Việc | Ai làm | Đầu ra |
|:-:|---|---|---|
| P0 | Máy chủ thử nghiệm trên HVN Cloud: `hbbs` + `hbbr`, DNS, khoá ký máy chủ; đo độ trễ và tỉ lệ kết nối thẳng/relay bằng client RustDesk gốc | Hạ tầng HVN Cloud (runbook: [phase-01-server-pilot.md](phase-01-server-pilot.md)) | Máy chủ chạy, số đo |
| P1 | Fork `rustdesk/rustdesk` → **`hvngroup/rustdesk`** (xong 2026-10-20, đã thêm vào phiên agent). Fork `hbb_common`/`rustdesk-server` chưa cần (xem P2) | Chủ sản phẩm | Repo fork |
| P2 | Đổi thương hiệu: `APP_NAME`, `ORG` (`vn.hvn`), `RENDEZVOUS_SERVERS`, `RS_PUB_KEY`, bundle/application ID `vn.hvn.remotehub` trên 5 nền tảng, icon + logo HVN, tiếng Việt mặc định, gỡ link cập nhật/tài trợ của RustDesk, ghi công + thông báo AGPL | Agent ([phase-02-rebrand-fork.md](phase-02-rebrand-fork.md)) | Client nói chuyện với máy chủ HVN |
| P3 | CI cho từng nền tảng: macOS (ký Developer ID + notarize), Windows (ký code signing), Android (APK/AAB), iOS (TestFlight) | Agent + chủ sản phẩm (secrets) | Bản build ký số trên 5 nền tảng |
| P4 | Hub (danh bạ đa nền, mở TeamViewer/AnyDesk/RDP/VNC) viết trong Flutter; UltraViewer trên macOS bọc engine Swift `UltraViewerProtocol` thành plugin Flutter cho macOS; trên Windows hub mở UltraViewer chính hãng | Agent | Một app HVN Remote Hub |
| P5 | Cổng ③ trên máy thật từng nền tảng (dùng nội bộ: chưa cần VAPT) | Chủ sản phẩm | Biên bản kiểm thử |
| P6 | Phát hành 2.0.0: GitHub Releases, App Store, Google Play, công bố mã nguồn theo AGPL | Chủ sản phẩm | Bản phát hành |

## Việc chủ sản phẩm cần chuẩn bị

1. **Ngay cho bản 1.0.0:** thêm secrets Developer ID vào repo này (`MACOS_CERTIFICATE_P12`, `MACOS_CERTIFICATE_PASSWORD`,
   `APPSTORE_API_KEY_P8`, `APPSTORE_API_KEY_ID`, `APPSTORE_API_ISSUER_ID`; xem `docs/release.md`). Ký Developer ID ngay từ
   bản đầu thì người dùng không phải "Open Anyway", app tự cài bản cập nhật, quyền macOS không bị hỏi lại sau mỗi lần cập
   nhật.
2. P0: một VPS trên HVN Cloud (gợi ý 2 vCPU, 4 GB RAM, băng thông lớn, IP tĩnh) và bản ghi DNS `connect.hvn.vn`.
3. Bật GitHub Actions trên `hvngroup/rustdesk` để CI chứng minh build của bản fork.
4. P3: chứng chỉ code signing cho Windows (EV hoặc OV, qua HVN Security/Sectigo), tài khoản Google Play Console.

## Chuyển tiếp từ app Swift 1.x sang app Flutter 2.0 trên Mac

- App Flutter 2.0 dùng **cùng bundle ID `vn.hvn.remotehub`**, cùng Team ID Developer ID và cùng tên file phát hành
  `HVNRemoteHub-*.dmg` trên Releases của repo này (hoặc repo mới, kèm bản 1.x cuối trỏ sang). Như vậy bản 1.x tự cập nhật
  lên 2.0 tại chỗ, người dùng không phải cài lại.
- Hai bản lưu cài đặt khác nhau: bản 2.0 cần đọc lại danh sách ID gần đây (UserDefaults `HVNRemoteHub.*`) và mật khẩu
  trong Keychain (`vn.hvn.remotehub.partner`) của bản 1.x, hoặc báo người dùng nhập lại.

---

HVN GROUP · hvn.vn
