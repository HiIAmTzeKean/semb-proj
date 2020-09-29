from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (HiddenField, PasswordField, SelectField, StringField,
                     SubmitField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired

from .helpers import fmd_type, statuses_type
from .models import Unit


class loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Sign in')


class paradestateform(FlaskForm):
    statuses = statuses_type().items()
    # workshops = [("Sembawang"),("Bedok"),("Navy"),("Selarang"),("HQ")]
    # fmw = SelectField(label='FMW', choices=workshops)
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


class paradestateviewform(FlaskForm):
    date = DateField(label='Date', validators=[DataRequired()], default=datetime.today)
    submit = SubmitField('Submit')


class admin_paradestateviewform(paradestateviewform):
    # workshops = [("Sembawang"),("Bedok"),("Navy"),("Selarang"),("HQ")]
    fmd = SelectField(label='FMD', choices=[(9),(92),(93)],default=0)
    fmw = SelectField(label='FMW', choices=[])


class strengthviewform(FlaskForm):
    fmw = SelectField(label='FMW', choices=[], id='fmw')
    fmd = SelectField(label='FMD', choices=[(9),(92),(93)], id='fmd')
    submit = SubmitField('Submit')


class admin_adddelform(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    rank = StringField(label='Rank', validators=[DataRequired()])
    add_del = SelectField(label='Add/Delete', choices=[('Add'),('Delete')])
    submit = SubmitField('Submit')
    #for clearance 2 and above
    workshops = [("Sembawang"),("Bedok"),("Navy"),("Selarang"),("HQ")]
    fmw = SelectField(label='FMW', choices=workshops)


class admin_actdeactform(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    rank = StringField(label='Rank', validators=[DataRequired()])
    act_deact = SelectField(label='Activate/Deactivate',validators=[InputRequired()],
                            choices=[('True','Activate'),('False','Deactivate')], coerce=lambda x: x == 'True')
    submit = SubmitField('Submit')
    fmd = SelectField(label='FMD', choices=fmd_type())
    fmw = SelectField(label='FMW', choices='')


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
