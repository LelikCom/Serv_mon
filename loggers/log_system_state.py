import os
import psutil
import subprocess
import datetime
import psycopg2


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


def log_to_db():
    # Сбор метрик
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    uptime = get_uptime()
    docker_list = get_docker_ps()
    docker_stat = get_docker_stats()

    # Подключение к БД
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    with conn:
        with conn.cursor() as cur:
            # system_metrics
            cur.execute("""
                INSERT INTO system_metrics (cpu_percent, ram_percent, disk_percent, uptime)
                VALUES (%s, %s, %s, %s)
            """, (cpu, ram, disk, uptime))

            # docker_info
            cur.execute("""
                INSERT INTO docker_info (container_list, stats)
                VALUES (%s, %s)
            """, (docker_list, docker_stat))

    conn.close()
    print(f"✅ Данные записаны: CPU={cpu}%, RAM={ram}%, Disk={disk}%")


if __name__ == "__main__":
    log_to_db()
