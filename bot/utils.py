import pandas as pd
import os
import subprocess
import datetime

LOG_PATH = "./log/speed_log.csv"

def build_stats_summary() -> str:
    """
    Читает лог скорости, рассчитывает средние значения за последний день и по часам.
    Возвращает HTML-строку со сводкой.
    """
    if not os.path.exists(LOG_PATH):
        return "⚠️ Лог-файл отсутствует."

    try:
        df = pd.read_csv(LOG_PATH, parse_dates=["timestamp"])
        df = df.sort_values("timestamp")
        df["date"] = df["timestamp"].dt.date
        df["hour"] = df["timestamp"].dt.strftime("%H:00")

        last_day = df["date"].max()
        df_day = df[df["date"] == last_day]

        if df_day.empty:
            return f"📊 Нет данных за {last_day}."

        mean_day = df_day[["ping", "jitter", "download", "upload"]].mean().round(2)
        hourly = (
            df_day.groupby("hour")[["ping", "jitter", "download", "upload"]]
            .mean()
            .round(2)
            .reset_index()
        )

        summary = f"<b>📊 Статистика за {last_day}</b>\n\n"
        summary += (
            f"<b>Средние значения:</b>\n"
            f"🕐 Время: {df_day['timestamp'].min().strftime('%H:%M')}–{df_day['timestamp'].max().strftime('%H:%M')}\n"
            f"📶 Ping: <b>{mean_day['ping']} ms</b>\n"
            f"📈 Jitter: <b>{mean_day['jitter']} ms</b>\n"
            f"⬇️ Download: <b>{mean_day['download']} Mbps</b>\n"
            f"⬆️ Upload: <b>{mean_day['upload']} Mbps</b>\n\n"
        )

        summary += "<b>По часам:</b>\n"
        for _, row in hourly.iterrows():
            summary += (
                f"{row['hour']}: ⏱ {row['ping']}ms | 📈 {row['jitter']}ms | "
                f"⬇️ {row['download']}Mbps | ⬆️ {row['upload']}Mbps\n"
            )

        return summary

    except Exception as e:
        return f"❌ Ошибка при обработке лога: {e}"

def format_sys_status() -> str:
    def clean_unit(val: str) -> float:
        return float(
            val.replace('Gi', '')
               .replace('Mi', '')
               .replace('Ti', '')
               .replace('G', '')
               .replace('M', '')
               .replace('T', '')
               .replace('i', '')
        )

    try:
        now = datetime.datetime.now().strftime("%H:%M")
        uptime_raw = subprocess.check_output("uptime", shell=True, text=True).strip()
        free = subprocess.check_output("free -h", shell=True, text=True).strip().splitlines()
        df = subprocess.check_output("df -h | grep -E '^(/dev|overlay)'", shell=True, text=True).strip().splitlines()
        top_output = subprocess.check_output("ps aux --sort=-%mem | head -n 6", shell=True, text=True)

        # uptime + нагрузка
        parts = uptime_raw.split(" up ")
        uptime_info = parts[1].split(",")[0]
        load_avg = uptime_raw.split("load average: ")[1]
        users = uptime_raw.split(" user")[0].split()[-1]

        # память
        ram = free[1].split()
        ram_total, ram_used = ram[1], ram[2]
        ram_pct = int(clean_unit(ram_used) / clean_unit(ram_total) * 100)

        swap = free[2].split()
        swap_total, swap_used = swap[1], swap[2]
        swap_pct = int(clean_unit(swap_used) / clean_unit(swap_total) * 100) if swap_total != "0M" else 0

        # диски
        disk_lines = []
        for line in df:
            parts = line.split()
            mount = parts[-1]
            used = parts[2]
            total = parts[1]
            percent = parts[4]
            disk_lines.append(f"📁 {mount} — {percent} — {used} / {total}")

        # топ процессов
        top_lines = top_output.strip().splitlines()[1:]
        top_formatted = []
        for line in top_lines:
            parts = line.split(None, 10)
            if len(parts) == 11:
                top_formatted.append(f"🔹 {parts[10]} — {parts[3]}% MEM")

        # итоговое сообщение
        msg = f"<b>📊 Состояние сервера на {now}</b>\n\n"
        msg += f"🕒 Аптайм: {uptime_info}\n"
        msg += f"👥 Пользователи: {users}\n"
        msg += f"💻 Загрузка (1/5/15 мин): {load_avg}\n\n"
        msg += f"💾 Память: <b>{ram_pct}%</b> — {ram_used} / {ram_total}\n"
        msg += f"💤 Swap: <b>{swap_pct}%</b> — {swap_used} / {swap_total}\n\n"
        msg += "🗂 <b>Диски:</b>\n" + "\n".join(disk_lines) + "\n\n"
        msg += "<b>🔥 Топ по памяти:</b>\n" + "\n".join(top_formatted)

        return msg

    except Exception as e:
        return f"<b>❌ Ошибка:</b> {e}"

