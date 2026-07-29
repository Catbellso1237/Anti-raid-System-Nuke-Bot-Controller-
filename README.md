# Anti-Nuke Sentinel Bot

Bot Discord bảo vệ server khỏi kiểu tấn công "bot/tài khoản giả danh anti-nuke":
được cấp quyền cao rồi âm thầm xóa kênh, xóa role, ban/kick hàng loạt để phá server.

## Cách hoạt động

1. **Giám sát audit log real-time** — bắt mọi hành động nguy hiểm (xóa kênh, xóa
   role, ban, kick, tạo webhook...) ngay khi xảy ra, không cần polling.
2. **Đếm theo cửa sổ thời gian** — nếu một tài khoản thực hiện nhiều hành động
   nguy hiểm liên tiếp trong thời gian ngắn (mặc định: 3 hành động / 10 giây),
   bot coi đó là tấn công.
3. **Giám sát cấp quyền Administrator** — bất kỳ ai không nằm trong whitelist
   được cấp quyền Administrator sẽ bị phát hiện và xử lý ngay lập tức, không
   cần chờ đủ ngưỡng.
4. **Phản ứng tự động**:
   - Tước toàn bộ role nguy hiểm của kẻ tấn công
   - Ban khỏi server
   - Khóa tạm thời server (chặn gửi tin / tạo invite mới của @everyone)
   - Gửi cảnh báo tới kênh log và webhook ngoài (nếu cấu hình)

## Cài đặt trên GitHub Codespaces

1. Fork/clone repo này, mở bằng **Codespaces** (nút "Code" → "Codespaces" → "Create codespace").
   Container sẽ tự cài Python 3.11 và các thư viện trong `requirements.txt`.
2. Tạo bot Discord tại https://discord.com/developers/applications:
   - Vào tab **Bot**, bật **Server Members Intent** và **Message Content Intent** (nếu cần).
   - Copy **Token**.
3. Trong terminal của Codespace:
   ```bash
   cp .env.example .env
   ```
   Sau đó mở `.env` và điền:
   - `DISCORD_TOKEN` — token bot vừa tạo
   - `LOG_CHANNEL_ID` — ID kênh dùng để nhận cảnh báo
   - `TRUSTED_IDS` — ID của bạn và các admin thật sự tin tưởng (cách nhau dấu phẩy)
4. Mời bot vào server với quyền: `Administrator` (bot cần quyền cao để có thể
   tước quyền của kẻ tấn công kịp thời) qua URL dạng:
   ```
   https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
   ```
5. Chạy bot:
   ```bash
   python bot.py
   ```

## Lệnh có sẵn

| Lệnh | Quyền | Mô tả |
|---|---|---|
| `!status` | Ai cũng dùng được | Xem trạng thái bảo vệ hiện tại |
| `!unlock` | Chỉ TRUSTED_IDS | Mở khóa server sau khi kiểm tra an toàn |
| `!trust <user_id>` | Chỉ TRUSTED_IDS | Thêm ID vào whitelist tạm thời (nhớ cập nhật `.env` để giữ vĩnh viễn) |

## Lưu ý quan trọng

- **Không commit file `.env`** — nó chứa token bot. File `.gitignore` đã loại trừ sẵn.
- Bot cần chạy 24/7 để giám sát liên tục — có thể deploy lên VPS, Railway,
  hoặc giữ Codespace chạy nền (Codespaces free tier sẽ tự ngủ sau một thời
  gian không hoạt động, không phù hợp cho chạy 24/7 lâu dài).
- Whitelist (`TRUSTED_IDS`) là tuyến phòng thủ quan trọng nhất — chỉ thêm ID
  của những người bạn tin tưởng tuyệt đối, vì họ sẽ không bị bot này chặn.
- Bot này **không** giả danh gì cả — mọi lệnh và hành vi đều minh bạch, không
  có backdoor hay lệnh ẩn.

## Cấu trúc file

```
anti-nuke-bot/
├── .devcontainer/devcontainer.json  # cấu hình Codespaces
├── bot.py                           # entry point
├── config.py                        # đọc biến môi trường
├── cogs/anti_nuke.py                # logic phát hiện & phản ứng
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
