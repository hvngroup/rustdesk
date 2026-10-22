# Phase P0 — Máy chủ HVN Connect thử nghiệm trên HVN Cloud (Việt Nam)

- Mục tiêu: chạy máy chủ ID/rendezvous (`hbbs`) và relay (`hbbr`) của RustDesk OSS trên HVN Cloud; đo chất lượng kết
  nối ở Việt Nam bằng client RustDesk gốc **trước khi** fork và đổi thương hiệu.
- Người làm: đội hạ tầng HVN Cloud. Agent không có quyền vào máy chủ.
- Phân loại: Nội bộ. Khoá riêng của máy chủ: **Tuyệt mật** (ATTT HVN 01-01/11/2024).

## 1. Chuẩn bị

| Hạng mục | Giá trị gợi ý |
|---|---|
| Máy chủ | VPS Linux (Ubuntu 24.04 LTS), 2 vCPU, 4 GB RAM, 40 GB SSD, IP tĩnh; băng thông lớn vì relay mang toàn bộ hình ảnh khi không kết nối thẳng được |
| Tên miền | `connect.hvn.vn` (bản ghi A → IP máy chủ) — đã chốt |
| Phần mềm | Docker + Docker Compose; image `rustdesk/rustdesk-server`, **ghim phiên bản** (bản mới nhất trên GitHub là `1.1.16`; kiểm tra tag tương ứng trên Docker Hub), không dùng `latest` |

## 2. Tường lửa

| Cổng | Giao thức | Dịch vụ | Bắt buộc |
|---|---|---|---|
| 21115 | TCP | `hbbs` — kiểm tra kiểu NAT | Có |
| 21116 | TCP + **UDP** | `hbbs` — đăng ký ID, đục lỗ NAT (hole punching) | Có |
| 21117 | TCP | `hbbr` — relay | Có |
| 21118, 21119 | TCP | WebSocket cho web client | Chỉ khi dùng web client |

Chỉ mở đúng các cổng trên; SSH chỉ cho dải IP quản trị của HVN.

## 3. Triển khai

`docker-compose.yml` (thư mục `/opt/hvn-connect`):

```yaml
services:
  hbbs:
    image: rustdesk/rustdesk-server:1.1.16   # ghim đúng tag đã kiểm tra
    command: hbbs -r connect.hvn.vn:21117
    ports: ["21115:21115", "21116:21116", "21116:21116/udp"]
    volumes: ["./data:/root"]
    depends_on: [hbbr]
    restart: unless-stopped
  hbbr:
    image: rustdesk/rustdesk-server:1.1.16
    command: hbbr
    ports: ["21117:21117"]
    volumes: ["./data:/root"]
    restart: unless-stopped
```

```sh
cd /opt/hvn-connect && docker compose up -d
docker compose logs --tail 50
```

Lần chạy đầu, `hbbs` sinh cặp khoá trong `./data`:

- `id_ed25519.pub` — **khoá công khai**. Đưa cho agent ở Phase P2 (gắn vào `RS_PUB_KEY` của client HVN).
- `id_ed25519` — **khoá riêng, Tuyệt mật**. Không gửi qua chat/email, không commit; sao lưu mã hoá vào kho bí mật của
  HVN. Mất khoá này thì mọi client đã phát hành phải cập nhật khoá mới.

Bật chế độ bắt buộc khoá để máy lạ không dùng ké máy chủ (xem tài liệu của đúng phiên bản `rustdesk-server` đang chạy).

## 4. Đo thử (dùng client RustDesk gốc)

1. Trên hai máy (một Windows, một Mac), vào **Settings → Network → ID/Relay server**: ID server `connect.hvn.vn`, Key =
   nội dung `id_ed25519.pub`.
2. Thử các tình huống, mỗi tình huống ghi: kết nối thẳng hay relay, độ trễ khi gõ, FPS, chất lượng hình:
   - cùng mạng LAN;
   - hai nhà mạng khác nhau (Viettel ↔ VNPT/FPT);
   - một máy dùng 4G/5G;
   - một máy sau NAT doanh nghiệp/tường lửa chặt.
3. Theo dõi tải máy chủ (`docker stats`) và băng thông relay.

## 5. Tiêu chí đạt

- [ ] Hai máy kết nối được qua `connect.hvn.vn` ở cả 4 tình huống.
- [ ] Máy không có khoá đúng bị từ chối.
- [ ] Khoá riêng đã sao lưu mã hoá; chỉ người được giao giữ.
- [ ] Bảng số đo gửi chủ sản phẩm. Từ đó quyết định cấu hình máy chủ thật (một vùng hay nhiều vùng, băng thông relay).

## Hoàn tác

`docker compose down` và xoá VPS. Chưa có client nào của HVN phụ thuộc vào máy chủ này.

---

HVN GROUP · hvn.vn
