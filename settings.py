from flask import Config
from datetime import timedelta


class Settings(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db?check_same_thread=False'
    SECRET_KEY = '740d9e58782809e59424751c9b5279af09e707febe831fec78ff1e2571f52b89'
    SESSION_TYPE = 'filesystem'
