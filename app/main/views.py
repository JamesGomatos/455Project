from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Aircraft, Engine, Mechanic, MaintenanceDue, Flight, Pilot
from sqlalchemy.sql import text

#-----------------------------View Methods-------------------------------------
def createAircraftView():
    c = db.engine.connect()
    c.execute("DROP VIEW james")
    c.execute("CREATE VIEW IF NOT EXISTS james (id, squardron_id) AS SELECT id, squardron_id FROM aircrafts")

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
    createAircraftView()
    squardron_id = current_user.squadron_id
    result=[]
    sql = "SELECT * FROM james WHERE squardron_id = ?"
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

It really doesn't make sense to have a worker id  either because we
already have captured the worker ID based on who is logged in. Instead we should
probaby put a completion note or something?
'''
@main.route('/mechanic/complete_maintenance', methods=['GET', 'POST'])
def mechanic_complete_maintenance():
    error = None
    try:
        if request.method == 'POST':
            attempted_job_id = request.form['job_id']
            attmepted_worker_id = request.form
    except Exception as e:
        flash(e)
        return render_template('mechanic/complete_maintenance.html', error=error)
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
