import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__, instance_relative_config=True, template_folder='templates')
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskapp.sqlite'),
)

# load the instance config
app.config.from_pyfile('config.py', silent=False)
app.config.from_object(Config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from flask_bootstrap import Bootstrap
Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from . import models

from . import auth
app.register_blueprint(auth.bp)

# for parade state page
from . import ps
app.register_blueprint(ps.bp)
app.add_url_rule('/', endpoint='index')

# for misc pages
from . import misc
app.register_blueprint(misc.bp)

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'hello world'