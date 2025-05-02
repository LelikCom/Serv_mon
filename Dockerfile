FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем нужные системные утилиты
RUN apt update && apt install -y \
    iputils-ping \
    procps \
    docker.io \
    curl \
    && apt clean

# Копируем необходимые файлы
COPY start.sh .
COPY init_db.py .
COPY run_speedtest.py .
COPY hourly_report.py .

# Копируем директории с ботом и логгерами
COPY bot/ ./bot/
COPY loggers/ ./loggers/

# Даём права на запуск основного скрипта
RUN chmod +x start.sh

# Старт всей системы
CMD ["./start.sh"]
