from flask import (Blueprint, flash, g, redirect, render_template, session, url_for, make_response, request)
from datetime import timedelta,datetime
from flaskapp.auth import login_required, clearance_one_required, fmw_required
from flaskapp.db import get_db
from .forms import (paradestateform, paradestateviewform, admin_add_del_form, admin_paradestateviewform,
                    strengthviewform, admin_three_add_del_form, admin_three_act_deact_form)
from .methods import nameconverter_paradestateform, retrieve_personnel_list, retrieve_personnel_statuses
from .db_methods import (retrive_record_by_date, submit_PS,
                         add_del_personnel_db, retrive_one_record, act_deact_personnel_db,
                         retrive_personnel_id, check_personnel_exist)

bp = Blueprint('ps', __name__)


@bp.route('/', methods=('GET', 'POST'))
@fmw_required
def index():
    '''
    Uploading of parade state to DB
    Clearance 1: Nil
    Clearance 3: Nil
    '''
    db = get_db()
    fmw = session.get('fmw')
    rows = retrieve_personnel_list(db, fmw)
    names = nameconverter_paradestateform(rows)
    form = paradestateform()
    form.name.choices = names
    updated = False
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        if end_date>start_date:
            flash("Your end date is earlier than your start date")
            return render_template('ps/index.html', form=form, updated=updated, personnel=None)
        personnel_id = form.name.data
        am_status = form.am_status.data
        am_remarks = form.am_remarks.data
        pm_status = form.pm_status.data
        pm_remarks = form.pm_remarks.data
        if start_date == end_date:
            submit_PS(db,personnel_id, start_date, am_status, am_remarks, pm_status, pm_remarks)
            multi_date = False
        else:
            date = start_date
            while date != (end_date + timedelta(days=1)):
                submit_PS(db,personnel_id, date, am_status, am_remarks, pm_status, pm_remarks)
                date = date + timedelta(days=1)
            multi_date =True
        updated = True
        record = retrive_record_by_date(db, personnel_id, start_date)
        resp = make_response(render_template('ps/index.html', form=form, updated=updated,
                            multi_date=multi_date, personnel=record, end_date=end_date))
        resp.set_cookie('personnel_id', value = str(personnel_id), max_age=60*60*24)
        return resp

        # return render_template('ps/index.html', form=form, updated=updated,
        #                         multi_date=multi_date, personnel=record, end_date=end_date)

    record = retrive_record_by_date(db, request.cookies.get('personnel_id'), datetime.date(datetime.today()) )
    if record:
        form.name.data = record['id']
        form.am_status.data = record['am_status']
        form.am_remarks.data = record['am_remarks']
        form.pm_status.data = record['pm_status']
        form.pm_remarks.data = record['pm_remarks']
        
    return render_template('ps/index.html', form=form, updated=updated, personnel=None)


@bp.route('/paradestate', methods=('GET', 'POST'))
@login_required
def paradestate():
    '''
    View paradestate with date input
    Clearance 1: Select FMW and FMD to view
    Clearance 3: View current FMW
    '''
    db = get_db()
    if session.get('clearance') <= 2:
        form = admin_paradestateviewform()
    else:
        form = paradestateviewform()
    if form.validate_on_submit():
        if session.get('clearance') <= 2: fmw = form.fmw.data
        else: fmw = session.get('fmw')
        date = form.date.data
        personnels_status, missing_status = retrieve_personnel_statuses(db, fmw, date)
        if len(personnels_status) != 0:
            return render_template('ps/paradestate.html', personnels=personnels_status,
                                   missing_personnels=missing_status, date=date)
        flash("No one has submitted PS. Please remind them to do so!")
    return render_template('ps/paradestate.html', form=form)


@bp.route('/strengthviewer', methods=('GET', 'POST'))
@login_required
def strengthviewer():
    '''
    Display current strength in FMW
    Clearance 1: Select FMW and FMD to view
    Clearance 3: View current FMW
    '''
    db = get_db()
    if session.get('clearance') <= 2:
        form = strengthviewform()
        if form.validate_on_submit():
            fmw = form.fmw.data
            personnels = retrieve_personnel_list(db, fmw)
            if personnels != []:
                return render_template('ps/strengthviewer.html', fmw=fmw, personnels=personnels)
            flash('No personnel in selected FMW yet.')
        return render_template('ps/select_fmw.html', form=form)
    else:
        fmw = session.get('fmw')
        personnels = retrieve_personnel_list(db, fmw)
        return render_template('ps/strengthviewer.html', fmw=fmw, personnels=personnels)
    

@bp.route('/admin/add_del_personnel', methods=('GET', 'POST'))
@login_required
def admin_add_del():
    db = get_db()
    if session.get('clearance') <= 2:
        form = admin_add_del_form()
    else:
        form = admin_three_add_del_form()
    if form.validate_on_submit():
        name = form.name.data
        rank = form.rank.data
        if session.get('clearance') <= 2: fmw = form.fmw.data
        else: fmw = session.get('fmw')
        add_del = form.add_del.data
        error, personnel = add_del_personnel_db(db,name,fmw,rank,add_del)
        if error == None:
            return render_template('ps/admin_add_del.html', add_del=add_del, personnel=personnel)
        flash(error)
    return render_template('ps/admin_add_del.html', form=form)


@bp.route('/admin/act_deact', methods=('GET', 'POST'))
@login_required
def admin_act_deact():
    db = get_db()
    if session.get('clearance') <= 2:
        form = admin_act_deact_form()
    else:
        form = admin_three_act_deact_form()
    if form.validate_on_submit():
        name = form.name.data
        rank = form.rank.data
        if session.get('clearance') <= 2: fmw = form.fmw.data
        else: fmw = session.get('fmw')
        act_deact = form.act_deact.data
        error = check_personnel_exist(db, name, fmw, rank)
        if error == None:
            act_deact_personnel_db(db, act_deact, name, fmw)
            personnel = retrive_one_record(db, name, fmw)
            return render_template('ps/admin_act_deact.html', act_deact=act_deact, personnel=personnel)
        flash(error)
    return render_template('ps/admin_act_deact.html', form=form)
