import requests
from telegram.ext import Updater, CommandHandler

TOKEN = "PASTE_YOUR_BOT_TOKEN"


CURRENCIES = ["USD", "EUR", "KZT", "RUB", "GBP"]


LANG = {}

TEXT = {
    "ru": {
        "start": " Бот обмена валют\n\nКоманды:\n/exchange USD EUR 100\n/rate USD EUR\n/language ru|kz|en",
        "result": " {a} {f} = {r} {t}\nКурс: 1 {f} = {rate} {t}",
        "rate": " Курс: 1 {f} = {rate} {t}"
    },
    "kz": {
        "start": " Валюта айырбастау боты\n\nКомандалар:\n/exchange USD EUR 100\n/rate USD EUR\n/language ru|kz|en",
        "result": "{a} {f} = {r} {t}\nБағам: 1 {f} = {rate} {t}",
        "rate": " Бағам: 1 {f} = {rate} {t}"
    },
    "en": {
        "start": " Currency exchange bot\n\nCommands:\n/exchange USD EUR 100\n/rate USD EUR\n/language ru|kz|en",
        "result": " {a} {f} = {r} {t}\nRate: 1 {f} = {rate} {t}",
        "rate": " Rate: 1 {f} = {rate} {t}"
    }
}

def get_rate(frm, to):
    url = f"https://api.exchangerate.host/latest?base={frm}&symbols={to}"
    data = requests.get(url).json()
    return round(data["rates"][to], 4)

def start(update, context):
    user = update.effective_user.id
    LANG[user] = "ru"
    update.message.reply_text(TEXT["ru"]["start"])

def language(update, context):
    user = update.effective_user.id
    try:
        lang = context.args[0]
        LANG[user] = lang
        update.message.reply_text("Language changed")
    except:
        update.message.reply_text("/language ru|kz|en")

def rate(update, context):
    user = update.effective_user.id
    lang = LANG.get(user, "ru")
    try:
        frm, to = context.args
        rate = get_rate(frm, to)
        update.message.reply_text(
            TEXT[lang]["rate"].format(f=frm, t=to, rate=rate)
        )
    except:
        update.message.reply_text("/rate USD EUR")

def exchange(update, context):
    user = update.effective_user.id
    lang = LANG.get(user, "ru")
    try:
        frm, to, amount = context.args
        amount = float(amount)
        rate = get_rate(frm, to)
        result = round(amount * rate, 2)
        update.message.reply_text(
            TEXT[lang]["result"].format(
                a=amount, f=frm, t=to, r=result, rate=rate
            )
        )
    except:
        update.message.reply_text("/exchange USD EUR 100")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("language", language))
    dp.add_handler(CommandHandler("rate", rate))
    dp.add_handler(CommandHandler("exchange", exchange))

    updater.start_polling()
    updater.idle()

main()