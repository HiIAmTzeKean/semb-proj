import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskapp import db

from .forms import loginform, strengthviewform
from .methods import authenticate_user
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = loginform()
    if form.validate_on_submit():
        error, user = authenticate_user(User, form.username.data, form.password.data)
        if error is None:
            session.clear()
            session['user_id'] = user.username
            session['fmw'] = user.fmw
            session['clearance'] = user.clearance
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html',form=form)

@bp.route('/load_fmw', methods=('GET', 'POST'))
def load_fmw():
    #form to select fmw
    form = strengthviewform()
    if form.validate_on_submit():
        fmw = form.fmw.data
        session.clear()
        session['fmw'] = fmw
        return redirect(url_for('index'))
    return render_template('ps/select_fmw.html',form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    clearance = session.get('clearance')
    if user_id is None:
        g.user = None
    else:
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE username = ?', (user_id,)
        # ).fetchone()
        # g.user = User.query.fliter_by(username=user_id).first() 
        # this return AttributeError: 'BaseQuery' object has no attribute 'fliter_by' WHY!!!!!
        g.user = db.session.query(User).filter_by(username=user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def fmw_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('fmw') is None:
            return redirect(url_for('auth.load_fmw'))
        return view(**kwargs)
    return wrapped_view


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
