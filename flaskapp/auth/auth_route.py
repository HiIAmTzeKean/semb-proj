import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, jsonify)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskapp import db, login_manager
from flask_login import current_user, login_user, logout_user, login_required
from datetime import timedelta
from .auth_form import loginform, strengthviewform, loadfmwform
from flaskapp.models import User, Unit, Fmw

bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(id):
    g.user = current_user
    return User.query.get(int(id))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password==form.password.data:
            session.clear()
            login_user(user, remember=True, duration=timedelta(minutes=10))
            session['fmw_id'] = user.fmw_id
            session['clearance'] = user.clearance
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Incorrect Username and Password')
    return render_template('auth/login.html',form=form)


@bp.route('/load_fmw', methods=('GET', 'POST'))
def load_fmw():
    form = loadfmwform()
    if request.method == "POST":
        fmd_id = form.fmd.data
        fmw_id = form.fmw.data
        session['fmw_id']=fmw_id
        return redirect(url_for('index'))
    return render_template('ps/select_fmw.html',form=form)


@bp.route('/fmw/<fmd_id>', methods=('GET', 'POST'))
def fmw(fmd_id):
    subquery = Unit.query.filter_by(id=fmd_id).first()
    fmws = Fmw.query.filter_by(fmd_id = subquery.id).all()
    fmw_array = []
    for fmw in fmws:
        fmwObj ={}
        fmwObj['id']=fmw.id
        fmwObj['fmw']=fmw.name
        fmw_array.append(fmwObj)
    return jsonify({'fmws': fmw_array})


@bp.before_app_request
def load_logged_in_user():
    g.user = current_user


@bp.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('Logged out!')
    return redirect(url_for('index'))


def fmw_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('fmw_id') is None:
            return redirect(url_for('auth.load_fmw'))
        return view(**kwargs)
    return wrapped_view
