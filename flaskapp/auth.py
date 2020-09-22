import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskapp.db import get_db

from .forms import loginform

from .methods import authenticate_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = loginform()
    if form.validate_on_submit():
        error, user = authenticate_user(get_db(), form.username.data, form.password.data)
        if error is None:
            session.clear()
            session['user_id'] = user['username']
            session['fmw'] = user['fmw']
            session['clearance'] = user['clearance']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html',form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    clearance = session.get('clearance')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def clearance_one_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user["clearance"] != 1:
            flash("You do not have rights to this page")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def clearance_two_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user["clearance"] < '2':
            flash("You do not have rights to this page")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
