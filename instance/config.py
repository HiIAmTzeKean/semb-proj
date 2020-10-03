import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

print(basedir)
class Config:
    DEBUG = False
    SECRET_KEY = "this_is_trial_run"
    FLASK_ENV= 'production'
    PERMANENT_SESSION_LIFETIME =  timedelta(minutes=10)
    SESSION_REFRESH_EACH_REQUEST = True
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'flaskapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
