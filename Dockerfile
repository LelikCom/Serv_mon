FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем нужные системные утилиты
RUN apt update && apt install -y \
    iputils-ping \       # для ping
    procps \             # для uptime, free, top
    docker.io \          # для docker ps / stats
    curl \               # на всякий случай
    && apt clean

# Копируем по частям, чтобы всё точно попало
COPY start.sh .
COPY init_db.py .
COPY run_speedtest.py .
COPY hourly_report.py .

COPY bot/ ./bot/
COPY loggers/ ./loggers/

# Разрешаем запуск скрипта
RUN chmod +x start.sh

# Старт всей системы
CMD ["./start.sh"]
