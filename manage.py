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


#-----------------------------SQL VIEWS----------------------------------------
@app.before_first_request
def createAircraftView():
    c = db.engine.connect()
    c.execute("DROP VIEW IF EXISTS aircraft_view")
    c.execute("CREATE VIEW IF NOT EXISTS aircraft_view (id, t_m_s, squardron_id, airframe_hours) AS SELECT id, t_m_s, squardron_id, airframe_hours FROM aircrafts")


#-----------------------------SQL TRIGGERS--------------------------------------

'''
WOULDN't this work beter after insert on the datase table
so it will update correct if somebody enters a date that is before or after
'''
@app.before_first_request
def createMaintMonthDueTrigger():
    c = db.engine.connect()
    c.execute('''CREATE TRIGGER IF NOT EXISTS init_monthly AFTER DELETE ON "maintenanceDues"
        WHEN OLD.description = "monthly inspection"
        BEGIN
        INSERT into maintenanceDues VALUES (OLD.job_id, OLD.aircraft_id, OLD.description,
        OLD.type_inspection, date(OLD.date_due, '+1 month'), OLD.hours_due);
        END;''')


#Create a trigger to update maint_due for '50 hr insp'
@app.before_first_request
def createMaint50DueTrigger():
    c = db.engine.connect()
    c.execute('''CREATE TRIGGER IF NOT EXISTS initiate_50hr AFTER DELETE ON "maintenanceDues"
             WHEN old.description = "50 hr insp"
             BEGIN
             INSERT into maintenanceDues VALUES (OLD.job_id, OLD.aircraft_id, OLD.description,
             OLD.type_inspection, OLD.date_due, (OLD.hours_due + 50));
             END;''')


# Trigger to update maint_due for 'eng_insp'
@app.before_first_request
def createMaintEngineInspTrigger():
    c = db.engine.connect()
    c.execute('''CREATE TRIGGER IF NOT EXISTS initiate_engInsp AFTER DELETE ON "maintenanceDues"
            WHEN old.description = "eng insp"
            BEGIN
            INSERT into maintenanceDues VALUES (OLD.job_id + 1, OLD.aircraft_id, OLD.description,
            OLD.type_inspection, OLD.date_due, OLD.hours_due + 100);
            END;''')



#Create a trigger to update aircraft hours after a flight
@app.before_first_request
def createUpdateEngineHoursTrigger():
    c = db.engine.connect()
    c.execute('''CREATE TRIGGER IF NOT EXISTS update_eng_hours AFTER INSERT ON "flights"
                 WHEN "aircraft_id" = new.aircraft_id
                 BEGIN
                 UPDATE aircraft_squadron SET airframe_hours = airframe_hours + new.hours;
                 END;''')



#Create a trigger to update aircraft hours after a flight
@app.before_first_request
def createUpdatePilotHoursTrigger():
    c = db.engine.connect()
    c.execute('''CREATE TRIGGER IF NOT EXISTS update_pilot_hrs AFTER INSERT ON "flights"
                 WHEN "pilots.pilot_id" = new.pilot_id
                 BEGIN
                 UPDATE pilots set hours = hours + new.hours;
                 END;''')



if __name__ == '__main__':
    manager.run()
