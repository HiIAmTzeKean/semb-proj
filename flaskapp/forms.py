from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, HiddenField
from wtforms.validators import DataRequired

# log admin into system
class loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')


# submit parade state
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

    statuses = list(map(lambda x: (x.key, x.value), statuses))
    workshops = [("Sembwang"),("Bedok"),("Navy"),("HQ")]
    fmw = SelectField(label='FMW', choices=workshops)
    name = SelectField(label='Name', choices='', coerce=int)
    status_date = HiddenField(label='Date')
    am_status = SelectField(label='AM Status', choices=status)
    am_remarks = StringField(label='AM Remarks',)
    pm_status = SelectField(label='PM Status', choices=status)
    pm_remarks = StringField(label='PM Remarks',)
    submit = SubmitField('Submit')

# Admin updater to change parade state
class update_paradestateform(paradestateform):
    pass