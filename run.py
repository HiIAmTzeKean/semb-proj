from flaskapp import create_app
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = create_app()
Bootstrap(app)
app.run(debug=True)
