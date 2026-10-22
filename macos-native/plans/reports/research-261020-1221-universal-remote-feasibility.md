# Nghiên cứu khả thi — app điều khiển từ xa "đa nền" (UltraViewer + TeamViewer + AnyDesk) và đổi tên app

- Ngày: 2026-10-20
- Câu hỏi: Có thể biến HVN UltraViewer thành một app "universal remote" hỗ trợ thêm TeamViewer và AnyDesk không? Có nên đổi tên app?
- Phân loại: Nội bộ

## Kết luận

1. **Tự viết giao thức TeamViewer/AnyDesk trong app (như đã làm với UltraViewer): không khả thi và không nên làm.** Hai giao
   thức này đóng, mã hoá đầu-cuối, đổi theo phiên bản; EULA của TeamViewer cấm rõ việc dịch ngược "kể cả để tìm giao diện
   tương tác". Với một đối tác ủy quyền của nhiều hãng như HVN GROUP, rủi ro pháp lý và uy tín lớn hơn nhiều lợi ích.
2. **Một app "trung tâm điều khiển từ xa" (remote hub) thì khả thi**: app giữ danh bạ máy, mở phiên qua **client chính hãng**
   của TeamViewer/AnyDesk bằng kênh hãng công bố (URL handler, tham số dòng lệnh), còn UltraViewer vẫn chạy bằng engine
   gốc trong app. Có thể bổ sung kênh chuẩn mở: **RDP** (Windows), **VNC/Screen Sharing** (Mac), và về lâu dài
   **RustDesk** làm giải pháp remote mang thương hiệu HVN, máy chủ tự host.
3. **Nên đổi tên, và nên đổi trước khi phát hành 1.0.0**: tên trung tính (ví dụ **HVN Remote**) giải luôn rủi ro thương hiệu
   "UltraViewer" đã ghi trong báo cáo phạm vi, và hợp với hướng đa nền. Đổi sau khi đã phát hành tốn kém hơn: bundle ID mới
   làm người dùng mất quyền đã cấp, mất kênh tự cập nhật, mất mật khẩu đã lưu trong Keychain.

## Bằng chứng theo từng nền tảng

| Nền tảng | Tự triển khai giao thức trong app | Kênh tích hợp chính thức | Mức tích hợp thực tế trên macOS |
|---|---|---|---|
| **UltraViewer** | Đã có (engine MacViewer, dịch ngược) | Không có API công bố | **Gốc trong app**: xem, điều khiển, chat, clipboard, âm thanh |
| **TeamViewer** | Không: giao thức đóng; EULA mục 4 cấm decompile/dịch ngược, kể cả để tìm giao diện tương tác | Tham số dòng lệnh `-i ID -p PASSWORD -m fileTransfer -q -a` (tài liệu ghi cho Windows); URL `teamviewer10://control?device=ID` (chỉ có trên diễn đàn, có người báo không chạy với TeamViewer 15); Web API REST + OAuth 2.0 (danh bạ, báo cáo kết nối, phiên hỗ trợ; tích hợp là add-on trả phí, cần license ≥ v11) | **Mở client chính hãng** tới ID; điền mật khẩu tự động **chưa chắc chạy trên Mac**, phải thử |
| **AnyDesk** | Không: giao thức đóng (DeskRT), mã hoá; không tìm thấy điều khoản cho phép | URL handler `anydesk:<ID>` (macOS từ 6.3.1); CLI macOS chỉ có `--get-id`, `--get-status`, `--version`, `--set-password`, `--register-license`; `--with-password` chỉ ghi cho Windows/Linux, có người dùng báo bị tắt trên macOS; REST API (lịch sử phiên, license) chạy trên my.anydesk I, giao diện quản trị này sắp ngừng | **Mở client chính hãng** tới ID; mật khẩu do người dùng nhập trong AnyDesk |
| **RDP** (Windows) | Không cần: chuẩn mở | URL `rdp://` / file `.rdp` mở bằng Windows App của Microsoft | Mở client của Microsoft |
| **VNC / Screen Sharing** (Mac) | Có thể, nhưng không cần | URL `vnc://host` mở Screen Sharing có sẵn trên macOS | Mở app có sẵn của hệ thống |
| **RustDesk** | Mã nguồn mở (AGPL-3.0) | Máy chủ OSS tự host miễn phí; bản build client đổi thương hiệu là tính năng trả phí của Server Pro | Có thể là **giải pháp remote của chính HVN** (sản phẩm riêng) |

## Phương án

| | A. Giữ "HVN UltraViewer" chỉ cho UltraViewer | **B. "HVN Remote": hub + engine UltraViewer (khuyến nghị)** | C. Tự viết giao thức TeamViewer/AnyDesk |
|---|---|---|---|
| Việc phải làm | Không thêm | Đổi tên/bundle ID trước 1.0.0; thêm danh bạ đa nền + trình mở phiên (URL/CLI); tài liệu | Dịch ngược hai giao thức đóng, có mã hoá |
| Công sức (ước lượng) | 0 | ~1–2 tuần cho bản hub đầu (danh bạ, mở phiên, kiểm tra app đã cài) | Không ước lượng được; có thể không làm được |
| Pháp lý | Rủi ro thương hiệu trong tên | Rủi ro tên **giảm**; tích hợp TeamViewer/AnyDesk đúng kênh hãng công bố | Vi phạm EULA, rủi ro thương hiệu, rủi ro bị khoá tài khoản/ID |
| Hỏng đầu tiên khi | UltraViewer đổi giao thức | TeamViewer/AnyDesk đổi URL/tham số (sửa nhỏ) | Mỗi bản cập nhật của hãng |
| Giá trị cho HVN | Một công cụ nội bộ | Một điểm vào cho đội hỗ trợ (#Witch) làm việc với khách dùng phần mềm nào cũng được; mở đường bán license TeamViewer/AnyDesk/RustDesk | Không tương xứng rủi ro |

### Giới hạn của phương án B — cần nói rõ với người dùng

- Với TeamViewer/AnyDesk, app **không hiển thị màn hình trong cửa sổ của mình**: nó mở client chính hãng (máy phải cài sẵn)
  và chuyển ID cho client đó. Trải nghiệm "một cửa sổ cho mọi thứ" chỉ có với UltraViewer (và RustDesk nếu làm sau).
- Điền mật khẩu tự động cho TeamViewer/AnyDesk trên macOS **chưa được kiểm chứng**; giả định ban đầu là người dùng nhập mật
  khẩu trong client chính hãng.
- Không lưu mật khẩu TeamViewer/AnyDesk thay hãng nếu chưa có kênh truyền an toàn (theo ATTT HVN 01-01/11/2024: không
  truyền mật khẩu qua tham số dòng lệnh, vì tiến trình khác trên máy đọc được).

## Đề xuất đặt tên

| Tên | Bundle ID | Nhận xét |
|---|---|---|
| **HVN Remote** (khuyến nghị) | `vn.hvn.remote` | Ngắn, trung tính, đúng mô hình đa nền; không chứa thương hiệu bên thứ ba |
| HVN Remote Hub | `vn.hvn.remotehub` | Nhấn vai trò "trung tâm"; dài hơn |
| HVN Support Desk | `vn.hvn.supportdesk` | Hợp với đội CSKH; dễ nhầm với phần mềm helpdesk/ticket |

Quy tắc chung: tên app và icon **không** chứa "UltraViewer", "TeamViewer", "AnyDesk". Các tên đó chỉ xuất hiện trong mô tả
khả năng tương thích ("Kết nối được với máy chạy UltraViewer…"), kèm câu miễn trừ.

## Chi phí đổi tên nếu làm ngay (trước khi phát hành 1.0.0)

- Đổi `CFBundleIdentifier`, tên hiển thị, tên module/sản phẩm, tên file phát hành (`HVNRemote-*.dmg`), tiền tố UserDefaults,
  dịch vụ Keychain, chuỗi giao diện chứa tên app (khoảng 30 chuỗi vi/en), tài liệu. Có thể đổi tên repo trên GitHub;
  GitHub tự chuyển hướng tên cũ, nhưng nên sửa URL trong `UpdateChecker`.
- Chưa có người dùng ngoài nhóm thử nghiệm, nên không phải chuyển dữ liệu cũ. Chỉ máy đã chạy thử phải cấp lại quyền Ghi
  màn hình và Trợ năng.
- Làm trên PR #1 (chưa merge) hoặc một PR mới trước PR phát hành; CI và Cổng ③ chạy lại.

## Bước tiếp theo đề xuất

1. Chủ sản phẩm chốt: tên mới + phương án B (hoặc A).
2. Nếu chọn B: đổi tên trong PR riêng trước khi phát hành 1.0.0; ghi tính năng hub vào kế hoạch 1.1.0 (danh bạ đa nền,
   mở TeamViewer/AnyDesk/RDP/VNC, nhận biết app đã cài).
3. Thử tay trên Mac thật: `teamviewer10://control?device=<ID>`, `anydesk:<ID>`, tham số `-i` của TeamViewer for Mac.
4. Tham vấn pháp chế về tên, về `8bit.dat` và về việc dùng engine UltraViewer dịch ngược trong sản phẩm thương mại.
5. (Tuỳ chọn, dài hạn) Đánh giá RustDesk Server Pro + client mang thương hiệu HVN như một dịch vụ remote của HVN Cloud.

## Câu hỏi còn mở

- App này chỉ dùng nội bộ cho đội hỗ trợ, hay sẽ phát cho khách hàng? Câu trả lời quyết định mức rủi ro pháp lý chấp nhận được.
- HVN có (hoặc muốn có) quan hệ đối tác với TeamViewer/AnyDesk không? Có thì có thể xin kênh tích hợp chính thức và API.

## Nguồn

- TeamViewer — Command line parameters: https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-remote/for-developers/command-line-parameters/
- TeamViewer — URL `teamviewer10://` (diễn đàn): https://community.teamviewer.com/English/discussion/131585/teamviewer-15-url-link-to-start-a-remote-connection
- TeamViewer — Build an integration / API: https://www.teamviewer.com/hk/global/support/knowledge-base/teamviewer-remote/for-developers/build-a-teamviewer-integration/ · https://www.teamviewer.com/pl/global/support/knowledge-base/teamviewer-classic/integrations/core-integrations/teamviewer-api/
- TeamViewer — EULA (bản sao): https://ftp.fau.de/gentoo-portage/licenses/TeamViewer
- AnyDesk — CLI for macOS: https://support.anydesk.com/docs/command-line-interface-for-macos.md · CLI (Windows/Linux): https://support.anydesk.com/docs/command-line-interface.md
- AnyDesk — URL handler: https://support.anydesk.com/docs/url-handler.md · REST API: https://support.anydesk.com/docs/rest-api.md
- Báo cáo người dùng về `--with-password` trên macOS: https://forum.devolutions.net/topics/36854/anydesk-for-rdm-macos
- RustDesk: https://rustdesk.com/ · https://rustdesk.com/blog/rustdesk-vs-anydesk

---

HVN GROUP · hvn.vn
