import telebot
from database import add_subscriber, remove_subscriber

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        subscribe_button = telebot.types.KeyboardButton('Subscribe')
        unsubscribe_button = telebot.types.KeyboardButton('Unsubscribe')
        markup.add(subscribe_button, unsubscribe_button)
        bot.send_message(message.chat.id, 'Welcome! Use the buttons below to subscribe or unsubscribe.', reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == 'Subscribe')
    def subscribe(message):
        chat_id = message.chat.id
        add_subscriber(chat_id)
        bot.reply_to(message, 'Subscribed successfully!')

    @bot.message_handler(func=lambda message: message.text == 'Unsubscribe')
    def unsubscribe(message):
        chat_id = message.chat.id
        remove_subscriber(chat_id)
        bot.reply_to(message, 'Unsubscribed successfully!')