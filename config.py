import os
basedir = os.path.abspath(os.path.dirname(__file__))

print(basedir)
class Config:
    DEBUG = False
    SECRET_KEY = "this_is_trial_run"
    FLASK_ENV= 'production'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'flaskapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False