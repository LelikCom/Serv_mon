import os
import psycopg2

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)


def init_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    with conn:
        with conn.cursor() as cur:
            # Таблица скорости
            cur.execute("""
                CREATE TABLE IF NOT EXISTS internet_speed (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    ping REAL,
                    jitter REAL,
                    download REAL,
                    upload REAL
                );
            """)
            # Таблица системных метрик
            cur.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    cpu_percent REAL,
                    ram_percent REAL,
                    disk_percent REAL,
                    uptime TEXT
                );
            """)
            # Таблица Docker
            cur.execute("""
                CREATE TABLE IF NOT EXISTS docker_info (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    container_list TEXT,
                    stats TEXT
                );
            """)

    conn.close()
    print("✅ Таблицы успешно созданы или уже существуют.")


if __name__ == "__main__":
    init_db()
