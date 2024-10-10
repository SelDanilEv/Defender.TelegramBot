from bot_instance import bot
from handlers import register_handlers
from scheduler import initialize_scheduler

register_handlers(bot)
initialize_scheduler()

if __name__ == '__main__':
    bot.polling()