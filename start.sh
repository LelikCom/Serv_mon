#!/bin/bash

# 1. Инициализация базы
python3 init_db.py

# 2. Каждые 5 минут — тест скорости
while true; do
    python3 run_speedtest.py
    sleep 300
done &

# 3. Каждые 10 минут — лог системных метрик и docker
while true; do
    python3 loggers/log_system_state.py
    sleep 300
done &

# 4. Раз в час — Telegram отчёт
while true; do
    sleep 3600
    python3 hourly_report.py
done
