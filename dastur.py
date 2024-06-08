import os
import  telebot
import requests
BOT_TOKEN=os.environ.get("7149381183:AAEvLoeModFw-mkZNzrWzrAR_fRjPIgwETw")
bot=telebot.TeleBot(BOT_TOKEN)
@bot.message_handlers(commands=["start", "Hello"])
def send_welcome(message):
    bot.reply_to(message, "Salom, Sizga qanday yordam berishim mumkin?")
@bot.message_handlers(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    bot.infinity_pollinng()
def holiday_days(sign:str, day:str) ->dict:
    url="https://calendarific.com/api/v2/holidays?"
    params={"sign":sign, "day":day}
    response=requests.get(url,params)
    return response.json()


@bot.message_handlers(commands=["holiday"])
def sign_handler(message):
    text="Sizga qaysi davlat kerak?\nDavlat kodini tanlang:"