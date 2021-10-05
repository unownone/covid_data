import os
from dotenv import load_dotenv

load_dotenv('.env')

class Config(object):
    SECRET_KEY = os.getenv('master_key')
    MONGO_URI = os.getenv('mongo_uri')