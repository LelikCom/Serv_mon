import pandas as pd
import os

LOG_PATH = "./log/speed_log.csv"

def build_stats_summary() -> str:
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
            return "📊 Нет данных за текущие сутки."

        # Средние по дню
        mean_day = df_day[["ping", "jitter", "download", "upload"]].mean().round(2)

        # Средние по часам
        hourly = (
            df_day.groupby("hour")[["ping", "jitter", "download", "upload"]]
            .mean()
            .round(2)
            .reset_index()
        )

        # Формируем текст
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
