## Thay đổi gì và vì sao

<!-- Mô tả thay đổi và lý do. Gắn issue nếu có. -->

## Checklist

- [ ] Workflow **Build** xanh trên commit hiện tại (`swift test`, đóng gói, `verify-bundle.sh`)
- [ ] `python3 scripts/check-localizations.py` qua; chuỗi giao diện mới có trong cả `vi.lproj` và `en.lproj`
- [ ] Thay đổi người dùng thấy được có một dòng trong `CHANGELOG.md` (mục Unreleased)
- [ ] Không commit chứng chỉ, khoá, mật khẩu, ID đối tác, token phiên hay ảnh chụp giao thức
- [ ] Đã chạy thử trên Mac thật theo `docs/manual-test-checklist.md` nếu thay đổi giao diện hoặc hành vi
