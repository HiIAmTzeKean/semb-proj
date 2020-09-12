from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskapp.auth import login_required

from flaskapp.db import get_db

from .forms import paradestateform

bp = Blueprint('ps', __name__)

# For all to submit their parade state
@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    fmw = "Sembawang" # Trial for Sembwang only
    rows = db.execute(
             'SELECT name FROM personnel WHERE fmw = ?', (fmw,)
         ).fetchall()
# Convert row object to name
    names = [] 
    for row in rows:
        names.append((row,row["name"]))
    form = paradestateform()
    form.name.choices = names
    if form.validate_on_submit():
# update database
        name = form.name.data
        am_status = form.am_status.data
        am_remarks = form.am_remarks.data
        pm_status = form.pm_status.data
        pm_remarks = form.pm_remarks.data
        db.execute(
            '''UPDATE personnel 
            SET am_status = ?, am_remarks = ?, pm_status = ?, pm_remarks = ?
            WHERE name = ?''', [am_status, am_remarks, pm_status, pm_remarks,name]
        )
        return redirect(url_for('ps.paradestate'))
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
@bp.route('/admin', methods=('GET', 'POST'))
@login_required
def admin():
    if g.user['username'] == 'Admin':
# displays admin functions
# 1. update changes 2. add/remove people
        return 'admin'

# show error 401 and forces user to login again
    return 'redirect'
