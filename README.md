# Anti-Nuke (CWC Introduce)

Bot Discord bảo vệ server khỏi kiểu tấn công "bot/tài khoản giả danh anti-nuke": được cấp quyền cao rồi âm thầm xóa kênh, xóa role, ban/kick hàng loạt để phá server.

## Cách hoạt động

1. **Giám sát audit log real-time** — bắt mọi hành động nguy hiểm (xóa kênh, xóa role, ban, kick, tạo webhook...) ngay khi xảy ra, không cần polling.
2. **Đếm theo cửa sổ thời gian** — nếu một tài khoản thực hiện nhiều hành động nguy hiểm liên tiếp trong thời gian ngắn (mặc định: 3 hành động / 10 giây), bot coi đó là tấn công.
3. **Giám sát cấp quyền Administrator** — bất kỳ ai không nằm trong whitelist được cấp quyền Administrator sẽ bị phát hiện và xử lý ngay lập tức, không cần chờ đủ ngưỡng.
4. **Phản ứng tự động**:
   - Tước toàn bộ role nguy hiểm của kẻ tấn công
   - Ban khỏi server
   - Khóa tạm thời server (chặn gửi tin / tạo invite mới của @everyone)
   - Gửi cảnh báo tới kênh log và webhook ngoài (nếu cấu hình)

---

## Cài đặt — chọn nền tảng phù hợp

Bot cần **chạy liên tục 24/7** để giám sát server không gián đoạn. Mỗi nền tảng dưới đây có ưu/nhược điểm khác nhau về việc duy trì uptime — đọc kỹ phần "Lưu ý" của từng mục trước khi chọn.

### 1. Termux (Android)

Phù hợp nếu bạn muốn chạy trực tiếp trên điện thoại, không cần máy tính.

**Yêu cầu:**
- Cài Termux (khuyến nghị lấy từ F-Droid, bản trên Google Play đã ngừng cập nhật)
- Python 3 (`py3`) — cài qua Termux
- Plugin/gói hỗ trợ Discord cho Termux (một số thiết lập Termux cần thêm gói `libffi`, `openssl` để `discord.py` cài đặt được đầy đủ)

**Các bước:**
```bash
pkg update && pkg upgrade
pkg install python git libffi openssl
git clone https://github.com/Catbellso1237/Anti-raid-System-Nuke-Bot-Controller-.git
cd Anti-raid-System-Nuke-Bot-Controller-
pip install -r requirements.txt
cp .env.example .env
nano .env   # điền DISCORD_TOKEN, LOG_CHANNEL_ID, TRUSTED_IDS
python bot.py
```

**Lưu ý quan trọng:**
- Termux sẽ bị hệ điều hành Android **tắt nền (kill)** sau một thời gian nếu không có biện pháp giữ chạy. Cài thêm gói `termux-wake-lock` và chạy lệnh `termux-wake-lock` trước khi start bot để hạn chế bị tắt.
- Thời gian bot "treo" (chạy liên tục) phụ thuộc vào cấu hình tiết kiệm pin của từng máy Android — không đảm bảo 24/7 tuyệt đối như máy chủ thật.
- Nếu tắt app Termux hoặc khởi động lại máy, bot sẽ dừng — cần mở lại và chạy `python bot.py` thủ công (trừ khi bạn tự cấu hình auto-start).

---

### 2. GitHub Codespaces

Giống hướng dẫn gốc — phù hợp để **test nhanh**, không cần cài gì trên máy.

**Các bước:**
1. Vào repo → nút **Code** → tab **Codespaces** → **Create codespace on main**
2. Container tự cài Python 3.11 và các thư viện trong `requirements.txt`
3. Trong terminal của Codespace:
   ```bash
   cp .env.example .env
   ```
   Mở `.env`, điền `DISCORD_TOKEN`, `LOG_CHANNEL_ID`, `TRUSTED_IDS`
4. Chạy:
   ```bash
   python bot.py
   ```

**Lưu ý quan trọng:**
- **Codespaces KHÔNG phù hợp để chạy 24/7.** Gói miễn phí của GitHub giới hạn số giờ sử dụng mỗi tháng, và Codespace sẽ **tự động ngủ (sleep)** sau khoảng 30 phút không hoạt động — bot sẽ dừng theo.
- Phù hợp nhất để: test code, debug, chỉnh sửa nhanh — không phù hợp làm nơi host bot vĩnh viễn.
- Nếu cần chạy 24/7 thật sự, nên cân nhắc VPS hoặc dịch vụ hosting bot chuyên dụng (Railway, Render, v.v.) thay vì Codespaces.

---

### 3. Windows (CMD)

Phù hợp nếu bạn có máy tính Windows sẵn sàng chạy liên tục.

**Yêu cầu:** đã cài [Git for Windows](https://git-scm.com/download/win) và [Python 3](https://www.python.org/downloads/) (nhớ tick "Add Python to PATH" lúc cài).

**Các bước (CMD):**
```cmd
git clone https://github.com/Catbellso1237/Anti-raid-System-Nuke-Bot-Controller-.git
cd Anti-raid-System-Nuke-Bot-Controller-
pip install -r requirements.txt
copy .env.example .env
notepad .env
```
Điền `DISCORD_TOKEN`, `LOG_CHANNEL_ID`, `TRUSTED_IDS` vào Notepad rồi lưu, sau đó chạy:
```cmd
python bot.py
```

**Lưu ý quan trọng:**
- Thao tác trên CMD **phức tạp hơn** so với Termux và Codespaces — dễ gặp lỗi liên quan tới biến môi trường PATH, phiên bản Python không khớp, hoặc thiếu quyền cài đặt. Nếu chưa quen dòng lệnh Windows, nên thử Codespaces trước để chắc code chạy đúng, rồi mới chuyển sang Windows.
- Nếu chọn chạy bot trên Windows, **bắt buộc máy phải bật và cửa sổ CMD phải luôn mở 24/7** — tắt máy, đóng CMD, hoặc máy vào chế độ ngủ (sleep) đều làm bot dừng hoạt động. Cần tắt tính năng ngủ màn hình/máy tính (Settings → Power) nếu muốn duy trì uptime liên tục.
- Muốn bot tự khởi động lại khi treo hoặc khi khởi động máy, cần tự thiết lập thêm (Task Scheduler hoặc script `.bat` lặp lại khi bot thoát).

---

## Lệnh có sẵn

| Lệnh | Quyền | Mô tả |
|---|---|---|
| `!status` | Ai cũng dùng được | Xem trạng thái bảo vệ hiện tại |
| `!unlock` | Chỉ TRUSTED_IDS | Mở khóa server sau khi kiểm tra an toàn |
| `!trust <user_id>` | Chỉ TRUSTED_IDS | Thêm ID vào whitelist tạm thời (nhớ cập nhật `.env` để giữ vĩnh viễn) |
| `?emoji` | Chỉ TRUSTED_IDS | Mở **panel quản lý Application Emoji** (xem mục bên dưới) |

## Quản lý Emoji liên kết Discord Developer Portal (`?emoji`)

Cog `cogs/emoji_manager.py` quản lý **Application Emoji** — loại emoji gắn liền
với chính con bot (application), hiển thị trong **Discord Developer Portal →
ứng dụng của bạn → mục "Emojis"**. Khác với emoji thường gắn vào 1 server,
loại này thuộc về bot và bot có thể dùng ở **bất kỳ server nào nó có mặt**.

**Cách dùng:** gõ đúng `?emoji` (tiền tố riêng `?`, không dùng chung `!` của
các lệnh khác) trong kênh Discord — bot sẽ mở ra một **panel** gồm các nút:

| Nút | Chức năng |
|---|---|
| ➕ Thêm | Mở form (modal) nhập **Tên** + **URL ảnh** để tạo emoji mới (PNG/JPG/GIF, tối đa 256KB) |
| ✏️ Đổi tên | Mở menu chọn 1 emoji có sẵn rồi mở form nhập tên mới |
| 🗑️ Xóa | Mở menu chọn 1 emoji, yêu cầu xác nhận trước khi xóa |
| 🔄 Làm mới | Tải lại danh sách emoji mới nhất từ Developer Portal |
| ✖️ Đóng | Khóa toàn bộ nút, đóng panel |

Toàn bộ thao tác **chỉ dùng nút bấm / menu chọn / form nhập liệu** của
Discord — không cần gõ thêm lệnh text nào sau `?emoji`.

**Quyền sử dụng:** chỉ tài khoản trong `TRUSTED_IDS` (hoặc chủ sở hữu bot)
mới thấy và dùng được panel này, vì Application Emoji ảnh hưởng tới **toàn
bộ bot** ở mọi server, không giới hạn trong 1 server như emoji thường.

**Lưu ý:** cần bật intent **Message Content** trong Developer Portal của
bot (Bot → Privileged Gateway Intents → Message Content Intent) thì bot mới
đọc được lệnh `?emoji`.

## Lưu ý chung

- **Không commit file `.env`** — nó chứa token bot. File `.gitignore` đã loại trừ sẵn.
- Whitelist (`TRUSTED_IDS`) là tuyến phòng thủ quan trọng nhất — chỉ thêm ID của những người bạn tin tưởng tuyệt đối, vì họ sẽ không bị bot này chặn.
- Bot này **không** giả danh gì cả — mọi lệnh và hành vi đều minh bạch, không có backdoor hay lệnh ẩn.
- Mời bot vào server với quyền `Administrator` (bot cần quyền cao để tước quyền của kẻ tấn công kịp thời) qua URL dạng:
  ```
  https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
  ```

## Cấu trúc file

```
anti-nuke-bot/
├── .devcontainer/devcontainer.json  # cấu hình Codespaces
├── bot.py                           # entry point
├── config.py                        # đọc biến môi trường
├── cogs/anti_nuke.py                # logic phát hiện & phản ứng
├── cogs/emoji_manager.py            # panel quản lý Application Emoji ("?emoji")
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
