import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

DBNAME = os.getenv("DBNAME")
MAIN_TABLE = os.getenv("MAIN_TABLE")

REGISTER_CHANNEL_ID = os.getenv("REGISTER_CHANNEL_ID")
