import telebot

token="8458822803:AAGw5RajT345CZc8j9-KcvEnMoJp34OXkZ8"

bot = telebot.Telebot("token")
@bot.message_handler(commands=["start"])
