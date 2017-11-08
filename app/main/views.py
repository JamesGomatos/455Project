from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Aircraft, Engine, Mechanic, MaintenanceDue, Flight, Pilot
from sqlalchemy.sql import text

'''
render the correct menu when the home button is pressed for pilots and
mechanics.
'''
@main.route('/')
def index():
    return render_template('index.html')

'''
render the mechanic menu when called
'''
@main.route('/mechanic')
def mechanic_menu():
    return render_template('mechanic/menu.html')

'''
  Query to retrieve aircraft by squadron
'''
@main.route('/mechanic/aircraft')
def mechanic_get_aircraft():
    squardron_id = current_user.squadron_id
    result=[]
    sql = "SELECT * FROM aircrafts WHERE squardron_id = ?"
    c = db.engine.connect()
    for row in c.execute(sql, (squardron_id,)):
        result.append(row)
    return render_template('mechanic/aircraft.html', result=result)

'''
render list of engines when button pressed in the mechanic menu
'''
@main.route('/mechanic/engine')
def mechanic_get_engine():
    data = Engine.query.all()
    return render_template('mechanic/engine.html', data=data)

'''
render list of mechanics when button pressed in the mechanic menu
'''
@main.route('/mechanic/list')
def mechanic_get_list():
    data = Mechanic.query.all()
    return render_template('mechanic/list.html', data=data)


'''
render maintenance due list when button pressed in the mechanic menu
'''
@main.route('/mechanic/maintenance_due')
def mechanic_get_maintenance_due():
    data = MaintenanceDue.query.all()
    return render_template('mechanic/maintenance_due.html', data=data)


'''
render complete_maintenance menu when button pressed in the mechanic menu
'''
@main.route('/mechanic/complete_maintenance')
def mechanic_complete_maintenance():
    return render_template('mechanic/complete_maintenance.html')

'''
render the piot menu when called
'''
@main.route('/pilot/menu')
def pilot_menu():
    return render_template('pilot/menu.html')

'''
render the flight query when button pressed in the pilot menu
'''
@main.route('/pilot/flights')
def pilot_get_flight():
    data =  Flight.query.all()
    return render_template('pilot/flights.html', data=data)

'''
render the add flight menu when button pressed in the pilot menu
'''
@main.route('/pilot/add_flight')
def pilot_add_flight():
    return render_template('pilot/add_flight.html')


'''
render the a list of pilots when button view pilots button is
pressed  in the pilot menu
'''
@main.route('/pilot/pilots')
def pilot_list():
    data = Pilot.query.all()
    return render_template('pilot/pilots.html', data=data)
