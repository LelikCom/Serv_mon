FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем основной код
COPY run_speedtest.py .
COPY hourly_report.py .
COPY start.sh .
COPY bot/ ./bot/

RUN mkdir -p /app/log
RUN chmod +x start.sh

CMD ["./start.sh"]
