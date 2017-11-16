from . import db, login_manager
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from flask_login import UserMixin
from datetime import date
from sqlalchemy_views import CreateView, DropView
from sqlalchemy.sql import text
from sqlalchemy import Table, MetaData

class User(UserMixin, db.Model, Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    usrename = db.Column(db.String(15))
    password = db.Column(db.String(80))
    squadron_id = db.Column(db.Integer, db.ForeignKey('squadron.id'))
    type = db.Column(db.String(50))


    __mapper_args__ = {
        'polymorphic_identity' : 'user',
        'polymorphic_on': type
    }

    def what_type(self):
        return self.type

    def __repr__(self):
        return '< User %r>' % self.username


class Mechanic(User):
    __tablename__ = 'mechanic'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(80))
    __mapper_args__= {'polymorphic_identity': 'mechanic'}


    '''
    Insert mechanics into the database
    '''
    @staticmethod
    def insert_mechanics():
        users = {
            1: ('jh1234', 'Joe Heins', 'dog', 367),
            2: ('js9015', 'Joe Smith', 'dog', 267),
            3: ('rm1007', 'Roger Moore', 'dog', 169)
        }
        for i in users:
            mechanic = Mechanic()
            mechanic.id = i
            mechanic.usrename = users[i][0]
            mechanic.name = users[i][1]
            mechanic.password = users[i][2]
            mechanic.squadron_id = users[i][3]
            db.session.add(mechanic)
        db.session.commit()

    def __repr__(self):
        return '<Mechanic %r>' % self.name

class Pilot(User):
    __tablename__ = 'pilot'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # t_m_s = db.Column(db.String(15))
    name = db.Column(db.String(80))
    hours = db.Column(db.Integer)
    __mapper_args__={'polymorphic_identity': 'pilot'}


    '''
    Insert pilots into the database
    '''
    @staticmethod
    def insert_pilots():
        pilots = {
            4: ('jb1007','John Barker','dog', 367, 102),
            5: ('ej2015','Earl Johnson', 'dog', 169, 75),
            6: ('jj1111','Jimmy John', 'dog', 267, 101),
            7: ('mj0023', 'Michael Jordan', 'dog', 303, 200),
            8: ('pq1009', 'Parker Quan', 'dog', 367, 50),
            9: ('pp2100', 'Penelope Pawn', 'dog', 169, 125),
            10:('jm0101', 'John Michael', 'dog', 267, 92),
            11:('dw0045', 'David Williams', 'dog', 303, 100)
        }
        for i in pilots:
            pilot = Pilot()
            pilot.id = i
            pilot.usrename = pilots[i][0]
            pilot.name = pilots[i][1]
            pilot.password = pilots[i][2]
            pilot.squadron_id = pilots[i][3]
            pilot.hours = pilots[i][4]
            db.session.add(pilot)
        db.session.commit()

    def __repr__(self):
        return '<Pilot %r' % self.id



class Squadron(db.Model):
    __tablename__= 'squadron'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64))

    '''
    # Static method that inserts squadrons into the database
    squadrons = [('HMLA-367', 'California'), ('HMLA-169', 'California'),
    ('HMLA-267', 'California'), ('HMLA-303','California'),
    ('HMLA-167', 'North Carolina'), ('HMLA-269', 'North Carolina')
    '''
    @staticmethod
    def insert_squadrons():
        squads = {
            367: ('California'),
            169: ('California'),
            267: ('California'),
            303: ('California'),
            167: ('North Carolina'),
            269: ('North Carolina')
        }
        for i in squads:
            squadron = Squadron()
            squadron.id = i
            squadron.location=squads[i]
            db.session.add(squadron)
        db.session.commit()

    def __repr__(self):
        return '<Squadron %r>' % self.id


class Aircraft(db.Model):
    __tablename__= 'aircrafts'
    id = db.Column(db.Integer, primary_key=True)
    t_m_s = db.Column(db.String(64))
    squardron_id = db.Column(db.Integer, db.ForeignKey('squadron.id'))
    airframe_hours = db.Column(db.Integer)



    '''
    Insert aircraft data into the database
    '''
    @staticmethod
    def insert_aircrafts():
        data = {
            165339: ('UH-1Y', 367, 2122.5),
            165212: ('AH-1Z', 267, 1821.0),
            168221: ('UH-1Y', 269, 4890.2),
            168950: ('AH-1Z', 169, 1209.0),
            168001: ('AH-1Z', 303, 2121.2),
            167223: ('UH-1Y', 167, 2356.7),
            167991: ('UH-1Y', 267, 2100.0),
            168002: ('AH-1Z', 367, 1500.1)
        }
        for i in data:
            aircraft = Aircraft()
            aircraft.id = i
            aircraft.t_m_s = data[i][0]
            aircraft.squardron_id = data[i][1]
            aircraft.airframe_hours = data[i][2]
            db.session.add(aircraft)
        db.session.commit()


    def __repr__(self):
        return '<Aircraft %r' % self.id


class Engine(db.Model):
    __tablename__ = 'engines'
    id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'))
    position = db.Column(db.Integer)
    e_hours = db.Column(db.Integer)

    '''
    Insert engine data into the database
    '''
    def insert_engines():
        data = {
            121001: (165339, 1, 350.0),
            121031: (165339, 2, 489.5),
            121002: (165212, 1, 101.1),
            121003: (165212, 2,  125.0),
            121004: (168221, 1, 109.0),
            121005: (168221, 2, 351.0),
            121090: (168950, 1, 421.0),
            121081: (168950, 2, 220.0),
            121991: (168001, 1, 219.0),
            121901: (168001, 2, 315.1),
            121853: (167223, 1, 200.5),
            121852: (167223, 2, 209.0),
            121723: (167991, 1, 321.0),
            121709: (167991, 2, 329.1)
        }
        for i in data:
            engine = Engine()
            engine.id = i
            engine.aircraft_id = data[i][0]
            engine.position = data[i][1]
            engine.e_hours = data[i][2]
            db.session.add(engine)
        db.session.commit()

    def __repr__(self):
        return '<Engine %r' % self.id

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key = True)
    pilot_id =db.Column(db.Integer, db.ForeignKey('pilot.id'))
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'))
    hours = db.Column(db.Integer)
    date = db.Column(db.String(150))

    @staticmethod
    def insert_flights():
        data = {
        1700101: (4, 165339, 1, 'January 1, 2005 1:33PM'),
        1700201: (9, 168950, 2, 'January 2, 2005 2:33PM')
        }
        for i in data:
            flight = Flight()
            flight.id = i
            flight.pilot_id = data[i][0]
            flight.aircraft_id = data[i][1]
            flight.hours = data[i][2]
            flight.date = data[i][3]
            db.session.add(flight)
        db.session.commit()

    def __repr__(self):
        return '<Flight %r' % self.id

class MaintenanceDue(db.Model):
    __tablename__ = 'maintenanceDues'
    job_id = db.Column(db.Integer, primary_key = True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'), primary_key = True)
    description = db.Column(db.String(150))
    type_inspection =  db.Column(db.String(80))
    date_due = db.Column(db.String(150))
    hours_due = db.Column(db.Integer)

    @staticmethod
    def insert_maintenanceDueData():
        data = {
            3671700101: (165339, 'monthly inspection', 'A/F', '17-01-20', 2200.0),
            3031700201: (168001, 'eng insp', 'ENG', '17-10-10', 2150.0),
            1691700101: (168950, '200 hr insp', 'A/F', '17-10-20', 1409.0)
        }
        for i in data:
            due_data = MaintenanceDue()
            due_data.job_id = i
            due_data.aircraft_id = data[i][0]
            due_data.description = data[i][1]
            due_data.type_inspection = data[i][2]
            due_data.date_due = data[i][3]
            due_data.hours_due = data[i][4]
            db.session.add(due_data)
        db.session.commit()

    def __repr__(self):
        return '<MaintenanceDue %r' % self.job_id


class MaintenanceHistory(db.Model):
    '''Should job_id be a foreign key?'''
    job_id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'), primary_key = True)
    description = db.Column(db.String(150))
    type_inspection =  db.Column(db.String(80))
    aircraft_hours = db.Column(db.Integer)
    engine_hours = db.Column(db.Integer)
    mechanic_id = db.Column(db.Integer, db.ForeignKey(Mechanic.id))
    date_complete = db.Column(db.Date, primary_key=True)


    @staticmethod
    def insert_maintenanceHistoryData():
        data = {
            36734001: (165339, '100 hr insp', 'A/F', 2150.0, 'jh1234', date('16/12/02')),
            167330010: (167223, '50 hr insp', 'ENG', 2356.7, 'pm1005', date('16/11/28'))
        }
        for i in data:
            due_data = MaintenanceDue()
            due_data.job_id = i
            due_data.aircraft_id = data[i][0]
            due_data.description = data[i][1]
            due_data.type_inspection = data[i][2]
            due_data.aircraft_hours = data[i][3]
            due_data.usrename= data[i][4]
            due_data.mechanic_id = None
            due_data.date_complete = data[i][5]
            db.session.add(due_data)
        db.session.commit()


    def __repr__(self):
        return '<MaintenaceHistory %r' % self.job_id

'''
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

'''

@login_manager.user_loader
def user_loader(id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(id)


#------------------------------RUN ALL------------------------------------------
