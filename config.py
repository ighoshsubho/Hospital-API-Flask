import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_here'
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_URI')
    }
