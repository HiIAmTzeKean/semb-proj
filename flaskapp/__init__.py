import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__, instance_relative_config=True, template_folder='templates')

# load config
app.config.from_pyfile('config.py', silent=False)
app.config.from_object(Config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from . import models

from . import auth
app.register_blueprint(auth.bp)

from . import ps
app.register_blueprint(ps.bp)
app.add_url_rule('/', endpoint='index')

from . import misc
app.register_blueprint(misc.bp)

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'hello world'
