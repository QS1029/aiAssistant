import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('API_KEY')
YANDEX_TOKEN = os.getenv('YAN_KEY')