from datetime import datetime, timedelta

from flask import (Blueprint, flash, g, make_response, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_required

from flaskapp import db

from flaskapp.auth.auth_route import fmw_required
from .db_methods import (act_deact_personnel_db, add_del_personnel_db,
                         check_personnel_exist,
                         retrive_record_by_date,
                         submit_PS_helper)
from .forms import (admin_adddelform, submitform,
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
        date = request.args.get('date')
        fmw_id= request.args.get('fmw_id')
        form.name.choices = [db.session.query(Personnel.id,Personnel.name).filter_by(id=personnel_id).first()]

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
            form.name.data = personnel_id
        return render_template('ps/index.html', form=form, updated=updated, personnel=None,
                               date=date, redirect_to_paradestate=True, fmw_id=fmw_id)

    if request.method =="POST":
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
            return redirect(url_for('ps.paradestate', redirect_to_paradestate=True ,fmw_id=request.args.get('fmw_id'), date=request.args.get('date')))
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


@bp.route('/paradestate_pre_view', methods=('GET', 'POST'))
@login_required
def paradestate_pre_view():
    """Pre-view for user to redirect after checking clearance 

    Args:
        
    Redirect:
        url_for(paradestate)
        date ([str]): [%Y-%m-%d]
        fmw_id: [current_user.fmw_id]
    """
    clearance = current_user.clearance
    form = admin_paradestateviewform()

    if form.validate_on_submit():
        date=form.date.data
        if clearance == 4:
            return redirect(url_for('ps.paradestate',date=date,fmw_id=current_user.fmw_id))
        # for clearance 3 and below 
        fmw_id = form.fmw.data
        return redirect(url_for('ps.paradestate',date=date,fmw_id=fmw_id))
    
    if clearance == 3:
        form.fmd.choices = [(coy.id, coy.name) for coy in Unit.query.filter_by(id=current_user.fmw.fmd_id).all()]
        form.fmw.choices = [(coy.id, coy.name) for coy in Fmw.query.filter_by(fmd_id = current_user.fmw.fmd_id).all()]
    elif clearance == 2:
        # HQ9 view (HQ9 and all in 9AMB)
        form.fmd.choices = [(coy.id, coy.name) for coy in Unit.query.filter(name!=0).all()]
        form.fmw.choices = [(coy.id, coy.name) for coy in Fmw.query.filter_by(fmd_id = current_user.fmw.fmd_id).all()]
    elif clearance == 1:
        pass
    return render_template('ps/paradestate_pre_view.html',form=form)


@bp.route('/paradestate/<date>/<fmw_id>', methods=('GET', 'POST'))
@login_required
def paradestate(date,fmw_id):
    """View paradestate with date input
       Clearance 1: Select FMW and FMD to view
       Clearance 3: View current FMW
    
    Args:
        date ([str]): [%Y-%m-%d]
        fmw_id: [requested fmw user wants to view]

    Methods:
        Set Present: [Button in html. Set present for selected time. Redirects user back
        to same view again]
        Other Status: [Button in html. Set other status for Person. 
        Redirects user to Index page then back to paradestate page again]
    """
    if request.args.get('redirect_to_paradestate'):
        personnels_status, missing_status = retrieve_personnel_statuses(db, fmw_id, date, clearance=current_user.clearance)
        if len(personnels_status) != 0:
            return render_template('ps/paradestate.html', personnels=personnels_status,
                                   missing_personnels=missing_status, date=date,
                                   fmw_name=db.session.query(Fmw.name).filter_by(id=fmw_id).scalar())
        flash("No one has submitted PS. Please remind them to do so!")
        return redirect(url_for('ps.paradestate_pre_view'))

    personnels_status, missing_status = retrieve_personnel_statuses(db, fmw_id, date, clearance=current_user.clearance)
    if len(personnels_status) != 0:
        return render_template('ps/paradestate.html', personnels=personnels_status,
                                missing_personnels=missing_status, date=date,
                                fmw_name=db.session.query(Fmw.name).filter_by(id=fmw_id).scalar())
    flash("No one has submitted PS. Please remind them to do so!")
    return redirect(url_for('ps.paradestate_pre_view'))


@bp.route('/statuschange/<personnel_id>/<date>', methods=('GET', 'POST'))
@login_required
def statuschange(personnel_id,date):
    """Route to change paradestate for personnel
    Methods:
        set_present: [Set status to present for time arg provided]
        redirect index: [Redirect for setting of status (Setting of other status or status was not set
        in the first place)]
    Args:
        personnel_id
        date ([str]): [%Y-%m-%d]
        fmw_id: [fmw_id belonging to personnel]
        set_present ([Boolean])
        time ([str]): [AM/PM]

    Redirects:
        personnel_id ([type]): [description]
        date ([str]): [%Y-%m-%d]
        fmw_id: [fmw_id belonging to personnel]
    """
    record = Personnel_status.query.filter_by(personnel_id=personnel_id,date=date).first()
    fmw_id = request.args.get('fmw_id')

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
        return redirect(url_for('index', status_change=False,personnel_id=personnel_id,date=date, fmw_id=fmw_id))
    elif record:
        return redirect(url_for('index', status_change=True,personnel_id=personnel_id,date=date, fmw_id=fmw_id))


@bp.route('/strengthviewer_pre_view', methods=('GET', 'POST'))
@login_required
def strengthviewer_pre_view():
    """Pre-view for user to redirect after checking clearance 

    Args:
        
    Redirect:
        url_for(strengthviewer)
        fmw_id: [current_user.fmw_id]
    """
    clearance = current_user.clearance
    if clearance == 4:
            return redirect(url_for('ps.strengthviewer',fmw_id=current_user.fmw_id))
    
    form = strengthviewform()
    if form.validate_on_submit():
        fmw_id = form.fmw.data
        return redirect(url_for('ps.strengthviewer',fmw_id=fmw_id))
    if clearance == 3:
        form.fmd.choices = [(coy.id, coy.name) for coy in Unit.query.filter_by(id=current_user.fmw.fmd_id).all()]
        form.fmw.choices = [(coy.id, coy.name) for coy in Fmw.query.filter_by(fmd_id = current_user.fmw.fmd_id).all()]
    elif clearance == 2:
        # HQ9 view (HQ9 and all in 9AMB)
        form.fmd.choices = [(coy.id, coy.name) for coy in Unit.query.filter(name!=0).all()]
        form.fmw.choices = [(coy.id, coy.name) for coy in Fmw.query.filter_by(fmd_id = current_user.fmw.fmd_id).all()]
    elif clearance == 1:
        pass
    return render_template('ps/select_fmw_strengthviewer.html',form=form)

@bp.route('/strengthviewer/<fmw_id>', methods=('GET', 'POST'))
@login_required
def strengthviewer(fmw_id):
    """Display current strength in FMW
       Clearance 1: Select FMW and FMD to view
       Clearance 3: View current FMW

    Methods:
        Add: [redirect user to add_del route on form submission]
        Del: [redirect user to add_del route. Button is in html form]
        Deactivate (not done)
        Activate (not done)
    """
    add_form = admin_adddelform()
    if add_form.validate_on_submit():
        fmw_id = current_user.fmw.id
        return redirect(url_for('ps.add_del', personnel_name=add_form.name.data,
                                fmw_id=fmw_id, rank=add_form.rank.data, add_del='add'))

    if request.args.get('redirect_to_strenghtviewer') and request.args.get('cancel_request'):
        flash('Cancelled!')
    elif request.args.get('redirect_to_strenghtviewer'): 
        flash('Success!')
    
    fmw_name = db.session.query(Fmw.name).filter_by(id=fmw_id).scalar()
    personnels = retrieve_personnel_list(fmw_id,current_user.clearance)
    if personnels != []:
        return render_template('ps/strengthviewer.html', personnels=personnels,add_form=add_form, fmw_name=fmw_name)
    flash('No personnel in selected FMW yet.')
    return redirect(url_for('ps.strengthviewer_pre_view'))


@bp.route('/add_del_personnel/<rank>/<personnel_name>/<fmw_id>/<add_del>', methods=('GET', 'POST'))
@login_required
def add_del(rank,personnel_name,fmw_id,add_del):
    """Add/Del personnel from DB

    Args:
        rank
        personnel_name
        fmw_id
        add_del
        personnel_id

    Returns:
        redirect_to_strenghtviewer ([Boolean])
        cancel_request ([Boolean]): [If user wants to cancel request, cancel button is in html page]
    """
    form = submitform()
    if add_del == 'del' and form.validate_on_submit():
        status_records = Personnel_status.query.filter(Personnel_status.personnel_id==request.args.get('personnel_id')).all()
        record = Personnel.query.filter_by(id=request.args.get('personnel_id')).first()
        for status in status_records:
            db.session.delete(status)
        db.session.commit()
        db.session.delete(record)
        db.session.commit()
        return redirect(url_for('ps.strengthviewer', redirect_to_strenghtviewer=True,fmw_id=fmw_id))
    elif add_del == 'add' and form.validate_on_submit():
        db.session.add(Personnel(rank,personnel_name,fmw_id))
        db.session.commit()
        return redirect(url_for('ps.strengthviewer', redirect_to_strenghtviewer=True,fmw_id=fmw_id))
    return render_template('ps/admin_add_del.html',form=form,rank=rank,personnel_name=personnel_name,fmw_id=fmw_id)


@bp.route('/act_deact/<rank>/<personnel_name>/<fmw_id>/<act_deact>', methods=('GET', 'POST'))
@login_required
def act_deact(rank,personnel_name,fmw_id,add_del):
    """Add/Del personnel from DB

    Args:
        rank
        personnel_name
        fmw_id
        add_del
        personnel_id

    Returns:
        redirect_to_strenghtviewer ([Boolean])
        cancel_request ([Boolean]): [If user wants to cancel request, cancel button is in html page]
    """
    form = submitform()
    if add_del == 'deact' and form.validate_on_submit():
        pass
        return redirect(url_for('ps.strengthviewer', redirect_to_strenghtviewer=True))
    elif add_del == 'act' and form.validate_on_submit():
        pass
    return render_template('ps/admin_add_del.html',form=form,rank=rank,personnel_name=personnel_name,fmw_id=fmw_id)

# @bp.route('/admin/act_deact', methods=('GET', 'POST'))
# @login_required
# def admin_act_deact():
#     form = admin_actdeactform()
#     fmd = session.get('fmd')
#     form.fmw.choices = workshop_type(fmd)
#     if form.validate_on_submit():
#         name = form.name.data
#         rank = form.rank.data
#         if session.get('clearance') <= 2: fmw = form.fmw.data
#         else: fmw = session.get('fmw')
#         act_deact = form.act_deact.data
#         error = check_personnel_exist(db, name, fmw_id, rank)
#         if error == None:
#             act_deact_personnel_db(db, act_deact, rank, name, fmw, fmd)
#             personnel = retrive_one_record(db, name, fmw_id)
#             return render_template('ps/admin_act_deact.html', act_deact=act_deact, personnel=personnel)
#         flash(error)
#     flash(form.errors)
#     return render_template('ps/admin_act_deact.html', form=form)

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