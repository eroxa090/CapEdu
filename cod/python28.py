import telebot
import requests
from telebot import types
BOT_TOKEN = "8378024957:AAFMEMNS198R5gkDxsusDDrt3JaWDUhaBgM"
API_KEY = "1a3bbb5c6b15e65c72ad46a3"


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


@bot.message_handler(commands=["start"])
def start_message(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("USD → KZT")
    btn2 = types.KeyboardButton("KZT → USD")
    btn3 = types.KeyboardButton("EUR → USD")
    btn4 = types.KeyboardButton("Другие валюты")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Привет! \n"
        "Я конвертирую валюты.\n\n"
        "Примеры:\n"
        "• 100 USD KZT\n"
        "• USD KZT (сумма = 1)\n\n"
        "Выберите валюты на клавиатуре или введите вручную.",
        reply_markup=markup
    )

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.reply_to(
        message,
        "📘 *Как пользоваться ботом:*\n\n"
        "1️⃣ Введите сумму и валюты:\n"
        "`100 USD KZT`\n\n"
        "2️⃣ Можно без суммы:\n"
        "`USD KZT` → будет считаться как 1 единица\n\n"
        "3️⃣ Можно нажимать кнопки на клавиатуре\n\n"
        "*Поддерживаются любые ISO валюты: USD, EUR, KZT, GBP и др.*",
        parse_mode="Markdown"
    )



@bot.message_handler(func=lambda m: m.text in ["USD → KZT", "KZT → USD", "EUR → USD"])
def handle_predefined(message):
    mapping = {
        "USD → KZT": ("USD", "KZT"),
        "KZT → USD": ("KZT", "USD"),
        "EUR → USD": ("EUR", "USD")
    }

    base, target = mapping[message.text]
    rate = get_exchange_rate(base, target)

    if rate:
        bot.reply_to(message, f"1 {base} = {rate} {target}")
    else:
        bot.reply_to(message, "Ошибка: API недоступно.")


@bot.message_handler(func=lambda m: m.text == "Другие валюты")
def ask_custom(message):
    bot.send_message(message.chat.id, "Введите валюты, например: GBP JPY или 10 GBP JPY")


@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    parts = message.text.split()

    try:
        
        if len(parts) == 3:
            amount = float(parts[0])
            base = parts[1].upper()
            target = parts[2].upper()

        elif len(parts) == 2:
            amount = 1       
            base = parts[0].upper()
            target = parts[1].upper()

        else:
            bot.reply_to(message, " Формат: 100 USD KZT или USD KZT")
            return

        rate = get_exchange_rate(base, target)
        if not rate:
            bot.reply_to(message, "Ошибка: неверная валюта или API недоступно.")
            return

        converted = amount * rate
        bot.reply_to(message, f"{amount} {base} = {converted} {target}")

    except ValueError:
        bot.reply_to(message, " Ошибка: проверьте формат данных.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

if __name__ == "__main__":
    bot.polling()
