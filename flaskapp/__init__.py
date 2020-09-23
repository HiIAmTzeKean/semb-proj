import os
from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # load the instance config
    app.config.from_pyfile('config.py', silent=False)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flask_bootstrap import Bootstrap
    Bootstrap(app)

    from . import db
    db.init_app(app)

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

    return app


app = create_app()
