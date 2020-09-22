from flask import (Blueprint, flash, g, redirect, render_template, session, url_for)
from datetime import datetime
from flaskapp.auth import login_required, clearance_one_required
from flaskapp.db import get_db
from .forms import (paradestateform, paradestateviewform, admin_add_del_form,
admin_strength_viewer,admin_three_add_del_form,admin_three_act_deact_form)
from .methods import nameconverter_paradestateform, retrieve_personnel_list, retrieve_personnel_statuses
from .db_methods import (update_PS, insert_PS, retrive_record_by_date,
del_personnel_db, add_personnel_db, retrive_one_record, act_deact_personnel_db,retrive_personnel_id)

bp = Blueprint('ps', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    """
    Open page to allow all to submit their parade state
    No admin access is required. Once submitted, confirmation page will be given
    """
    db = get_db()
    # Trial for Sembawang only
    # form should display only fmw attributes once clicked on
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
        if retrive_record_by_date(db,personnel_id,status_date): 
            update_PS(db,personnel_id, status_date, am_status, am_remarks, pm_status,pm_remarks)
            updated = True
        else: 
            insert_PS(db,personnel_id, status_date, am_status, am_remarks, pm_status,pm_remarks)
        record = retrive_record_by_date(db,personnel_id,status_date)
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
        date = form.date.data
        personnels_status, missing_status = retrieve_personnel_statuses(db,fmw,date)
        if len(personnels_status) != 0:
            return render_template('ps/paradestate.html', personnels=personnels_status,
            missing_personnels=missing_status)
        flash("No one has submitted PS. Please remind them to do so!")  
    return render_template('ps/paradestate.html', form=form)


@bp.route('/strengthviewer', methods=('GET', 'POST'))
@login_required
def strengthviewer():
    # if admin rights, have a choice of the form to select
    # else auto display current fmw
    db = get_db()
    fmw = session.get('fmw')
    form = admin_strength_viewer()
    if form.validate_on_submit():
        fmw = form.fmw.data
        personnels = retrieve_personnel_list(db, fmw)
        return render_template('ps/strengthviewer.html', personnels=personnels)
    return render_template('ps/strengthviewer.html',form=form)


@bp.route('/admin', methods=('GET', 'POST'))
@login_required
def admin():
    if session.get('clearance')==3:
        # redirect to fmw page according to clearance level
        return redirect(url_for("ps.admin_three"))
    db = get_db()
    form = admin_add_del_form()
    if form.validate_on_submit():
        name =  form.name.data
        rank =  form.rank.data
        fmw =  form.fmw.data
        add_del = form.add_del.data
        if add_del == 'Add':
            error = add_personnel_db(db,name,fmw,rank)
            personnel = retrive_one_record(db,name,fmw)
        else:
            personnel = retrive_one_record(db,name,fmw)
            if personnel != None: error = del_personnel_db(db,name,fmw)
            else: error = "Personnel does not exist in the table, please check"
        if error == None:
            return render_template('ps/admin.html', add_del=add_del,personnel=personnel)
        flash(error)
    return render_template('ps/admin.html',form=form)


@bp.route('/admin_three', methods=('GET', 'POST'))
@login_required
def admin_three():
    db = get_db()
    form = admin_three_add_del_form()
    if form.validate_on_submit():
        name =  form.name.data
        rank =  form.rank.data
        fmw = session.get('fmw')
        add_del = form.add_del.data
        if add_del == 'Add':
            error = add_personnel_db(db,name,fmw,rank)
            personnel = retrive_one_record(db,name,fmw)
        else:
            personnel = retrive_one_record(db,name,fmw)
            if personnel != None: error = del_personnel_db(db,name,fmw)
            else: error = "Personnel does not exist in the table, please check"
        if error == None:
            return render_template('ps/admin.html', add_del=add_del,personnel=personnel)
        flash(error)
    return render_template('ps/admin.html',form=form)


@bp.route('/admin_three/act_deact', methods=('GET', 'POST'))
@login_required
def admin_three_act_deact():
    db = get_db()
    form = admin_three_act_deact_form()
    if form.validate_on_submit():
        name =  form.name.data
        rank =  form.rank.data
        fmw = session.get('fmw')
        act_deact = form.act_deact.data
        error = retrive_personnel_id(db,name,fmw,rank=rank)
        if error != None:
            act_deact_personnel_db(db,act_deact,name,fmw)
            personnel = retrive_one_record(db,name,fmw)
            return render_template('ps/admin_act_deact.html', act_deact=act_deact,personnel=personnel)
        flash('User does not exist in your FMW')
    return render_template('ps/admin_act_deact.html',form=form)