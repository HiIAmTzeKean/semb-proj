from datetime import datetime, timedelta

from flask import (Blueprint, flash, g, make_response, redirect,
                   render_template, request, session, url_for)

from flaskapp import db
from flaskapp.auth import fmw_required, login_required

from .db_methods import (act_deact_personnel_db, add_del_personnel_db,
                         check_personnel_exist, retrive_one_record,
                         retrive_personnel_id, retrive_record_by_date,
                         submit_PS)
from .forms import (admin_actdeactform, admin_adddelform,
                    admin_generateexcelform, admin_paradestateviewform,
                    paradestateform, paradestateviewform, strengthviewform)
from .methods import (generate_PS, nameconverter_paradestateform,
                      retrieve_personnel_list, retrieve_personnel_statuses)
from .models import Personnel, Personnel_status, User
from .helpers import workshop_type

bp = Blueprint('ps', __name__)


@bp.route('/', methods=('GET', 'POST'))
@fmw_required
def index():
    '''
    Uploading of parade state to DB
    Clearance 1: Nil
    Clearance 3: Nil
    '''
    fmw = session.get('fmw')
    rows = retrieve_personnel_list(fmw,clearance=100)
    names = nameconverter_paradestateform(rows)
    form = paradestateform()
    form.name.choices = names
    updated = False
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
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
        record = Personnel_status.query.filter(Personnel_status.personnel_id==personnel_id,Personnel_status.date==start_date).first()
        print(record)
        resp = make_response(render_template('ps/index.html', form=form, updated=updated,
                            multi_date=multi_date, personnel=record, end_date=end_date))
        resp.set_cookie('personnel_id', value = str(personnel_id), max_age=60*60*24)
        return resp
    record = Personnel_status.query.filter(Personnel_status.personnel_id==request.cookies.get('personnel_id'),Personnel_status.date==datetime.date(datetime.today())).first()
    if record:
        form.name.data = record.id
        form.am_status.data = record.am_status
        form.am_remarks.data = record.am_remarks
        form.pm_status.data = record.pm_status
        form.pm_remarks.data = record.pm_remarks
    return render_template('ps/index.html', form=form, updated=updated, personnel=None)


@bp.route('/paradestate', methods=('GET', 'POST'))
@login_required
def paradestate():
    '''
    View paradestate with date input
    Clearance 1: Select FMW and FMD to view
    Clearance 3: View current FMW
    '''
    if session.get('clearance') <= 2: form = admin_paradestateviewform()
    else: form = paradestateviewform()
    if form.validate_on_submit():
        if session.get('clearance') <= 2: fmw = form.fmw.data
        else: fmw = session.get('fmw')
        date = form.date.data
        personnels_status, missing_status = retrieve_personnel_statuses(db, fmw, date,session.get('clearance'))
        print(missing_status)
        if len(personnels_status) != 0:
            ## To retrive data from personnel table, use query.Person.whateverdatayouneed
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
    if session.get('clearance') <= 2:
        form = strengthviewform()
        if form.validate_on_submit():
            fmw = form.fmw.data
            personnels = retrieve_personnel_list(fmw)
            if personnels != []:
                return render_template('ps/strengthviewer.html', fmw=fmw, personnels=personnels)
            flash('No personnel in selected FMW yet.')
        return render_template('ps/select_fmw.html', form=form)
    else:
        fmw = session.get('fmw')
        personnels = retrieve_personnel_list(fmw)
        return render_template('ps/strengthviewer.html', fmw=fmw, personnels=personnels)
    

@bp.route('/admin/add_del_personnel', methods=('GET', 'POST'))
@login_required
def admin_add_del():
    form = admin_adddelform()
    if form.validate_on_submit():
        name = form.name.data
        rank = form.rank.data
        if session.get('clearance') <= 2: fmw = form.fmw.data
        else: fmw = session.get('fmw')
        add_del = form.add_del.data
        error, personnel = add_del_personnel_db(db, add_del, rank, name, fmw)
        if error == None:
            return render_template('ps/admin_add_del.html', add_del=add_del, personnel=personnel)
        flash(error)
    flash(form.errors)
    return render_template('ps/admin_add_del.html', form=form)


@bp.route('/admin/act_deact', methods=('GET', 'POST'))
@login_required
def admin_act_deact():
    form = admin_actdeactform()
    fmd = session.get('fmd')
    form.fmw.choices = workshop_type(fmd)
    if form.validate_on_submit():
        name = form.name.data
        rank = form.rank.data
        if session.get('clearance') <= 2: fmw = form.fmw.data
        else: fmw = session.get('fmw')
        act_deact = form.act_deact.data
        error = check_personnel_exist(db, name, fmw, rank)
        if error == None:
            act_deact_personnel_db(db, act_deact, rank, name, fmw, fmd)
            personnel = retrive_one_record(db, name, fmw)
            return render_template('ps/admin_act_deact.html', act_deact=act_deact, personnel=personnel)
        flash(error)
    flash(form.errors)
    return render_template('ps/admin_act_deact.html', form=form)

@bp.route('/admin/generate_excel', methods=('GET', 'POST'))
@login_required
def admin_generate_excel():
    form = admin_generateexcelform()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        if end_date<start_date:
            flash("Your end date is earlier than your start date")
            return render_template('ps/admin_generate_excel.html', form=form)
        if start_date == end_date:
            records = retrieve_personnel_statuses(db,'Admin',start_date,missing_status_needed=False)
            error = generate_PS(records)
            if error:
                flash("Error in compiling data to excel file. Contact admin!")
        else:
            while start_date != (end_date + timedelta(days=1)):
                records = retrieve_personnel_statuses(db,'Admin',start_date,missing_status_needed=False)
                error = generate_PS(records,start_date)
                if error:
                    flash("Error in compiling multiple dates to excel file. Contact admin!")
                start_date = start_date + timedelta(days=1)
        if error == None:
            flash('Success! Data is now stored in archives')
            return redirect(url_for('ps.admin_add_del'))
    return render_template('ps/admin_generate_excel.html', form=form)
