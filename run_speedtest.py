import os
import csv
import datetime
import speedtest
import psycopg2

# Пути и настройки
log_path = "./log/speed_log.csv"
write_header = not os.path.exists(log_path)

# Выполняем тест
s = speedtest.Speedtest()
s.get_best_server()
download = s.download()
upload = s.upload()
ping = s.results.ping
jitter = s.results.dict().get("jitter", 0)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

row = {
    "timestamp": timestamp,
    "ping": round(ping, 2),
    "jitter": round(jitter, 2),
    "download": round(download / 1e6, 2),
    "upload": round(upload / 1e6, 2)
}

# Сохраняем в CSV
os.makedirs("./log", exist_ok=True)
with open(log_path, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    if write_header:
        writer.writeheader()
    writer.writerow(row)

print("✅ Записано в CSV:", row)

# Сохраняем в PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO internet_speed (ping, jitter, download, upload)
                VALUES (%s, %s, %s, %s)
            """, (row["ping"], row["jitter"], row["download"], row["upload"]))
    conn.close()
    print("✅ Записано в БД.")
except Exception as e:
    print("❌ Ошибка записи в БД:", e)
