from flask import (
    Blueprint, flash, g, redirect, render_template, session, url_for
)
from datetime import datetime
from flaskapp.auth import login_required
from flaskapp.db import get_db
from .forms import paradestateform
from .methods import nameconverter_paradestateform, retrieve_personnel_list, retrieve_member_statuses

bp = Blueprint('ps', __name__)

# For all to submit their parade state
@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    # Trial for Sembawang only
    fmw = "Sembawang"
    rows = retrieve_personnel_list(db, fmw)
    names = nameconverter_paradestateform(rows)
    form = paradestateform()
    form.name.choices = names
    # date to be changed to drop down box in the future for uploading
    form.status_date.data = datetime.today().strftime('%Y-%m-%d')
    if form.validate_on_submit():
        # update database
        status_date = form.status_date.data
        personnel_id = form.name.data
        am_status = form.am_status.data
        am_remarks = form.am_remarks.data
        pm_status = form.pm_status.data
        pm_remarks = form.pm_remarks.data

        sql_str = '''INSERT INTO "personnel_status" (personnel_id, date, time, status, remarks)
            VALUES (?,?,?,?,?)'''

        db.execute(sql_str, (personnel_id, status_date, 'AM', am_status, am_remarks))
        db.execute(sql_str, (personnel_id, status_date, 'PM', pm_status, pm_remarks))
        db.commit()

        return redirect(url_for('misc.success'))
    return render_template('ps/index.html', form=form)

# For COS to retrive parade state to send via whatsapp
@bp.route('/paradestate')
@login_required
def paradestate():
    db = get_db()
    fmw = session.get('fmw')
    # check if func work. Not working on my end
    statuses = retrieve_member_statuses(db, fmw, '2020-09-14', 'AM')
    return render_template('ps/paradestate.html', personnels=statuses)

# view only to admin
@bp.route('/admin', methods=('GET', 'POST'))
@login_required
def admin():
    if session.get('user_id') == 'Admin':
    # displays admin functions
    # 1. add/remove people to db
    # 2. any additional functions? Hq level scope?
        return render_template('ps/admin.html')
    # show error 401 and forces user to login again
    return 'You are not authorised, please log in as Admin'