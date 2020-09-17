import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskapp.db import get_db

from .forms import loginform

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = loginform()
    if form.validate_on_submit():
        error = None
        username = form.username.data
        password = form.password.data
    # validating user (Still need to add in password auth)
        db = get_db()
        user = db.execute(
             'SELECT * FROM user WHERE username = ?', (username,)
         ).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif user['password'] != password:
            error = 'Wrong password'
    # Log user in and redirect to index page
        if error is None:
            session.clear()
            session['user_id'] = user['username']
            session['fmw'] = user['fmw']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login2.html',form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

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
