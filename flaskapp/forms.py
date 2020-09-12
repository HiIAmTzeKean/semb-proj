from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired

# log admin into system
class loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

# submit parade state
class paradestateform(FlaskForm):
    status = [("P","Present"),("OS","Out Station"),("MC","Medical Cert")]
    name = SelectField(label='Name', choices='')
    am_status = SelectField(label='AM Status', choices=status)
    am_remarks = StringField(label='AM Remarks',)
    pm_status = SelectField(label='PM Status', choices=status)
    pm_remarks = StringField(label='PM Remarks',)
    submit = SubmitField('Submit')

# Admin updater to change parade state
# class update_paradestateform(paradestateform):
#     pass