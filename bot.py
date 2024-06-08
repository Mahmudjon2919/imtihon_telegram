import os
import requests
import telebot
from datetime import date

# Replace with your actual Telegram bot token
BOT_TOKEN = os.environ.get("7149381183:AAEvLoeModFw-mkZNzrWzrAR_fRjPIgwETw")

bot = telebot.TeleBot(BOT_TOKEN)

def get_holidays(country_code: str, year: int = date.today().year) -> dict:
    url = "https://calendarific.com/api/v2/holidays?"
    params = {
        "api_key": "nP5EjQWi9KDHNzVOySuULjOKLdgn6o",
        "country": country_code.upper(),
        "year": year
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("response", {}).get("holidays", [])

def get_country_preference(message):
    user_id = message.chat.id

    # Example (replace with your preference storage implementation):
    return user_preferences.get(user_id, None)

# Message handler for "/start" command
@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.reply_to(message, "Salom, Sizga qanday yordam berishim mumkin?")

# Message handler for "/holiday" command
@bot.message_handler(commands=["holiday"])
def holiday_handler(message):
    country_code = get_country_preference(message)  # Retrieve user's preferred country code

    if not country_code:
        # Offer options to set or view preferred country code
        options_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        options_markup.add("Mamlakat kodini o'rnatish", "Mavjud kodni ko'rish")
        bot.reply_to(message, "Sizga qaysi davlat kerak?\nTanlang:", reply_markup=options_markup)
        return

    try:
        holidays = get_holidays(country_code)
        if not holidays:
            bot.reply_to(message, f"Siz tanlagan mamlakatda ({country_code.upper()}) 2024-yil uchun dam olish kunlari topilmadi.")
            return

        holiday_info = "\n".join(f"{h['date']['iso']}: {h['name']}" for h in holidays)
        bot.reply_to(message, f"{country_code.upper()}dagi dam olish kunlari:\n{holiday_info}")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Dam olish kunlari ma'lumotlarini olishda xatolik yuzaga keldi: {e}")

# Message handler for setting/viewing country code preference
@bot.message_handler(func=lambda msg: msg.text in ("Mamlakat kodini o'rnatish", "Mavjud kodni ko'rish"))
def handle_country_preference(message):
    user_id = message.chat.id
    if message.text == "Mamlakat kodini o'rnatish":
        # Prompt user to enter their preferred country code
        bot.reply_to(message, "Iltimos, siz yashash mamlakatingiz kodini kiriting (masalan, UZ):")


    elif message.text == "Mavjud kodni ko'rish":
        country_code = get_country_preference(message)
        if country_code:
            bot.reply_to(message, f"Sizning hozirgi mamlakat kodingiz: {country_code.upper()}")
        else:
            bot
