from dotenv import load_dotenv
import os

load_dotenv()

ENV = {
    'MONGO_CONNECTION_STRING': os.environ.get('MONGO_CONNECTION_STRING'),
    'DB_NAME': os.environ.get('DB_NAME')
}