from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskapp.auth import login_required

from flaskapp.db import get_db

bp = Blueprint('ps', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('ps/index.html')

# view only to admin
@bp.route('/admin')
@login_required
def admin():
    if g.user['username'] == 'Admin':
#displays admin functions
        return 'admin'

# show error 401 and forces user to login again
    return 'redirect'

# view to cos (admin is also able to view)
@bp.route('/cos')
@login_required
def cos():
    return 'cos'