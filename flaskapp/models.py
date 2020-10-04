from flaskapp import db, login_manager
from datetime import datetime
from sqlalchemy.orm import validates
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash


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

    def set_fmw(self, fmw):
        self.fmw = fmw

    def get_fmw(self):
        return self.fmw


login_manager.anonymous_user = MyAnonymousUser

# Code below represents the tables that are used in the database


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    clearance = db.Column(db.Integer, nullable=False)

    fmw_id = db.Column(db.Integer, db.ForeignKey('fmw.id'), nullable=False)
    fmw = db.relationship('Fmw', back_populates='user')

    @validates('clearance')
    def validate_clearance(self, key, clearance):
        if not 1 <= clearance <= 3:
            raise AssertionError('Clearance should be an int value form 1 to 3') 
        return clearance @validates('clearance')

    def __init__(self, username='', password='', clearance=3):
        self.username = username
        self.password = generate_password_hash(password).decode('utf8')

    def check_password(self, password_str):
        # return check_password_hash(self.password, password_str)
        return self.password == password_str

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    rank = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    fmw_id = db.Column(db.Integer, db.ForeignKey('fmw.id'), nullable=False)
    fmw = db.relationship('Fmw',back_populates='personnel')
    # statuses = db.relationship('Personnel_status', backref=db.backref('Person', lazy=False))
    status = db.relationship('Personnel_status', back_populates='person')

    def __init__(self, rank, name, fmw_id, active=True):
        self.rank = rank
        self.name = name
        self.active = active
        self.fmw_id = fmw_id
        
    def __repr__(self):
        return '<User {}>'.format(self.name)


class Personnel_status(db.Model):
    __tablename = "personnel_status"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    am_status = db.Column(db.Text)
    am_remarks = db.Column(db.Text)
    pm_status = db.Column(db.Text)
    pm_remarks = db.Column(db.Text)

    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    person = db.relationship('Personnel', back_populates='status')
    
    def __init__(self, date, am_status, am_remarks, pm_status, pm_remarks, personnel_id):
        self.date = date
        self.am_status = am_status
        self.am_remarks = am_remarks
        self.pm_status = pm_status
        self.pm_remarks = pm_remarks
        self.personnel_id = personnel_id

    def __repr__(self):
        return '<Record {}>'.format(self.date)


class Fmw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    fmd_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    unit = db.relationship('Unit',back_populates='fmw')
    # personnels = db.relationship('Personnel',backref=db.backref('fmw', lazy=False))
    # users = db.relationship('User', backref=db.backref('fmw', lazy=False))
    personnel = db.relationship('Personnel', back_populates='fmw')
    user = db.relationship('User', back_populates='fmw')

    def __init__(self, name=''):
        self.name = name
        
    def __repr__(self):
        return '<Fmw {}>'.format(self.name)


class Unit(db.Model):
    __tablename = "unit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer,nullable=False)

    # fmws = db.relationship('Fmw',backref=db.backref('unit', lazy=False))
    fmw = db.relationship('Fmw',back_populates='unit')

    def __init__(self, name=''):
        self.name = name
        
    def __repr__(self):
        return '<Unit {}>'.format(self.name)
