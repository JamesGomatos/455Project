from . import db
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from flask_login import UserMixin


class Employee(UserMixin, db.Model, Base):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    usrename = db.Column(db.String(15))
    password = db.Column(db.String(80))
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity' : 'employee',
        'polymorphic_on': type
    }

    def __repr__(self):
        return '< Employee %r>' % self.username

class Engineer(Employee):
    __tablename__ = 'engineer'
    id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)

    __mapper_args__= {
        'polymorphic_identity': 'engineer',
    }


class Manager(Employee):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)

    __mapper_args__={
        'polymorphic_identity': 'manager',

    }


'''
class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Ciolumn(db.String(80))

class Role(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Integer(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
'''

'''
class Squadron(db.model):
    __tablename__= 'squadron'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64))

    def __repr__(self):
        return '<Squadron %r>' % self.id


class Mechanic(db.model):
    __tablename__='mechanics'
    id = db.Column(db.Integer, primary_key=True)
    squardron_id = db.Column(db.Integer, db.ForeignKey('squadron.id'))
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Mechanic %r>' % self.name

class Aircraft(db.model):
    __tablename__= 'aircrafts'
    id = db.Column(db.Integer, primary_key=True)
    squardron_id = db.Column(db.Integer, db.ForeignKey('squadron.id'))
    t_m_s = db.Column(db.String(64))
    airframe_hours = db.Column(db.Integer)

    def __repr__(self):
        return '<Aircraft %r' % self.id


class Engine(db.model):
    __tablename__ = 'engines'
    id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'))
    position = db.Column(db.Integer)
    e_hours = db.Column(db.Integer)

    def __repr__(self):
        return '<Engine %r' % self.id

class Pilot(db.model):
    __tablename__ = 'pilots'
    id = db.Column(db.Integer, primary_key=True)
    t_m_s = db.Column(db.Integer)
    squardron_id = db.Column(db.Integer, db.ForeignKey('squadron.id'))
    hours = db.Column(db.Integer)

    def __repr__(self):
        return '<Pilot %r' % self.id


class User(db.model):
    __tablename__'users'
    id = db.Column(db.Integer, primary_key=True)
    squardron_id = db.Column(db.Integer, db.ForeignKey('squadron.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(128))

class Role(db.model):
    __tablename__'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class Flight(db.model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key = True)
    pilot_id =db.Column(db.Integer, db.ForeignKey('pilots.id'))
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'))
    date = db.column(db.Date)
    hours = db.column(db.Integer)
    def __repr__(self):
        return '<Flight %r' % self.id

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)
'''
