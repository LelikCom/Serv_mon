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
                    uptime TEXT,
                    users INTEGER,
                    load_1min REAL,
                    load_5min REAL,
                    load_15min REAL,
                    ram_total TEXT,
                    ram_used TEXT,
                    ram_pct INTEGER,
                    swap_total TEXT,
                    swap_used TEXT,
                    swap_pct INTEGER,
                    top_processes TEXT
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
