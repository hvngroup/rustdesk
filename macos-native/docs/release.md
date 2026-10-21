# Phát hành HVN Remote Hub

## Quy trình (Cổng ④)

1. **PR phát hành riêng** `chore: release X.Y.Z` (không kèm tính năng):
   - `CHANGELOG.md`: đổi `[Unreleased]` thành `[X.Y.Z] - YYYY-MM-DD`, thêm mục `[Unreleased]` trống, cập nhật link so
     sánh cuối file;
   - `version.conf`: `APP_VERSION=X.Y.Z`, `APP_BUILD` tăng 1;
   - chạy thử `scripts/release-notes.sh X.Y.Z`.
2. CI xanh → chủ sản phẩm merge vào `main`.
3. **Sau khi merge**, chủ sản phẩm tạo Release trên GitHub: *Releases → Draft a new release* → tag mới `mac-vX.Y.Z`,
   target **`master`**, để trống mô tả, không bấm "Generate release notes" → **Publish**. Tag `vX.Y.Z` (không có `mac-`)
   là của HVN Remote Hub 2.0, xem [docs/HVN-RELEASE.md](../../docs/HVN-RELEASE.md).
4. Workflow của tag: kiểm tag khớp `APP_VERSION` → test → đóng gói → (ký Developer ID + notarize nếu có secrets) →
   kiểm tra bundle → đính kèm `HVNRemoteHub-X.Y.Z.dmg`, `.zip`, `.sha256`, `SHA256SUMS.txt` và mô tả từ CHANGELOG.
5. Kiểm tra Release: tag trỏ đúng commit merge; đủ file; `shasum -a 256 -c SHA256SUMS.txt` khớp; `Info.plist` trong zip
   đúng `CFBundleShortVersionString` và `CFBundleVersion`.

Release tạo nhầm (trước khi PR merge, hoặc target sai nhánh): **xoá Release và xoá tag** (trang Tags) rồi tạo lại.
Sửa/đăng lại Release cũ không dời tag và không chạy lại workflow. Không ghi đè bản đã phát hành — lỗi thì ra bản patch.

## Tên file và cập nhật trong app

`UpdateChecker` (từ 1.0.1) đọc danh sách `https://api.github.com/repos/hvngroup/universal-remote-hub/releases`, chỉ xét
các bản có tag `mac-v…`, bỏ qua bản nháp/pre-release, lấy phiên bản cao nhất và chọn file `HVNRemoteHub-*.dmg` tải từ
`github.com`. Giữ đúng tên file này, nếu không app sẽ chỉ mở trang Release.

Bản 1.0.0 vẫn đọc `releases/latest` của repo cũ `hvngroup/mac-ultra-viewer`, nên 1.0.1 được phát hành ở repo cũ (tag
`v1.0.1`) trước khi repo đó được lưu trữ (archive). Từ 1.0.2 mọi bản chỉ phát hành ở repo chung.

Repo phải **công khai** (hoặc Release công khai) để app của người dùng đọc được thông tin phiên bản.

## Ký số

| Mức | Cách bật | Người dùng gặp |
|---|---|---|
| Ad-hoc (mặc định) | Không cần gì | Gatekeeper chặn lần đầu → Open Anyway; cập nhật trong app mở DMG thay vì tự cài |
| Developer ID + notarize | Thêm secrets bên dưới | Mở bình thường; cập nhật tự cài và mở lại |

Team ID của HVN GROUP: **`TVZNQ5W8NG`**. Team ID không phải bí mật (Apple in nó trong mọi chữ ký), nên được ghi thẳng
vào workflow (`env.APPLE_TEAM_ID`). Workflow chỉ nhận chứng chỉ "Developer ID Application" của đúng team này, và kiểm
`TeamIdentifier` của app sau khi ký.

### Chuẩn bị một lần (Account Holder hoặc Admin của tài khoản Apple Developer)

1. **Chứng chỉ Developer ID Application:** [developer.apple.com → Certificates](https://developer.apple.com/account/resources/certificates/list)
   → **+** → *Developer ID Application* → tải về, mở bằng Keychain Access → chuột phải vào chứng chỉ (kèm khoá riêng)
   → *Export* → định dạng `.p12`, đặt mật khẩu mạnh. Mã base64: `base64 -i DeveloperID.p12 | pbcopy`.
2. **Khoá API App Store Connect** (để notarize): [App Store Connect → Users and Access → Integrations → App Store Connect
   API](https://appstoreconnect.apple.com/access/integrations/api) → *Team Keys* → **+**, quyền **Developer** → tải file
   `AuthKey_<KEY_ID>.p8` (chỉ tải được **một lần**), ghi lại *Key ID* và *Issuer ID*.
3. Thêm secrets tại **Settings → Secrets and variables → Actions → New repository secret**.

Secrets phân loại **Tuyệt mật** theo ATTT HVN 01-01/11/2024: không dán vào chat, issue, email hay log; file `.p12`, `.p8` gốc
cất trong kho bí mật của HVN, xoá khỏi máy cá nhân sau khi thêm.

| Secret | Nội dung |
|---|---|
| `MACOS_CERTIFICATE_P12` | Chứng chỉ "Developer ID Application" dạng `.p12`, mã base64 |
| `MACOS_CERTIFICATE_PASSWORD` | Mật khẩu file `.p12` |
| `APPSTORE_API_KEY_P8` | Toàn bộ nội dung file `AuthKey_<KEY_ID>.p8`, từ dòng `-----BEGIN PRIVATE KEY-----` đến hết `-----END PRIVATE KEY-----` (hoặc mã base64 của file: `base64 -i AuthKey_<KEY_ID>.p8 \| pbcopy`) |
| `APPSTORE_API_KEY_ID` | Key ID |
| `APPSTORE_API_ISSUER_ID` | Issuer ID |
| `APPLE_ID`, `APPLE_APP_PASSWORD` | Phương án thay thế khoá API: Apple ID + app-specific password |

### Workflow làm gì

| Có gì | Kết quả |
|---|---|
| Không có chứng chỉ | Ký ad-hoc như trước |
| Chứng chỉ + thông tin notarize | Ký Developer ID với hardened runtime → notarize app → staple → `spctl` kiểm tra → ký, notarize, staple DMG |
| Chứng chỉ nhưng **thiếu** thông tin notarize | **Workflow dừng với lỗi.** App ký mà không notarize vẫn bị Gatekeeper chặn, nên không phát hành |
| Chứng chỉ của team khác | Workflow dừng với lỗi |

**Thử trước khi phát hành:** *Actions → Build → Run workflow* trên `main`. Lần chạy tay sẽ ký và notarize như bản phát hành
nhưng không đăng Release; tải artifact về Mac, mở thử, rồi chạy `spctl -a -vv "/Applications/HVN Remote Hub.app"` — kết
quả phải là `accepted` và `source=Notarized Developer ID`.

**Notarize lâu:** mỗi lần gửi Apple, workflow chờ tối đa 90 phút. Lần notarize đầu tiên của một tài khoản Apple
Developer có thể mất vài giờ; các lần sau thường vài phút. Nếu hết giờ chờ, hồ sơ vẫn được Apple xử lý tiếp: xem trạng
thái trên Mac bằng `xcrun notarytool history` (đăng nhập bằng cùng khoá API), đợi `Accepted` rồi chạy lại workflow. Với
Release, xoá Release và tag rồi tạo lại.

Lưu ý: chuyển từ ad-hoc sang Developer ID đổi danh tính ký, nên người dùng phải cấp lại quyền Ghi màn hình/Trợ năng
một lần và tải bản Developer ID đầu tiên thủ công.

---

HVN GROUP · hvn.vn
