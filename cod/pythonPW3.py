from telegram.ext import Updater, CommandHandler
import datetime

TOKEN = "7992532689:AAHJ09gRe0x0p6P725aD-k1pjRBHDy22G7I"

users = {}  
DAILY_NORM = 2000  

def start(update, context):
    update.message.reply_text(
        " Привет!\n\n"
        "Я бот для напоминания пить воду.\n\n"
        "Команды:\n"
        "/setreminder 1 — напоминание каждые 1 час\n"
        "/drank 300 — выпил 300 мл воды\n"
        "/status — проверить водный баланс"
    )

def set_reminder(update, context):
    try:
        hours = int(context.args[0])
        chat_id = update.message.chat_id

        if chat_id not in users:
            users[chat_id] = {"water": 0, "last_date": datetime.date.today()}

        context.job_queue.run_repeating(
            remind_water,
            interval=hours * 3600,
            first=0,
            context=chat_id
        )

        update.message.reply_text(f" Напоминание установлено каждые {hours} час(а).")
    except:
        update.message.reply_text(" Используй: /setreminder 1")

def remind_water(context):
    chat_id = context.job.context
    context.bot.send_message(
        chat_id=chat_id,
        text=" Не забывай пить воду! Выпей стакан воды."
    )

def drank(update, context):
    try:
        amount = int(context.args[0])
        chat_id = update.message.chat_id
        today = datetime.date.today()

        if chat_id not in users or users[chat_id]["last_date"] != today:
            users[chat_id] = {"water": 0, "last_date": today}

        users[chat_id]["water"] += amount

        update.message.reply_text(f" Записано: {amount} мл воды.")
    except:
        update.message.reply_text(" Используй: /drank 300")

def status(update, context):
    chat_id = update.message.chat_id
    today = datetime.date.today()

    if chat_id not in users or users[chat_id]["last_date"] != today:
        users[chat_id] = {"water": 0, "last_date": today}

    drank = users[chat_id]["water"]
    remaining = max(0, DAILY_NORM - drank)

    update.message.reply_text(
        f" Сегодня выпито: {drank} мл\n"
        f" Осталось: {remaining} мл из 2000 мл"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setreminder", set_reminder))
    dp.add_handler(CommandHandler("drank", drank))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
