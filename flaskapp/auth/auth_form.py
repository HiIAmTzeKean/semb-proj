from flask_wtf import FlaskForm
from wtforms import (HiddenField, PasswordField, SelectField, StringField,
                     SubmitField, BooleanField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Optional

from flaskapp import db

from flaskapp.helpers import fmd_type, statuses_type
from flaskapp.models import Fmw, Unit


class loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Sign in')

class loadfmwform(FlaskForm):
    fmds = [(coy.id, coy.name) for coy in db.session.query(Unit).filter(Unit.name!=0).all()]
    fmd = SelectField(label='FMD', choices=fmds, default=None)
    default_unit_display = Unit.query.filter_by(name=9).first()
    fmws = [(coy.id, coy.name) for coy in Fmw.query.filter_by(fmd_id = default_unit_display.id).all()]
    fmw = SelectField(label='FMW', choices=fmws, default=None)
    submit = SubmitField('Submit')


class strengthviewform(FlaskForm):
    fmds = [(coy.id, coy.name) for coy in Unit.query.all()]
    fmd = SelectField(label='FMD', choices=fmds, validators=[Optional()], default=None)
    default_unit_display = Unit.query.filter_by(name=0).first()
    fmws = [(coy.id, coy.name) for coy in Fmw.query.filter_by(fmd_id = default_unit_display.id).all()]
    fmw = SelectField(label='FMW', choices=fmws, validators=[Optional()], validate_choice=False, default=None)
    submit = SubmitField('Submit')
