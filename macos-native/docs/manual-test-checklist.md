# Checklist chạy thử trên Mac thật — HVN Remote Hub {{phiên bản}}

Người chạy: ______ · Máy: ______ (chip, macOS) · Ngày: ______
Bản build: link artifact hoặc Release ______
Máy đối tác: ______ (Windows + UltraViewer phiên bản ______)

## Cài đặt

- [ ] Mở `.dmg`, kéo app vào Applications; `shasum -a 256 -c` khớp file `.sha256`.
- [ ] Lần mở đầu: macOS chỉ hỏi xác nhận mở app tải từ Internet (không cần Open Anyway); `spctl -a -vv` báo
  `accepted` và `source=Notarized Developer ID`.
- [ ] Icon đỏ HVN đúng trên Dock, Launchpad, Finder.

## Điều khiển máy khác

- [ ] Nhập ID + mật khẩu của máy Windows → **Kết nối** → thấy màn hình máy kia.
- [ ] Sai mật khẩu → báo lỗi rõ ràng, không treo.
- [ ] Bật **Điều khiển**: gõ chữ (có dấu tiếng Việt nếu máy kia dùng bộ gõ), ⌘ → Win, ⌥ → Alt, ⌃ → Ctrl, click, kéo
      thả, cuộn trackpad và con lăn.
- [ ] Đổi màn hình (máy nhiều màn hình), tỉ lệ, chất lượng, hình nền, con trỏ máy xa.
- [ ] **Âm thanh máy tính**: nghe được âm thanh máy kia; tắt được.
- [ ] Chụp vùng màn hình + chú thích → lưu được ảnh.
- [ ] **Quay màn hình từ xa…** → dừng → file `.mov` phát được.
- [ ] **Trò chuyện**: gửi/nhận tin nhắn hai chiều.
- [ ] Clipboard: copy chữ trên Mac dán ở máy kia và ngược lại; tắt trong Cài đặt thì không còn chia sẻ.
- [ ] **Ghi nhớ mật khẩu** → kết nối lại không phải nhập; **Quên mật khẩu đã lưu** xoá được.
- [ ] **Ngắt kết nối** (⇧⌘D): máy kia thấy phiên kết thúc ngay.

## Chia sẻ máy Mac này

- [ ] **Bắt đầu chia sẻ máy Mac** → hướng dẫn cấp quyền Ghi màn hình và Trợ năng hoạt động (kéo app vào danh sách).
- [ ] Máy Windows nhập ID + mật khẩu của Mac → Mac hiện yêu cầu → **Cho phép xem**: máy kia thấy màn hình Mac.
- [ ] **Cho phép điều khiển**: máy kia điều khiển được chuột, bàn phím của Mac.
- [ ] **Từ chối** → máy kia không vào được.
- [ ] **Kết thúc phiên truy cập** và **Tạm dừng truy cập từ xa** hoạt động.
- [ ] Đổi phía điều khiển (máy Windows yêu cầu) → Mac duyệt → kết nối ngược lại được.

## Ngôn ngữ, Giới thiệu, Trợ giúp

- [ ] Giao diện tiếng Việt mặc định ở lần mở đầu, kể cả thanh menu.
- [ ] Cài đặt (⌘,) → English → cửa sổ đổi ngay; **Khởi động lại ngay** → thanh menu tiếng Anh. Đổi lại Tiếng Việt.
- [ ] **Giới thiệu HVN Remote Hub**: đúng phiên bản/build, logo HVN GROUP rõ ở chế độ Sáng và Tối, link hvn.vn và
      kythuat@hvn.vn mở được, câu miễn trừ hiện đủ; **Giấy phép** mở thư mục giấy phép.
- [ ] **Trợ giúp → Trợ giúp HVN Remote Hub** mở hướng dẫn; **Hướng dẫn trực tuyến**, **Website HVN GROUP**, **Gửi
      email hỗ trợ kỹ thuật**, **Báo lỗi…** mở đúng đích.
- [ ] Header cửa sổ chính có logo HVN GROUP, đổi đúng theo Sáng/Tối; nút chính màu đỏ brand.

## Cập nhật

- [ ] **Kiểm tra bản cập nhật…** báo "đang là bản mới nhất" (hoặc đúng bản mới khi có Release mới hơn).
- [ ] Khi có bản mới hơn: nút **Cập nhật lên …** hiện; bản Developer ID tự cài và mở lại (bản ad-hoc mở DMG trong
  Downloads).

## Kết luận

- [ ] Đạt — chuyển PR sang ready / phát hành.
- [ ] Chưa đạt — ghi lỗi và ảnh chụp: ______

---

HVN GROUP · hvn.vn
