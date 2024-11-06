import telebot
from config import TOKEN

def update_bot_instance():
    bot = telebot.TeleBot(TOKEN)

bot = telebot.TeleBot(TOKEN)