from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')


class paradestateform(FlaskForm):
    statuses = {
        'P': 'PRESENT',
        'AO': 'ATTACHED OUT',
        'DUTY': 'DUTY',
        'OS': 'OUT STATION',
        'OC': 'ON COURSE',
        'OFF': 'OFF',
        'LL': 'LOCAL LEAVE',
        'OL': 'OVERSEAS LEAVE',
        'MC': 'MC',
        'MA': 'MA',
        'RSO': 'RSO',
        'RSI': 'RSI',
        'SOL': 'SOL',
        'DR': 'DUTY REST',
        'OTHERS': 'OTHERS'
    }
    statuses = statuses.items()
    workshops = [("Sembwang"),("Bedok"),("Navy"),("HQ")]
    fmw = SelectField(label='FMW', choices=workshops)
    name = SelectField(label='Name', choices='', coerce=int)
    status_date = DateField(label='Date', validators=[DataRequired()])
    am_status = SelectField(label='AM Status', choices=statuses)
    am_remarks = StringField(label='AM Remarks',)
    pm_status = SelectField(label='PM Status', choices=statuses)
    pm_remarks = StringField(label='PM Remarks',)
    submit = SubmitField('Submit')


class paradestateviewform(FlaskForm):
    date = DateField(label='Date', validators=[DataRequired()])
    submit = SubmitField('Submit')


class personnelseeker(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    rank = StringField(label='Rank', validators=[DataRequired()])
    workshops = [("Sembwang"),("Bedok"),("Navy"),("HQ")]
    fmw = SelectField(label='FMW', choices=workshops)
    add_del = SelectField(label='Add/Delete', choices=[('Add'),('Delete')])
    submit = SubmitField('Submit')