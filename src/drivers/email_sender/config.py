import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("MAIL_HOST")
USERNAME = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")
PORT = os.getenv("MAIL_PORT", 456)