from flask import (
    Blueprint, flash, g, redirect, render_template, session, url_for
)
from datetime import datetime
from flaskapp.auth import login_required
from flaskapp.db import get_db
from .forms import paradestateform,paradestateviewform
from .methods import nameconverter_paradestateform, retrieve_personnel_list, retrieve_personnel_statuses
from .db_methods import update_PS,insert_PS,retrive_one_record

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
    if form.validate_on_submit():
        status_date = form.status_date.data
        personnel_id = form.name.data
        am_status = form.am_status.data
        am_remarks = form.am_remarks.data
        pm_status = form.pm_status.data
        pm_remarks = form.pm_remarks.data
        updated = False
        if retrive_one_record(db,personnel_id,status_date): 
            update_PS(db,personnel_id, status_date, am_status, am_remarks, pm_status,pm_remarks)
            updated = True
        else: 
            insert_PS(db,personnel_id, status_date, am_status, am_remarks, pm_status,pm_remarks)
        record = retrive_one_record(db,personnel_id,status_date)
        return render_template('misc/success.html', updated=updated, personnel=record)
    return render_template('ps/index.html', form=form)

@bp.route('/paradestate', methods=('GET', 'POST'))
@login_required
def paradestate():
    '''
    To view paradestate with date input
    View is only viewable to respective FMW lest Admin
    '''
    db = get_db()
    fmw = session.get('fmw')
    form = paradestateviewform()
    if form.validate_on_submit():
        date =  form.date.data
        personnels_status=retrieve_personnel_statuses(db,fmw,date)
        # None handler for those who have not submitted
        return render_template('ps/paradestate.html', personnels=personnels_status)
    return render_template('ps/paradestate.html', form=form)

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