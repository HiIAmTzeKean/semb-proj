from flaskapp import db, login_manager
from datetime import datetime
from sqlalchemy.orm import validates
from flask_login import UserMixin, AnonymousUserMixin


class MyAnonymousUser(AnonymousUserMixin):
    """Add custom methods to anonymous_user

    Context:
        This class will be used for Users who are not logged in

    Methods:
        current_user.set_fmw(fmw) sets the fmw for an anonymous user

        current_user.get_fmw() retrives the fmw for the anonymous user

        login_manager.anonymous_user = MyAnonymousUser takes customs and add it to AnonymousUserMixin
    """
    def __init__(self):
        self.fmw = None
    def set_fmw(self,fmw):
        self.fmw = fmw
    def get_fmw(self):
        return self.fmw
login_manager.anonymous_user = MyAnonymousUser

# Code below represents the tables that are used in the database

class User(db.Model,UserMixin):
    __tablename = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False,)
    password = db.Column(db.Text, nullable=False)
    fmw = db.Column(db.Text, nullable=False)
    fmd = db.Column(db.Integer, nullable=False)
    clearance = db.Column(db.Integer, nullable=False)
    unit_id = db.Column(db.Integer,db.ForeignKey('unit.id'), nullable=False)

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
    
    def get_fmw(self):
        return self.fmw

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
    unit_id = db.Column(db.Integer,db.ForeignKey('unit.id'), nullable=False)
    status = db.relationship('Personnel_status',backref=db.backref('Person', lazy=False))

    def __init__(self, rank='', name='', fmw='', fmd=''):
        self.rank = rank
        self.name = name
        self.fmw = fmw
        self.fmd = fmd
        
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
    

    def __init__(self,date='',am_status = '',am_remarks = '',pm_status = '',pm_remarks = '',personnel_id=''):
        self.date = date
        self.am_status = am_status
        self.am_remarks = am_remarks
        self.pm_status = pm_status
        self.pm_remarks = pm_remarks
        self.personnel_id = personnel_id


    def __repr__(self):
        return '<Record {}>'.format(self.date)

class Unit(db.Model):
    __tablename = "unit"
    id = db.Column(db.Integer, primary_key=True)
    fmd = db.Column(db.Integer,nullable=False)
    fmw = db.Column(db.Text,nullable=False)
    coy = db.relationship('Personnel',backref=db.backref('unit', lazy=False))
    member = db.relationship('User',backref=db.backref('unit', lazy=False))

    def __init__(self, fmw='', fmd=''):
        self.fmw = fmw
        self.fmd = fmd
        
    def __repr__(self):
        return '<Unit {}>'.format(self.fmd)
