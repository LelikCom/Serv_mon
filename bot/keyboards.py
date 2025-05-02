from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📂 Лог-файл", callback_data="get_log")],
    [InlineKeyboardButton(text="📊 Статистика", callback_data="get_stats")],
    [InlineKeyboardButton(text="💻 Терминал", callback_data="start_terminal")],
    [InlineKeyboardButton(text="💽 CPU/RAM", callback_data="sys_status")],
    [InlineKeyboardButton(text="🐳 Docker ps", callback_data="docker_ps")],
    [InlineKeyboardButton(text="📊 Docker stats", callback_data="docker_stats")],
    [InlineKeyboardButton(text="📜 Логи Telegram-бота", callback_data="bot_logs")],
    [InlineKeyboardButton(text="🔄 Перезапустить LibreSpeed", callback_data="restart_librespeed")]
])

exit_terminal_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚫 Выйти из терминала", callback_data="exit_terminal")]
])
