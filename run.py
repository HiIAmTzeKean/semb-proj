from flaskapp import create_app
from flask_bootstrap import Bootstrap

app = create_app()
Bootstrap(app)
app.run(debug=True)
