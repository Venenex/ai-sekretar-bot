from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "7636640960:AAF8BqymLif1gIRuFtb03jjWytj7FNWGKcw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой AI-секретарь. Напиши задачу.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Задача добавлена: {text}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(msg="Произошла ошибка:", exc_info=context.error)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
