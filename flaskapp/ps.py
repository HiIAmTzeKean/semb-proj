from datetime import datetime, timedelta

from flask import (Blueprint, flash, g, make_response, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_required

from flaskapp import db

from .auth import fmw_required
from .db_methods import (act_deact_personnel_db, add_del_personnel_db,
                         check_personnel_exist, retrive_one_record,
                         retrive_record_by_date,
                         submit_PS_helper)
from .forms import (admin_actdeactform, admin_adddelform,
                    admin_generateexcelform, admin_paradestateviewform,
                    paradestateform, strengthviewform)
from .helpers import workshop_type
from .methods import (generate_PS, retrieve_personnel_list,
                      retrieve_personnel_statuses)
from .models import Personnel, Personnel_status, User, Unit, Fmw

bp = Blueprint('ps', __name__)


@bp.route('/', methods=('GET', 'POST'))
@fmw_required
def index():
    """[summary]

    Returns:
        [type]: [description]
    """
    fmw_id = session.get('fmw_id')
    if session.get('clearance') is None: clearance = 100
    else: clearance = current_user.clearance
    form = paradestateform()
    form.name.choices = [(pers.id,pers.name) for pers in retrieve_personnel_list(fmw_id,clearance)]
    updated = False

    if request.args.get('status_change') is not None:
        personnel_id = int(request.args.get('personnel_id'))
        print(personnel_id)
        date = request.args.get('date')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        fmw_id= request.args.get('fmw_id')
        if request.args.get('status_change') == True:
            record = retrive_record_by_date(personnel_id, date)
            form.start_date.data = record.date
            form.end_date.data = record.date
            form.name.data = record.personnel_id
            form.am_status.data = record.am_status
            form.am_remarks.data = record.am_remarks
            form.pm_status.data = record.pm_status
            form.pm_remarks.data = record.pm_remarks
        else:
            print('setting id for you')
            form.name.data = personnel_id
        return render_template('ps/index.html', form=form, updated=updated, personnel=None,
                               date=date, redirect_to_paradestate=True, fmw_id=fmw_id)

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        personnel_id = form.name.data
        am_status = form.am_status.data
        am_remarks = form.am_remarks.data
        pm_status = form.pm_status.data
        pm_remarks = form.pm_remarks.data

        multi_date = submit_PS_helper(db,personnel_id, start_date, end_date, am_status, am_remarks, pm_status, pm_remarks)
        updated = True
        record = Personnel_status.query.filter(Personnel_status.personnel_id==personnel_id,Personnel_status.date==start_date).first()

        if request.args.get('redirect_to_paradestate'):
            return redirect(url_for('ps.paradestate', redirect_to_paradestate=True ,fmw_id=fmw_id, date=request.args.get('date')))
        else:
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
    form = admin_paradestateviewform()
    if request.args.get('redirect_to_paradestate'):
        fmw_id = request.args.get('fmw_id')
        date = request.args.get('date')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        personnels_status, missing_status = retrieve_personnel_statuses(db, fmw_id, date, clearance=current_user.clearance)
        if len(personnels_status) != 0:
            return render_template('ps/paradestate.html', personnels=personnels_status,
                                   missing_personnels=missing_status, date=date,
                                   fmw_name=db.session.query(Fmw.name).filter_by(id=fmw_id).scalar())
        flash("No one has submitted PS. Please remind them to do so!")

    elif form.validate_on_submit():
        if current_user.clearance <= 1: fmw_id = form.fmw.data
        else: fmw_id = current_user.fmw.id
        date = form.date.data
        personnels_status, missing_status = retrieve_personnel_statuses(db, fmw_id, date, clearance=current_user.clearance)
        if len(personnels_status) != 0:
            return render_template('ps/paradestate.html', personnels=personnels_status,
                                   missing_personnels=missing_status, date=date,
                                   fmw_name=db.session.query(Fmw.name).filter_by(id=fmw_id).scalar())
        flash("No one has submitted PS. Please remind them to do so!")

    return render_template('ps/paradestate.html', form=form)

@bp.route('/statuschange/<personnel_id>/<date>', methods=('GET', 'POST'))
@login_required
def statuschange(personnel_id,date):
    """Route to change paradestate for personnel

    Args:
        personnel_id
        date ([str]): [%Y-%m-%d]
        fmw_id: [fmw_id belonging to personnel]
        set_present: [Boolean]
        time ([str]): [AM/PM]

    Redirects:
        personnel_id ([type]): [description]
        date ([str]): [%Y-%m-%d]
        fmw_id: [fmw_id belonging to personnel]
    """
    record = Personnel_status.query.filter_by(personnel_id=personnel_id,date=date).first()
    fmw_id = request.args.get('fmw_id')
    date = datetime.strptime(date, '%Y-%m-%d').date()

    if 'set_present' in request.args:
        if request.args.get('time') == "AM":
            record = Personnel_status(date, 'P', '', None, '', personnel_id)
        else:
            record = Personnel_status(date, None, '', 'P', '', personnel_id)
        db.session.add(record)
        db.session.commit()
        flash('Updated Personnel selected!')
        return redirect(url_for('ps.paradestate', redirect_to_paradestate=True, fmw_id=fmw_id, date=date))

    elif record is None:
        return redirect(url_for('index', status_change=False,redirect_to_paradestate=True,personnel_id=personnel_id,date=date))

    elif record:
        return redirect(url_for('index', status_change=True,redirect_to_paradestate=True,personnel_id=personnel_id,date=date))


@bp.route('/strengthviewer', methods=('GET', 'POST'))
@login_required
def strengthviewer():
    '''
    Display current strength in FMW
    Clearance 1: Select FMW and FMD to view
    Clearance 3: View current FMW
    '''
    if current_user.clearance <= 2:
        form = strengthviewform()
        if form.validate_on_submit():
            fmw_id = form.fmw.data
            personnels = retrieve_personnel_list(fmw_id,current_user.clearance)
            if personnels != []:
                return render_template('ps/strengthviewer.html', fmw=fmw_id, personnels=personnels)
            flash('No personnel in selected FMW yet.')
        return render_template('ps/select_fmw_strengthviewer.html', form=form)
    else:
        fmw_id = current_user.fmw.id
        personnels = retrieve_personnel_list(current_user.clearance)
        return render_template('ps/strengthviewer.html', fmw=fmw_id, personnels=personnels)
    

@bp.route('/admin/add_del_personnel', methods=('GET', 'POST'))
@login_required
def admin_add_del():
    form = admin_adddelform()
    if form.validate_on_submit():
        name = form.name.data
        rank = form.rank.data
        if session.get('clearance') <= 2: fmw_id = form.fmw.data
        else: fmw_id = session.get('fmw_id')
        add_del = form.add_del.data
        error, personnel = add_del_personnel_db(db, add_del, rank, name, fmw_id)
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
        error = check_personnel_exist(db, name, fmw_id, rank)
        if error == None:
            act_deact_personnel_db(db, act_deact, rank, name, fmw, fmd)
            personnel = retrive_one_record(db, name, fmw_id)
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
