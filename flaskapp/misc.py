from flask import (
    Blueprint, g, redirect, render_template, url_for
)
from flaskapp.db import get_db
from .forms import paradestateform

bp = Blueprint('misc', __name__)

# For all to submit their parade state
@bp.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('misc/success.html')

# generate route for error page