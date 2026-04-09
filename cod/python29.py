import telebot 
import requests

BOT_TOKEN = ""
API_KEY = ""

bot = telebot.TeleBot(BOT_TOKEN)

def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        rates = data.get("conversion_rates", {})
        return rates.get(target_currency, None)
    else:
        return None


@bot.message_handler(commands=["start", "help"])
def help_message(message):
    bot.reply_to(message, "Пример: 100 USD KZT")


@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        amount, base_currency, target_currency = message.text.split()
        amount = float(amount)

        exchange_rate = get_exchange_rate(base_currency.upper(), target_currency.upper())

        if exchange_rate:
            converted_amount = amount * exchange_rate
            bot.reply_to(
                message,
                f"{amount} {base_currency.upper()} = {converted_amount} {target_currency.upper()}"
            )
        else:
            bot.reply_to(message, "Ошибка: нет такой валюты или проблема с API.")

    except ValueError:
        bot.reply_to(message, "❗ Формат: 100 USD KZT")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")


if __name__ == "__main__":
    bot.polling()

