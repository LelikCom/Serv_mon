# 📡 Internet Monitor + Telegram Bot

Мониторинг скорости интернета, состояния сервера и Docker-контейнеров с управлением через Telegram-бота.

---

## ⚙️ Возможности

- ⏱ Автоматический замер скорости (LibreSpeed) каждые 5 минут  
- 🕐 Раз в час — отчёт в Telegram:
  - 📶 Ping, 📈 Jitter, ⬇️ Download, ⬆️ Upload  
  - 💽 CPU, RAM, диск  
  - 🐳 Docker-контейнеры (ps, stats, логи)  
- 🤖 Telegram-бот с inline-меню:
  - 📂 Скачать лог-файл
  - 📊 Статистика (сводка + по часам)
  - 💻 Терминал с безопасным bash
  - 🐳 Управление контейнерами
  - 🔄 Перезапуск LibreSpeed сервиса

---

## 📦 Установка и запуск

```bash
git clone https://github.com/LelikCom/Serv_mon.git
cd Serv_mon
cp .env.template .env     # заполни токен бота и данные БД
docker compose build
docker compose up -d
```

---

## 🔐 Переменные окружения

Файл `.env`:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# PostgreSQL
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

---

## 🗃️ Логирование

| Источник            | Хранилище         | Интервал     |
|---------------------|-------------------|--------------|
| Скорость интернета  | CSV + PostgreSQL  | каждые 5 мин |
| Системные метрики   | PostgreSQL        | каждые 10 мин|
| Docker-инфо         | PostgreSQL        | каждые 10 мин|
| Telegram отчёт      | Telegram чат      | раз в час    |

---

## 📁 Структура проекта

```
├── bot/                  # Telegram-бот (Aiogram 3)
├── loggers/              # Логгеры системы и Docker
├── log/                  # CSV-логи скорости
├── init_db.py            # Создание таблиц в PostgreSQL
├── start.sh              # Запуск всех процессов
├── run_speedtest.py      # Измерение скорости
├── hourly_report.py      # Telegram-отчёт
├── docker-compose.yml
├── requirements.txt
└── .env / .env.template
```