import os
import logging
import openai_whisper
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Инициализация Whisper (для голосовых сообщений)
whisper_model = openai_whisper.load_model("base")  # Модель Whisper (base, small, medium, large)

# Временное хранилище задач
tasks = {}

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я — AI-секретарь 🤖\n\nОтправь мне задачу текстом или голосом, и я её сохраню.\n"
        "Доступные команды:\n/добавить — добавить задачу\n/все — показать все задачи"
    )

# Команда /добавить
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task_text = ' '.join(context.args)
    if not task_text:
        await update.message.reply_text("Напиши задачу после команды. Например: /добавить Купить молоко")
        return
    tasks.setdefault(user_id, []).append(task_text)
    await update.message.reply_text(f"✅ Задача добавлена: {task_text}")

# Команда /все
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_tasks = tasks.get(user_id, [])
    if not user_tasks:
        await update.message.reply_text("У вас пока нет задач.")
    else:
        response = "\n".join([f"{i+1}. {task}" for i, task in enumerate(user_tasks)])
        await update.message.reply_text("📝 Ваши задачи:\n" + response)

# Обработка голосовых сообщений
async def handle_voice(update_
