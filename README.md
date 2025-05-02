# Internet Monitor + Telegram Bot

📡 Мониторинг скорости интернета, состояния сервера и Docker с управлением через Telegram-бота.

---

## ⚙️ Функциональность

- Измерение скорости каждые 5 минут (`LibreSpeed`)
- Раз в час отправка отчёта в Telegram:
  - Ping, jitter, upload/download
  - CPU, RAM, диск
  - Docker-контейнеры
- Telegram-бот с inline-меню:
  - 📂 Скачать лог
  - 📊 Статистика
  - 💻 Терминал с безопасным bash
  - 🐳 Docker: `ps`, `stats`, рестарт, логи

---

## 📦 Установка

```bash
git clone https://github.com/yourname/internet_monitor.git
cd internet_monitor
cp .env.template .env  # и заполни токен + chat_id
docker compose build
docker compose up -d
