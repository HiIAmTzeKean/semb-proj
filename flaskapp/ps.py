from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskapp.auth import login_required

from flaskapp.db import get_db

from .forms import paradestateform

bp = Blueprint('ps', __name__)

# For all to submit their parade state
@bp.route('/')
def index():
    form = paradestateform()
    if form.validate_on_submit():
        pass
    return render_template('ps/index.html', form=form)

# For COS to retrive parade state to send via whatsapp
@bp.route('/paradestate')
def paradestate():
# Access db to retive records
    db = get_db()
    fmw = "Sembawang" # Trial for Sembwang only
    personnels = db.execute(
             'SELECT * FROM personnel WHERE fmw = ?', (fmw,)
         ).fetchall()
    return render_template('ps/paradestate.html',personnels=personnels)

# view only to admin
@bp.route('/admin')
@login_required
def admin():
    if g.user['username'] == 'Admin':
# displays admin functions
# 1. update changes 2. add/remove people
        return 'admin'

# show error 401 and forces user to login again
    return 'redirect'
