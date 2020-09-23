from flaskapp import create_app
from flask_bootstrap import Bootstrap

def run_app():
    app = create_app()
    Bootstrap(app)
    return app

if __name__ == "__main__":
    app = run_app()
    app.run()