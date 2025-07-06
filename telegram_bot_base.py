import os
import logging
import whisper
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Инициализация Whisper (модель base)
whisper_model = whisper.load_model("base")

# Временное хранилище задач
tasks = {}

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я — AI-секретарь 🤖\n\n"
        "Отправь мне задачу текстом или голосом, и я её сохраню.\n"
        "Доступные команды:\n"
        "/добавить — добавить задачу\n"
        "/все — показать все задачи"
    )


# Команда /добавить
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task_text = ' '.join(context.args)
    if not task_text:
        await update.message.reply_text("Напиши задачу после команды. Например: /добавить Купить молоко")
        return
    tasks.setdefault(user_id, []).append(task_text)
    await update.message.reply_text("✅ Задача добавлена!")


# Команда /все
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_tasks = tasks.get(user_id, [])
    if not user_tasks:
        await update.message.reply_text("🗒️ У вас пока нет задач.")
        return
    response = "\n".join([f"{i+1}. {task}" for i, task in enumerate(user_tasks)])
    await update.message.reply_text("📝 Ваши задачи:\n" + response)


# Обработка голосовых сообщений и их расшифровка через Whisper
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    voice_path = f"voice_{update.message.message_id}.ogg"
    await file.download_to_drive(voice_path)
    await update.message.reply_text("🎤 Голосовое сообщение получено. Распознаю текст...")

    try:
        audio = whisper.load_audio(voice_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
        _, probs = whisper_model.detect_language(mel)
        transcription = whisper_model.transcribe(audio)
        transcribed_text = transcription["text"]
        await update.message.reply_text(f"📝 Распознано: {transcribed_text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при распознавании: {str(e)}")
        return


# Основной запуск
def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("❌ Не указан BOT_TOKEN в переменных окружения.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("добавить", add_task))
    app.add_handler(CommandHandler("все", list_tasks))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("✅ Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
