import schedule
import time
from utils import fetch_data

def start_scheduler():
    schedule.every(10).minutes.do(fetch_data)

    while True:
        schedule.run_pending()
        time.sleep(1)

def initialize_scheduler():
    import threading
    threading.Thread(target=start_scheduler).start()