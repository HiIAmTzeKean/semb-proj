from flask import (
    Blueprint, g, redirect, render_template, url_for
)
from flaskapp.db import get_db
from .forms import paradestateform
import git

bp = Blueprint('misc', __name__)

# successful upload page
@bp.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('misc/success.html')

# generate route for webhook
@bp.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/HiIAmTzeKean/semb-proj.git')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400