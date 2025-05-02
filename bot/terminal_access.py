import subprocess

# Можно дополнить список
BLOCKED_PATTERNS = ["rm", "reboot", "shutdown", ":", ";", ">", "<", "`", "$(", "kill", "dd", "mkfs"]


def run_command(command: str) -> str:
    try:
        if any(bad in command for bad in BLOCKED_PATTERNS):
            return "⛔ Команда запрещена системой безопасности."

        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        output = result.stdout.strip() or result.stderr.strip() or "✅ Команда выполнена."

        if len(output) > 4000:
            output = output[:4000] + "\n\n...Обрезано."

        return output

    except subprocess.TimeoutExpired:
        return "⏱ Команда превысила лимит времени (15 секунд)."

    except Exception as e:
        return f"❌ Ошибка: {e}"
