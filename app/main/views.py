from __future__ import print_function
from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Aircraft, Engine, Mechanic, MaintenanceDue, Flight, Pilot, MaintenanceHistory
from sqlalchemy.sql import text
import sys
from datetime import date


#--------------------------MECHANIC MENU----------------------------------------
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

'''sqlalchemy_viewsviewsbiew
Query to retrieve aircraft by squadron using view

'''
@main.route('/mechanic/aircraft')
def mechanic_get_aircraft():
    squardron_id = current_user.squadron_id
    result=[]
    sql = "SELECT * FROM aircraft_view WHERE squardron_id = ?"
    c = db.engine.connect()
    for row in c.execute(sql, (squardron_id,)):
        result.append(row)
    return render_template('mechanic/aircraft.html', result=result)


'''
Query to retrieve a list of engines matched with aircraft,
specific to squadron. This query works but returns a weird result because there is no
engine that is associated with airraft ID 168002
'''
@main.route('/mechanic/engine')
def mechanic_get_engine():
    squardron_id = current_user.squadron_id
    result=[]
    sql = "SELECT a.id as engine_id, b.id as buno, b.t_m_s, b.squardron_id, a.position, a.e_hours " \
          "FROM engines as a LEFT OUTER JOIN aircrafts as b ON b.id = a.aircraft_id WHERE squardron_id = ?"
    c = db.engine.connect()
    for row in c.execute(sql, (squardron_id,)):
        result.append(row)
    return render_template('mechanic/engine.html', result=result)


'''
render list of mechanics when button pressed in the mechanic menu.
Can talk about what sqlalcehmy provides through .query and how it is
much easier and less messy than alternative.

Could include current_user do we highlight?


Need to decide if we want to
render all the mechanics or just those mechanics that are not equal to current
user and in the same squadron.

@main.route('/mechanic/list')
def mechanic_get_list():
    data = Mechanic.query.filter(Mechanic.id is not current_user.id and Mechanic.squadron_id is current_user.squadron_id)
    return render_template('mechanic/list.html', data=data)

'''
@main.route('/mechanic/list')
def mechanic_get_list():
    data = Mechanic.query.filter(Mechanic.id != current_user.id)
    return render_template('mechanic/list.html', data=data)


'''
render maintenance due list when button pressed in the mechanic menu

NOTE: need to show only maintenance dues which
are due for the specific squadron

SOMETHING TO ADD: could alert mechanics when their due dates are past due
by highlighting it red?
'''
@main.route('/mechanic/maintenance_due')
def mechanic_get_maintenance_due():
    data = MaintenanceDue.query.all()
    return render_template('mechanic/maintenance_due.html', data=data)


'''
render complete_maintenance menu when button is pressed in the mechanic menu.
I'm thinking that we shouldn't have the mechanic put in a date and instead
just automatically insert a timestamp. Could use momemt.js to continually show
something.

Should I add a trigger to insert?
'''
@main.route('/mechanic/complete_maintenance', methods=['GET', 'POST'])
def mechanic_complete_maintenance():
    data = MaintenanceDue.query.all()
    result=[]
    error = None
    try:
        if request.method == 'POST':
            job_id = request.form['job_id']
            description = request.form['description']
            date_complete = request.form['date_complete']
            sel = "SELECT aircraft_id, type_inspection, hours_due FROM maintenanceDues WHERE job_id = ?"
            dele = "DELETE FROM maintenanceDues WHERE job_id=? AND description=?"
            ins = " INSERT into MaintenanceHistory VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            c = db.engine.connect()
            data = c.execute(sel, (job_id,)).fetchone()
            aircraft_id = data.aircraft_id
            type_inspection = data.type_inspection
            aircraft_hours = data.hours_due
            mechanic_id = current_user.id
            c.execute(dele, (job_id, description,))
            c.execute(ins, (job_id, aircraft_id, description, data.type_inspection, data.hours_due, 0, current_user.id, date_complete))
            flash('You Successfully Completed Job ID ' + job_id)
            return redirect(url_for('main.mechanic_get_maintenance_history'))
    except Exception as e:
        flash(e)
        return render_template('mechanic/complete_maintenance.html', error=error)
    return render_template('mechanic/complete_maintenance.html', data=data)


@main.route('/mechanic/maintenance_history')
def mechanic_get_maintenance_history():
    data = MaintenanceHistory.query.all()
    return render_template('mechanic/maintenance_history.html', data=data)
#-------------------------------PILOT MENU--------------------------------------

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
