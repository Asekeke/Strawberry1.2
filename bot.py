from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7581746741:AAFK9tL8BvgzJ8HbAV1CkBHzmdfOm4OAOzg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я живой бот. Напиши мне что-нибудь")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"🔹 Вы сказали: {user_text}\n"
                                    f"🔹 Длина: {len(user_text)} символов")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")

if __name__ == "__main__":  # Исправлено
    print("Запуск бота...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error)

    print("Бот работает!")
    app.run_polling()
