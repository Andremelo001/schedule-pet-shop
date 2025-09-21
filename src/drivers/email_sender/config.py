import os
from dotenv import load_dotenv

load_dotenv()
# Carregar .env.local se existir (sobrescreve configurações para desenvolvimento local)
load_dotenv('.env.local', override=True)

HOST = os.getenv("MAIL_HOST")
USERNAME = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")
PORT = int(os.getenv("MAIL_PORT", 587))