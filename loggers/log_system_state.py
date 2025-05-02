import os
import psutil
import subprocess
import datetime
import psycopg2
import json


def get_uptime() -> str:
    try:
        return subprocess.check_output("uptime -p", shell=True, text=True).strip()
    except:
        return "n/a"


def get_docker_ps() -> str:
    try:
        return subprocess.check_output("docker ps --format '{{.Names}} - {{.Status}}'", shell=True, text=True).strip()
    except:
        return "n/a"


def get_docker_stats() -> str:
    try:
        return subprocess.check_output("docker stats --no-stream", shell=True, text=True).strip()
    except:
        return "n/a"


def clean_unit(val: str) -> float:
    """Удаляет единицы измерения и конвертирует в float"""
    return float(
        val.replace('Gi', '')
           .replace('Mi', '')
           .replace('Ti', '')
           .replace('G', '')
           .replace('M', '')
           .replace('T', '')
           .replace('i', '')
    )


def insert_sys_status(cur):
    try:
        uptime_raw = subprocess.check_output("uptime", shell=True, text=True).strip()
        free = subprocess.check_output("free -h", shell=True, text=True).strip().splitlines()
        load_avg = uptime_raw.split("load average: ")[1].split(", ")
        users = int(uptime_raw.split(" user")[0].split()[-1])

        ram = free[1].split()
        ram_total, ram_used = ram[1], ram[2]
        ram_pct = int(clean_unit(ram_used) / clean_unit(ram_total) * 100)

        swap = free[2].split()
        swap_total, swap_used = swap[1], swap[2]
        swap_pct = int(clean_unit(swap_used) / clean_unit(swap_total) * 100) if swap_total != "0M" else 0

        uptime_str = uptime_raw.split(" up ")[1].split(",")[0]

        # Топ процессов
        top_output = subprocess.check_output("ps aux --sort=-%mem | head -n 6", shell=True, text=True)
        top_lines = top_output.strip().splitlines()[1:]
        top_data = []
        for line in top_lines:
            parts = line.split(None, 10)
            if len(parts) == 11:
                top_data.append({"cmd": parts[10], "mem": parts[3]})

        cur.execute("""
            INSERT INTO system_metrics (
                uptime, users, load_1min, load_5min, load_15min,
                ram_total, ram_used, ram_pct,
                swap_total, swap_used, swap_pct,
                top_processes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            uptime_str, users, float(load_avg[0]), float(load_avg[1]), float(load_avg[2]),
            ram_total, ram_used, ram_pct,
            swap_total, swap_used, swap_pct,
            json.dumps(top_data)
        ))

    except Exception as e:
        print(f"❌ Ошибка при логировании системных метрик: {e}")


def log_to_db():
    # Сбор базовых метрик
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    uptime = get_uptime()
    docker_list = get_docker_ps()
    docker_stat = get_docker_stats()

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    with conn:
        with conn.cursor() as cur:
            # system_metrics (basic)
            cur.execute("""
                INSERT INTO system_metrics (cpu_percent, ram_percent, disk_percent, uptime)
                VALUES (%s, %s, %s, %s)
            """, (cpu, ram, disk, uptime))

            # docker_info
            cur.execute("""
                INSERT INTO docker_info (container_list, stats)
                VALUES (%s, %s)
            """, (docker_list, docker_stat))

            # Дополнительно: расширенные системные метрики
            insert_sys_status(cur)

    conn.close()
    print(f"✅ Данные записаны: CPU={cpu}%, RAM={ram}%, Disk={disk}%")


if __name__ == "__main__":
    log_to_db()
