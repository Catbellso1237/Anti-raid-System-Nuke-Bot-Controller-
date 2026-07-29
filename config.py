"""
Cấu hình trung tâm cho bot - đọc toàn bộ giá trị từ biến môi trường (.env)
Không hard-code token hay ID nhạy cảm trong code.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _parse_id_list(raw: str) -> set[int]:
    ids = set()
    if not raw:
        return ids
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            ids.add(int(part))
    return ids


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0") or 0)
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL", "").strip()

TRUSTED_IDS = _parse_id_list(os.getenv("TRUSTED_IDS", ""))

ACTION_THRESHOLD = int(os.getenv("ACTION_THRESHOLD", "3"))
ACTION_WINDOW_SECONDS = int(os.getenv("ACTION_WINDOW_SECONDS", "10"))

if not DISCORD_TOKEN:
    raise RuntimeError(
        "Thiếu DISCORD_TOKEN. Hãy tạo file .env dựa theo .env.example và điền token bot vào."
    )
