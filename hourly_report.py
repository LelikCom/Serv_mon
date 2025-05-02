import csv
import datetime
import os
import psutil
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = "./log/speed_log.csv"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def read_last_hour_entries():
    now = datetime.datetime.now()
    hour_ago = now - datetime.timedelta(hours=1)
    results = []

    if not os.path.exists(LOG_PATH):
        return []

    with open(LOG_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = datetime.datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            if ts >= hour_ago:
                results.append({k: float(v) if k != "timestamp" else v for k, v in row.items()})
    return results

def get_docker_stats():
    try:
        output = subprocess.check_output(["docker", "ps", "--format", "{{.Names}} - {{.Status}}"], text=True)
        return output.strip()
    except:
        return "Docker info unavailable."

def build_report(data):
    if not data:
        return "Нет данных за последний час."

    avg = {k: round(sum(d[k] for d in data) / len(data), 2) for k in ["ping", "jitter", "download", "upload"]}

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    report = f"""
🕐 <b>Статистика за последний час</b>:
📶 Ping: <b>{avg['ping']} ms</b>
📈 Jitter: <b>{avg['jitter']} ms</b>
⬇️ Download: <b>{avg['download']} Mbps</b>
⬆️ Upload: <b>{avg['upload']} Mbps</b>

🖥 <b>Загрузка сервера</b>:
🧠 CPU: {cpu}%
📊 RAM: {ram.percent}% ({round(ram.used / 1e9, 1)} ГБ из {round(ram.total / 1e9, 1)} ГБ)
💾 Disk: {disk.percent}% свободно ({round(disk.free / 1e9, 1)} ГБ из {round(disk.total / 1e9, 1)} ГБ)

📦 <b>Docker-контейнеры:</b>
{get_docker_stats()}
    """.strip()

    return report

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

if __name__ == "__main__":
    report = build_report(read_last_hour_entries())
    send_telegram_message(report)
    print("✅ Telegram report sent")
