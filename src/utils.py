import random
import requests
from datetime import datetime
from config import SERVICE_URL, HEADERS, IS_TEST_MODE, logger
from database import get_active_subscribers
from bot_instance import bot
from database import add_to_cache


employee_id = 5
employee_id_str = str(employee_id)

def generate_random_object():
    return {
        'id': random.randint(1, 100),
        'name': f'Item{random.randint(1, 100)}',
        'value': random.random()
    }

def fetch_data():
    today = datetime.now().strftime('%Y-%m-%d')
    params = {
        'used_slots': 1,
        'number_of_days': 100,
        'service_id': 1,
        'employee_ids': employee_id,
        'start_date': today,
        'customer_time_zone': 'Europe/Warsaw'
    }
    try:
        if len(get_active_subscribers()) == 0:
            logger.info('No active subscribers')
            return False

        response = requests.get(SERVICE_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        if IS_TEST_MODE:
            for date in data[employee_id_str]:
                data[employee_id_str][date] = [generate_random_object() for _ in range(random.randint(0, 1))]

            filtered_data = {date: slots for date, slots in data[employee_id_str].items() if slots}
            if filtered_data:
                notify_subscribers(filtered_data)
        else:
            filtered_data = {date: slots for date, slots in data[employee_id_str].items() if slots}
            if filtered_data:
                notify_subscribers(filtered_data)
    except requests.RequestException as e:
        logger.error(f'Error fetching data: {e}')
        return False

    return bool(filtered_data)

def notify_subscribers(data):
    for activeUser in get_active_subscribers():
        try:
            message = "Available slots:\n" + "\n".join([f"{date}: {len(slots)} slots" for date, slots in data.items()])
            bot.send_message(activeUser.chat_id, message)
            logger.info(f'Notification sent to {activeUser.chat_id}')
        except Exception as e:
            logger.error(f'Error sending message to {activeUser.chat_id}: {e}')
    add_to_cache(data)
    