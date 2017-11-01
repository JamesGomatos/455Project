from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Aircraft, Engine, Mechanic, MaintenanceDue
from sqlalchemy.sql import select

'''
render the index menu when called.
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
render the aircrafts when button pressed in the mechanic menu
'''
@main.route('/mechanic/aircraft')
def mechanic_get_aircraft():
    data = Aircraft.query.all()
    return render_template('mechanic/aircraft.html', data=data)

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
    return render_template('mechanic/maintenanceDue.html', data=data)


'''
render complete_maintenance menu when button pression in the mechanic menu
'''
@main.route('/mechanic/complete_maintenance')
def mechanic_complete_maintenance():
    return render_template('mechanic/complete_maintenance.html')
