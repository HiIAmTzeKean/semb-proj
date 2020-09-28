import git
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flaskapp import db
from .models import User, Unit, Personnel
from .forms import paradestateform

bp = Blueprint('misc', __name__)

# successful upload page
@bp.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('misc/success.html')

@bp.route('/generate_testdata', methods=('GET', 'POST'))
def testdata():
    coys = Unit.query.all()
    # ("username", "password", "fmw","fmd","clearance","unit_id")
    for coy in coys:
        print("('{}','{}','{}',{},{},{}),".format(coy.fmw,coy.fmw,coy.fmw,coy.fmd,3,coy.id))
    return('hi')

# generate route for webhook
@bp.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/HiIAmTzeKean/semb-proj.git')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
