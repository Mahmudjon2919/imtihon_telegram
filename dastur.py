import os
import requests
from telebot import TeleBot

# Retrieve bot token from environment variable
BOT_TOKEN = os.environ.get("7149381183:AAEvLoeModFw-mkZNzrWzrAR_fRjPIgwETw")
POLLING_TIMEOUT = None

# Initialize the bot
bot = TeleBot("7149381183:AAEvLoeModFw-mkZNzrWzrAR_fRjPIgwETw")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Salom, Men sizga qanday yordam bera olaman?")


@bot.message_handler(commands=["holiday"])
def ask_country_code(message):
    """Prompts user for country code for holiday information."""
    Davlat = "Dam olish kunlari uchun davlat kodini kiriting (masalan, UZ):"
    bot.send_message(message.chat.id, Davlat)
    bot.register_next_step_handler(message, fetch_holidays)


def fetch_holidays(message):
    country_code = message.text.upper()
    year = 2024
    api_key = "nP5EjQWi9KDHNzVOySuULjOKLdgn6oWW"
    url = f"https://calendarific.com/api/v2/holidays?&api_key={api_key}&country={country_code}&year={year}"

    response = requests.get(url)

    if response.status_code == 200:
        holidays = response.json().get('response', {}).get('holidays', [])
        if holidays:
            holiday_message = "Dam olish kunlari:\n\n"
            for holiday in holidays:
                holiday_message += f"{holiday['name']} - {holiday['date']['iso']}\n"
            bot.send_message(message.chat.id, holiday_message)
        else:
            bot.send_message(message.chat.id, "Hech qanday dam olish kuni topilmadi.")
    else:
        bot.send_message(message.chat.id,
                         "Ma'lumotni olishda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")

    # Re-prompt for another country code
    ask_country_code(message)


if __name__ == "__main__":
    bot.polling(timeout=POLLING_TIMEOUT)
