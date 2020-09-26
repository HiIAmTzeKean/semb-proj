from flaskapp import db
from datetime import datetime
from sqlalchemy.orm import validates


class User(db.Model):
    __tablename = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False,)
    password = db.Column(db.Text, nullable=False)
    fmw = db.Column(db.Text, nullable=False)
    fmd = db.Column(db.Integer, nullable=False)
    clearance = db.Column(db.Integer, nullable=False)

    @validates('clearance')
    def validate_clearance(self, key, clearance):
        if clearance!=1 or clearance!=2 or clearance!=3:
            raise AssertionError('Clearance should be an int value form 1 to 3') 
        return clearance @validates('clearance')

    @validates('fmd') 
    def validate_fmd(self, key, fmd):
        if fmd!=1 or fmd!=2:
            raise AssertionError('FMD should be 93 or 92') 
        return fmd @validates('fmd') 

    def __init__(self, username=''):
        self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Personnel(db.Model):
    __tablename = "personnel"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    fmw = db.Column(db.Text, nullable=False)
    fmd = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, nullable = False, default='True')
    status = db.relationship('Personnel_status',backref=db.backref('PersonnelID', lazy=False))

    # def __init__(self):
    #     self.name = name
    #     self.fmw = fmw
    #     self.fmd = fmd
    #     self.rank = rank
    #     self.active = active

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Personnel_status(db.Model):
    __tablename = "personnel_status"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    am_status = db.Column(db.Text)
    am_remarks = db.Column(db.Text, nullable=False)
    pm_status = db.Column(db.Text, nullable=False)
    pm_remarks = db.Column(db.Text)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    

    # def __init__(self,**kwargs):
    #     super(Personnel_status, self).__init__(**kwargs)
    #     self.date = date
    #     self.am_status = am_status
    #     self.am_remarks = am_remarks
    #     self.pm_status = pm_status
    #     self.pm_remarks = pm_remarks


    def __repr__(self):
        return '<Record {}>'.format(self.date)

