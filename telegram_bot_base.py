import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# Ответ на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш AI-секретарь 🤖. Отправьте голосовое или текстовое сообщение!")

# Заглушка для голосовых сообщений (без Whisper)
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    voice_path = f"voice_{update.message.message_id}.ogg"
    await file.download_to_drive(voice_path)

    await update.message.reply_text("🎤 Голосовое сообщение получено. (распознавание временно отключено)")
    
    # Временно: просто подставим фейковый текст
    transcribed_text = "распознавание временно отключено"

    # Тут можно что-то делать с transcribed_text, например сохранить в базу, отправить и т.п.
    await update.message.reply_text(f"📝 Текст сообщения: {transcribed_text}")

# Ответ на текстовые сообщения
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Вы написали: {text}")

# Запуск бота
if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")  # Задай токен как переменную среды или вставь прямо сюда (не рекомендую)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен...")
    app.run_polling()
