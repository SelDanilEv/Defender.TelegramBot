import time
from bot_instance import bot,update_bot_instance
from handlers import register_handlers
from scheduler import initialize_scheduler

register_handlers(bot)
initialize_scheduler()

def start_polling():
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)  # Wait for 5 seconds before restarting
            update_bot_instance()


if __name__ == '__main__':
    start_polling()