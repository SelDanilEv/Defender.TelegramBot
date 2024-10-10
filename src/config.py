import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
IS_TEST_MODE = bool(int(os.getenv('IS_TEST_MODE')))
MONGO_URI = os.getenv('MONGO_URI')
SERVICE_URL = 'https://api.calendesk.com/api/available-slots'
HEADERS = {'x-tenant': '8vx7qbepcx'}