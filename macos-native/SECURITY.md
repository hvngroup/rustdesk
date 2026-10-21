# Bảo mật

## Báo lỗ hổng

Vui lòng **không mở issue công khai**. Gửi riêng tới **kythuat@hvn.vn** hoặc qua
[GitHub Security Advisories](https://github.com/hvngroup/universal-remote-hub/security/advisories/new), kèm phiên bản bị
ảnh hưởng và các bước tái hiện. HVN GROUP phản hồi trong vài ngày làm việc và ghi công người báo trong release notes
nếu anh/chị muốn.

Không gửi kèm dữ liệu nội bộ, dữ liệu khách hàng, ID đối tác, mật khẩu, token hay ảnh chụp phiên.

## App xử lý dữ liệu thế nào

- **Mật khẩu đối tác** chỉ lưu khi người dùng chọn ghi nhớ, và chỉ trong Keychain của macOS (service
  `vn.hvn.remotehub.partner`). Không bao giờ ghi vào UserDefaults, lịch sử hay hồ sơ đăng ký.
- **Lịch sử kết nối** chỉ lưu ID đối tác đã kết nối thành công (tắt được trong Cài đặt).
- **Hồ sơ cài đặt** (định danh thiết bị dùng để đăng ký với máy chủ UltraViewer) nằm trong
  `~/Library/Application Support/HVN Remote Hub/`, thư mục quyền `0700`.
- **Ảnh chụp và video** chỉ tạo khi người dùng bấm, lưu trên máy.
- **Không có telemetry.** App không gửi dữ liệu nào tới HVN GROUP.

## Kết nối mạng app chủ động mở

- Máy chủ tra cứu và relay của UltraViewer (TLS có kiểm chứng chỉ) khi kết nối hoặc chia sẻ màn hình.
- Kết nối thẳng trong mạng LAN tới máy đối tác khi được, tự quay về relay.
- `api.github.com` (thông tin Release công khai) khi kiểm tra cập nhật; tải DMG từ `github.com`. Tắt được trong Cài đặt.

## Cơ chế cập nhật

App chỉ nhận file DMG có host `github.com` từ Release không phải nháp/pre-release. Tự cài chỉ khi app đang chạy được ký
Developer ID: bản mới phải có chữ ký hợp lệ, neo Apple, **cùng Team ID** và cùng bundle ID; nếu không, app chỉ mở DMG để
người dùng tự kiểm tra.

## Quyền macOS

Ghi màn hình và Trợ năng chỉ cần khi **chia sẻ máy Mac này**. Mỗi kết nối tới Mac phải được người dùng duyệt; quyền
xem và quyền điều khiển duyệt riêng.

## Phiên bản được hỗ trợ

Chỉ bản phát hành mới nhất được vá lỗi.

---

HVN GROUP · hvn.vn
