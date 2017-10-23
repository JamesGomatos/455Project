from . import db, login_manager
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from flask_login import UserMixin


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

    @staticmethod
    def insert_users():
        users = {
            1: ('james', 'dog', 169),
            2: ('joe', 'dog', 367),
        }
        for i in users:
            user = User()
            user.id = i
            user.usrename = users[i][0]
            user.password = users[i][1]
            user.squadron_id = users[i][2]
            user.type = users[i][3]
            db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '< User %r>' % self.username



class Mechanic(User):
    __tablename__ = 'mechanic'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__= {'polymorphic_identity': 'mechanic'}

    @staticmethod
    def insert_mechanics():
        for i in range(5):
            mechanic = Mechanic()
            mechanic.id = i
            mechanic.usrename = "james"
            db.session.add(mechanic)
        db.session.commit()


    def __repr__(self):
        return '<Mechanic %r>' % self.name

class Pilot(User):
    __tablename__ = 'pilot'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    t_m_s = db.Column(db.Integer)
    hours = db.Column(db.Integer)

    __mapper_args__={
        'polymorphic_identity': 'pilot',

    }

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
            169: ('North Carolina'),
            269: ('South Carolina')
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
    squardron_id = db.Column(db.Integer, db.ForeignKey('squadron.id'))
    t_m_s = db.Column(db.String(64))
    airframe_hours = db.Column(db.Integer)

    def __repr__(self):
        return '<Aircraft %r' % self.id


class Engine(db.Model):
    __tablename__ = 'engines'
    id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'))
    position = db.Column(db.Integer)
    e_hours = db.Column(db.Integer)

    def __repr__(self):
        return '<Engine %r' % self.id

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key = True)
    pilot_id =db.Column(db.Integer, db.ForeignKey('pilot.id'))
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'))
    date = db.column(db.Date)
    hours = db.column(db.Integer)

    def __repr__(self):
        return '<Flight %r' % self.id

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
    return Employee.query.get(id)
