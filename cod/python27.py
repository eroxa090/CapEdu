import telebot
import requests

bot = telebot.TeleBot("8458822803:AAGw5RajT345CZc8j9-KcvEnMoJp34OXkZ8")
API_KEY = " d205476b01894f95afe85939253011"

def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(url).json()

        city_name = response['location']['name']
        temp = response['current']['temp_c']
        condition = response['current']['condition']['text']

        return f"Город: {city_name}\n Температура: {temp}°C\n Погода: {condition}"
    except:
        return " Город введён неправильно или не найден."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Напиши название города — скажу погоду ")

@bot.message_handler(content_types=['text'])
def send_weather(message):
    city = message.text
    weather_report = get_weather(city)
    bot.reply_to(message, weather_report)

bot.polling()