from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (HiddenField, PasswordField, SelectField, StringField,
                     SubmitField, BooleanField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Optional

from flaskapp import db

from .helpers import fmd_type, statuses_type
from .models import Fmw, Unit


class paradestateform(FlaskForm):
    statuses = statuses_type().items()
    name = SelectField(label='Name', choices='',validators=[DataRequired()], coerce=int)
    start_date = DateField(label='Start Date', validators=[DataRequired()], default=datetime.today)
    end_date = DateField(label='End Date', validators=[DataRequired()], default=datetime.today)
    am_status = SelectField(label='AM Status', choices=statuses)
    am_remarks = StringField(label='AM Remarks',)
    pm_status = SelectField(label='PM Status', choices=statuses)
    pm_remarks = StringField(label='PM Remarks',)
    submit = SubmitField('Submit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.end_date.data < self.start_date.data:
            self.end_date.errors.append('End Date must not come before Start Date!')
            return False
        return True


class strengthviewform(FlaskForm):
    fmds = [(coy.id, coy.name) for coy in Unit.query.all()]
    fmd = SelectField(label='FMD', choices=fmds, validators=[Optional()], default=None)
    default_unit_display = Unit.query.filter_by(name=0).first()
    fmws = [(coy.id, coy.name) for coy in Fmw.query.filter_by(fmd_id = default_unit_display.id).all()]
    fmw = SelectField(label='FMW', choices=fmws, validators=[Optional()], validate_choice=False, default=None)
    submit = SubmitField('Submit')


class admin_paradestateviewform(strengthviewform):
    date = DateField(label='Date', validators=[DataRequired()], default=datetime.today)


################################ Pending del after init of del methods
class submitform(FlaskForm):
    submit = SubmitField('Submit')


class admin_adddelform(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    rank = StringField(label='Rank', validators=[DataRequired()])
    submit = SubmitField('Submit')
    fmw = SelectField(label='FMW', choices=[], validators=[Optional()], validate_choice=False, default=None)


class admin_actdeactform(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    rank = StringField(label='Rank', validators=[DataRequired()])
    act_deact = SelectField(label='Activate/Deactivate',validators=[InputRequired()],
                            choices=[('True','Activate'),('False','Deactivate')], coerce=lambda x: x == 'True')
    submit = SubmitField('Submit')
    fmd = SelectField(label='FMD', choices=fmd_type())
    fmw = SelectField(label='FMW', choices='')
##################################


class admin_generateexcelform(FlaskForm):
    start_date = DateField(label='Start Date', validators=[DataRequired()], default=datetime.today)
    end_date = DateField(label='End Date', validators=[DataRequired()], default=datetime.today)
    submit = SubmitField('Submit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.end_date.data < self.start_date.data:
            self.end_date.errors.append('End Date must not come before Start Date!')
            return False
        return True
