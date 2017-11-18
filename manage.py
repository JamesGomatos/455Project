#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Mechanic, Pilot, Squadron, Aircraft, Engine, Flight, MaintenanceDue, MaintenanceHistory
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Mechanic=Mechanic, Pilot=Pilot, Squadron=Squadron,
    Aircraft=Aircraft, Engine=Engine, Flight=Flight, MaintenanceDue=MaintenanceDue, MaintenanceHistory=MaintenanceHistory)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


#-----------------------------SQL VIEWS-------------------------------------
@app.before_first_request
def createAircraftView():
    c = db.engine.connect()
    c.execute("DROP VIEW IF EXISTS aircraft_view")
    c.execute("CREATE VIEW IF NOT EXISTS aircraft_view (id, t_m_s, squardron_id, airframe_hours) AS SELECT id, t_m_s, squardron_id, airframe_hours FROM aircrafts")


if __name__ == '__main__':
    manager.run()
