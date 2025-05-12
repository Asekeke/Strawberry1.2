from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "7581746741:AAFK9tL8BvgzJ8HbAV1CkBHzmdfOm4OAOzg"

def start(update, context):
    update.message.reply_text("🚀 Бот запущен! /help")

def help(update, context):
    update.message.reply_text("Справка:\n/start\n/help")

def unknown(update, context):
    update.message.reply_text("Неизвестная команда 😢")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    print("Бот работает! 🌍")
    updater.start_polling()
    updater.idle()

if name == "main":
    main()