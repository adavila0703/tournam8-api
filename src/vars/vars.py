from enum import Enum, unique
from dotenv import load_dotenv
import os

load_dotenv()

@unique
class Env(Enum):
    MONGO_CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING'),
    DB_NAME = os.environ.get('DB_NAME')