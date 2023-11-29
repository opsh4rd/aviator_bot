import telebot

# Токен вашего бота и ID вашего чата
bot_token = '...'  # Бот токен
bot_chatID = '...'  # Чат, где бот
bot = telebot.TeleBot(bot_token)


# Отправка сообщения в чат-бот
def send_notification(message):
    bot.send_message(bot_chatID, message)
