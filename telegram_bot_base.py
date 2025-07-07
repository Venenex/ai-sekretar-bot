import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой AI-секретарь. Чем могу помочь?")

# Главная функция
def main():
    app = ApplicationBuilder().token("7636640960:AAF8BqymLif1gIRuFtb03jjWytj7FNWGKcw").build()

    app.add_handler(CommandHandler("start", start))

    # Запускаем бота
    app.run_polling()

if __name__ == '__main__':
    main()
