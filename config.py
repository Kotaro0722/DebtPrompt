import os
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("TOKEN")

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

DBNAME = os.getenv("DBNAME")
MAIN_TABLE = os.getenv("MAIN_TABLE")

REGISTER_CHANNEL_ID = os.getenv("REGISTER_CHANNEL_ID")
