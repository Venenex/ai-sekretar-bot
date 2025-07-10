import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой AI-секретарь. Напиши задачу.")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"Задача добавлена: {user_message}")

# Обработка ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Ошибка при обработке обновления:", exc_info=context.error)

def main():
    TOKEN = "7636640960:AAF8BqymLif1gIRuFtb03jjWytj7FNWGKcw"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
