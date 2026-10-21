# Hướng dẫn sử dụng HVN Remote Hub for Mac

HVN Remote Hub giúp bạn **điều khiển một máy tính đang chạy UltraViewer** ngay trên Mac, hoặc **chia sẻ máy Mac này**
cho người hỗ trợ sau khi bạn duyệt. Giao diện mặc định là tiếng Việt.

> HVN Remote Hub do HVN GROUP phát triển; app kết nối được với UltraViewer nhưng không phải sản phẩm chính thức của UltraViewer. Chỉ kết nối
> tới máy tính bạn được phép truy cập.

## 1. Cài đặt

1. Tải file `HVNRemoteHub-<phiên bản>.dmg` từ trang
   [Releases](https://github.com/hvngroup/universal-remote-hub/releases), trong bản mới nhất có tag `mac-v…` (các bản tag `v…` là HVN Remote Hub 2.0).
2. (Tuỳ chọn) Kiểm tra file tải về không bị thay đổi: đặt file `.sha256` cạnh file DMG rồi chạy
   `shasum -a 256 -c HVNRemoteHub-<phiên bản>.dmg.sha256` — kết quả phải là `OK`.
3. Mở file DMG, kéo **HVN Remote Hub** vào thư mục **Applications**.
4. Mở app từ thư mục Applications. Từ bản 1.0.1, app được HVN GROUP ký và Apple kiểm duyệt (notarize): macOS chỉ hỏi
   xác nhận mở app tải từ Internet, bấm **Open**.
   Bản 1.0.0 ký ad-hoc: nếu macOS báo không mở được vì chưa xác minh nhà phát triển, bấm **Done** (không bấm Move to
   Trash), mở **System Settings → Privacy & Security**, kéo xuống, bấm **Open Anyway** cạnh dòng HVN Remote Hub.

Yêu cầu: macOS 14 Sonoma trở lên, máy Apple silicon hoặc Intel.

## 2. Điều khiển một máy tính khác

1. Trên máy kia, mở UltraViewer và đọc **ID** cùng **mật khẩu**.
2. Trên Mac, nhập **ID đối tác** và mật khẩu ở thẻ **Kết nối đến máy khác**, bấm **Kết nối** (⌘K).
3. Màn hình máy kia hiện ra. Để gửi bàn phím và chuột, bật **Điều khiển** trên thanh công cụ phiên.
   - <kbd>⌘</kbd> gửi phím Win, <kbd>⌥</kbd> gửi Alt, <kbd>⌃</kbd> gửi Ctrl.
   - Cuộn bằng trackpad hoặc con lăn; tốc độ cuộn chỉnh trong Cài đặt.
4. Thanh công cụ phiên còn có: chọn **Màn hình** (khi máy kia có nhiều màn hình), tỉ lệ hiển thị, chất lượng ảnh,
   ẩn/hiện hình nền, con trỏ máy xa, **Âm thanh máy tính**, chụp vùng màn hình có chú thích, **Quay màn hình từ xa…**,
   **Trò chuyện** và chia sẻ bảng nhớ tạm.
5. Bấm **Ngắt kết nối** (⇧⌘D) khi xong.

**Ghi nhớ mật khẩu:** chọn **Ghi nhớ mật khẩu trên máy Mac này** để lưu mật khẩu vào Keychain của macOS. Lịch sử kết
nối chỉ lưu ID, không bao giờ lưu mật khẩu. Xoá lịch sử hoặc mật khẩu đã lưu trong **Cài đặt → Lịch sử**.

## 3. Chia sẻ máy Mac này

1. Bấm **Bắt đầu chia sẻ máy Mac**.
2. Lần đầu, app mở hướng dẫn cấp quyền:

   | Quyền | Dùng để |
   |---|---|
   | **Ghi màn hình** (Screen Recording) | Cho máy kia xem màn hình Mac |
   | **Trợ năng** (Accessibility) | Cho máy kia điều khiển bàn phím, chuột của Mac |

   Bấm **Mở Cài đặt** ở từng quyền: macOS hỏi quyền, HVN Remote Hub xuất hiện trong danh sách của System Settings, bạn
   bật công tắc cạnh app. Nếu vẫn không thấy app trong danh sách, kéo biểu tượng app trong cửa sổ hướng dẫn vào danh sách.
   Sau khi cấp quyền Ghi màn hình, thoát và mở lại app nếu quyền vẫn hiện là chưa có.
   Luôn mở app từ thư mục **Applications**: bản mở thẳng từ file DMG hoặc thư mục Downloads sẽ mất quyền khi chuyển chỗ.
3. Đọc **ID** và **mật khẩu** của Mac cho người cần kết nối. Họ nhập vào UltraViewer trên máy của họ.
4. Khi có yêu cầu, chọn **Cho phép xem** hoặc **Cho phép điều khiển**, hay **Từ chối**.
5. Trong phiên, menu ở góc trên cho phép bật/tắt quyền điều khiển, **Kết thúc phiên truy cập** hoặc **Tạm dừng truy cập
   từ xa**.

## 4. Cài đặt (⌘,)

- **Ngôn ngữ:** Tiếng Việt (mặc định), English hoặc Theo hệ thống. Cửa sổ đổi ngay; thanh menu đổi sau khi bấm
  **Khởi động lại ngay**.
- **Lịch sử:** nhớ ID đối tác đã kết nối thành công; xoá lịch sử; quên mật khẩu đã lưu.
- **Bảng nhớ tạm:** bật/tắt chia sẻ clipboard cho phiên mới.
- **Màn hình từ xa:** làm mượt ảnh khi phóng to/thu nhỏ; tốc độ cuộn.
- **Giới thiệu:** phiên bản, tự kiểm tra cập nhật.

## 5. Cập nhật

App tự kiểm tra bản mới trên GitHub Releases của HVN GROUP (tắt được trong Cài đặt), hoặc chọn
**HVN Remote Hub → Kiểm tra bản cập nhật…**. Khi có bản mới, nút **Cập nhật lên …** hiện ở thanh tiêu đề:

- từ bản 1.0.1 (ký Developer ID): app tự tải, kiểm chữ ký, cài và mở lại;
- bản 1.0.0 (ký ad-hoc): app tải file DMG về thư mục Downloads và mở ra; kéo app mới vào Applications để thay bản cũ.

Cập nhật sẽ ngắt các kết nối đang mở. Khi chuyển từ bản 1.0.0 lên 1.0.1, macOS yêu cầu cấp lại quyền Ghi màn hình và
Trợ năng một lần, vì chữ ký của app đã đổi; các bản sau giữ nguyên quyền.

## 6. Xử lý sự cố

| Hiện tượng | Cách xử lý |
|---|---|
| Không mở được app lần đầu | Làm theo mục 1, bước 4. |
| Máy kia không thấy màn hình Mac | Kiểm tra quyền Ghi màn hình; thoát hẳn app (⌘Q) rồi mở lại. |
| Máy kia không điều khiển được Mac | Kiểm tra quyền Trợ năng và bạn đã chọn **Cho phép điều khiển**. |
| Không kết nối được | Kiểm tra ID, mật khẩu và mạng; UltraViewer trên máy kia phải đang mở. |
| Quyền đã bật nhưng app vẫn báo thiếu | Xoá app khỏi danh sách trong System Settings, thêm lại bằng cửa sổ hướng dẫn. |

## 7. Hỗ trợ

- Email kỹ thuật: **kythuat@hvn.vn** — hoặc menu **Trợ giúp → Gửi email hỗ trợ kỹ thuật**.
- Hotline: **024.9999.7777** · Website: **https://hvn.vn**
- Báo lỗi: **Trợ giúp → Báo lỗi…** (GitHub Issues). Không gửi kèm mật khẩu, ID đối tác hay dữ liệu khách hàng.

---

HVN GROUP · hvn.vn
