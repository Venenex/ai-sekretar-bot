import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой AI-секретарь. Напиши задачу.")

# Ответ на любое сообщение
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    # Здесь можно подключить обработку через OpenAI, категоризацию и т.п.
    await update.message.reply_text(f"Задача принята: \"{user_message}\"")

# Обработка ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Ошибка при обработке обновления:", exc_info=context.error)

# Основная точка входа
def main():
    # 🔑 Укажи здесь свой токен Telegram-бота
    TOKEN = "7636640960:AAF8BqymLif1gIRuFtb03jjWytj7FNWGKcw"

    # Создаём приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
