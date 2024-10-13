import telebot
from classes import User
from database import activate_user, add_user, deactivate_user, get_active_subscribers, get_user_by_username, subscribe_user, unsubscribe_user
from utils import fetch_data
from config import logger


def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        force_check_button = telebot.types.KeyboardButton('Check')
        subscribe_button = telebot.types.KeyboardButton('Subscribe')
        unsubscribe_button = telebot.types.KeyboardButton('Unsubscribe')
        get_chat_id_button = telebot.types.KeyboardButton('Get my chat id')
        markup.add(force_check_button,subscribe_button, unsubscribe_button,get_chat_id_button)

        user = User.from_chat_info(message.chat)
        add_user(user)

        bot.send_message(message.chat.id, 'Welcome! Use the buttons below to subscribe or unsubscribe.', reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == 'Subscribe')
    def subscribe(message):
        user = User.from_chat_info(message.chat)
        subscribe_user(user)
        bot.reply_to(message, 'Subscribed successfully!')

    @bot.message_handler(func=lambda message: message.text == 'Unsubscribe')
    def unsubscribe(message):
        user = User.from_chat_info(message.chat)
        unsubscribe_user(user)
        bot.reply_to(message, 'Unsubscribed successfully!')

    @bot.message_handler(func=lambda message: message.text == 'Check')
    def check(message):
        user = User.from_chat_info(message.chat)
        active_subscribers = get_active_subscribers()
        
        # Check if the user is in the list of active subscribers
        if any(sub.chat_id == user.chat_id for sub in active_subscribers):
            if not fetch_data():
                bot.reply_to(message, 'There is no free slots!')
        else:
            bot.reply_to(message, 'You are not an active subscriber.')

    @bot.message_handler(func=lambda message: message.text == 'Get my chat id')
    def getChatId(message):
        bot.reply_to(message, message.chat.id)


    @bot.message_handler(commands=['a'])
    def activate(message):
        try:
            user = get_user_by_username(message.text.split()[1])
            if not user:
                bot.reply_to(message, 'User not found!')
                return
            
            activate_user(user)
            bot.reply_to(message, f'User {user.chat_id}:{user.username} activated successfully!')
            bot.send_message(user.chat_id, 'You have been activated!')
        except IndexError:
            bot.reply_to(message, 'Please provide a username.')
    
    @bot.message_handler(commands=['da'])
    def deactivate(message):
        try:
            user = get_user_by_username(message.text.split()[1])
            if not user:
                bot.reply_to(message, 'User not found!')
                return
            
            deactivate_user(user)
            bot.send_message(user.chat_id, 'You have been deactivated!')
            bot.reply_to(message, f'User {user.chat_id}:{user.username} deactivated successfully!')
        except IndexError:
            bot.reply_to(message, 'Please provide a username.')