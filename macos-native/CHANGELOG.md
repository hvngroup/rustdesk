# Changelog

Mọi thay đổi đáng chú ý của HVN Remote Hub được ghi tại đây. Định dạng theo
[Keep a Changelog](https://keepachangelog.com/vi/1.1.0/), phiên bản theo [Semantic Versioning](https://semver.org/lang/vi/).

Khi phát hành, workflow **Build** lấy đúng mục của phiên bản tương ứng trong file này làm mô tả cho GitHub Release.

## [Unreleased]

## [1.0.1] - 2026-10-20

### Thay đổi

- Bản phát hành được ký Developer ID của HVN GROUP và notarize với Apple: mở được ngay, không cần "Open Anyway",
  và từ bản này app tự cài các bản cập nhật sau.
- Nâng cấp từ 1.0.0 (ký ad-hoc): bấm **Cập nhật lên 1.0.1**, app tải file DMG về Downloads; kéo app mới vào Applications
  để thay bản cũ, rồi cấp lại quyền Ghi màn hình và Trợ năng một lần vì chữ ký của app đã đổi.
- Hướng dẫn cài đặt (trong app và README) cập nhật theo bản đã ký.
- App kiểm tra cập nhật ở repo chung `hvngroup/universal-remote-hub` và chỉ nhận các bản có tag `mac-v…`, vì repo này
  còn phát hành HVN Remote Hub 2.0. Liên kết báo lỗi và hướng dẫn trực tuyến cũng chuyển sang repo chung.

## [1.0.0] - 2026-10-20

### Thêm mới

- Ứng dụng HVN Remote Hub for Mac đầu tiên: điều khiển máy tính đang chạy UltraViewer bằng ID và mật khẩu, chia sẻ
  máy Mac sau khi duyệt từng yêu cầu, chat, chia sẻ clipboard, âm thanh máy xa, chụp vùng màn hình có chú thích và quay
  video — dựa trên engine của MacViewer (MIT).
- Nhận diện HVN GROUP: icon đỏ `#EA4445`, logo HVN GROUP trong cửa sổ chính và cửa sổ Giới thiệu, màu nhấn brand.
- Giao diện tiếng Việt mặc định, kể cả thanh menu; đổi English hoặc Theo hệ thống trong Cài đặt, có nút Khởi động lại.
- Cửa sổ Giới thiệu (phiên bản, liên hệ hvn.vn · kythuat@hvn.vn · 024.9999.7777, câu miễn trừ, giấy phép) và menu Trợ
  giúp (hướng dẫn đóng gói trong app, hướng dẫn trực tuyến, website, email hỗ trợ, báo lỗi).
- Kiểm tra và cài bản mới từ GitHub Releases của `hvngroup/mac-ultra-viewer`.
- Gói cài DMG, zip và mã SHA-256 cho mỗi bản build; ký Developer ID + notarize tự động khi repo có chứng chỉ.

[Unreleased]: https://github.com/hvngroup/mac-ultra-viewer/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/hvngroup/mac-ultra-viewer/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/hvngroup/mac-ultra-viewer/releases/tag/v1.0.0
