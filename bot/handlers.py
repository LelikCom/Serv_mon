from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from bot.keyboards import main_menu, exit_terminal_kb
from bot.states import TerminalState
from bot.terminal_access import run_command
import os
from bot.utils import build_stats_summary

router = Router()
ALLOWED_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))


@router.message(CommandStart())
async def start(message: Message):
    if message.chat.id != ALLOWED_CHAT_ID:
        return await message.answer("⛔ Доступ запрещён.")
    await message.answer("📡 Мониторинг активен. Выбери действие:", reply_markup=main_menu)


@router.callback_query(F.data == "get_log")
async def send_log(callback: CallbackQuery):
    if callback.message.chat.id != ALLOWED_CHAT_ID:
        return
    log_path = "./log/speed_log.csv"
    if os.path.exists(log_path):
        await callback.message.answer_document(FSInputFile(log_path))
    else:
        await callback.message.answer("⚠️ Лог-файл не найден.")
    await callback.answer()


@router.callback_query(F.data == "get_stats")
async def send_stats(callback: CallbackQuery):
    if callback.message.chat.id != ALLOWED_CHAT_ID:
        return
    summary = build_stats_summary()
    await callback.message.answer(summary)
    await callback.answer()


@router.callback_query(F.data == "start_terminal")
async def start_terminal(callback: CallbackQuery, state: FSMContext):
    if callback.message.chat.id != ALLOWED_CHAT_ID:
        return
    await state.set_state(TerminalState.active)
    await callback.message.answer("💻 Терминал активен. Введи команду:", reply_markup=exit_terminal_kb)
    await callback.answer()


@router.callback_query(F.data == "exit_terminal")
async def exit_terminal(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❎ Вы вышли из терминала.", reply_markup=main_menu)
    await callback.answer()


@router.message(TerminalState.active)
async def handle_terminal_input(message: Message):
    if message.chat.id != ALLOWED_CHAT_ID:
        return
    result = run_command(message.text)
    await message.answer(f"<pre>{result}</pre>")


@router.callback_query(F.data == "sys_status")
async def sys_status(callback: CallbackQuery):
    result = run_command("uptime && free -h && df -h")
    await callback.message.answer(f"<pre>{result}</pre>")
    await callback.answer()


@router.callback_query(F.data == "docker_ps")
async def docker_ps(callback: CallbackQuery):
    result = run_command("docker ps")
    await callback.message.answer(f"<pre>{result}</pre>")
    await callback.answer()


@router.callback_query(F.data == "docker_stats")
async def docker_stats(callback: CallbackQuery):
    result = run_command("docker stats --no-stream")
    await callback.message.answer(f"<pre>{result}</pre>")
    await callback.answer()


@router.callback_query(F.data == "bot_logs")
async def telegram_bot_logs(callback: CallbackQuery):
    result = run_command("cd Tele_VBA_Bot && docker logs telegram_bot --tail 50")
    await callback.message.answer(f"<pre>{result}</pre>")
    await callback.answer()


@router.callback_query(F.data == "restart_librespeed")
async def restart_librespeed(callback: CallbackQuery):
    result = run_command("docker restart librespeed")
    await callback.message.answer(f"<pre>{result}</pre>")
    await callback.answer()
