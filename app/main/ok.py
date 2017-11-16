from sqlalchemy.sql import text
from sqlalchemy import Table, MetaData
from sqlalchemy_views import CreateView, DropView

def createAircraftView():
    view = Table('aircraft_view', MetaData())
    definition = text("CREATE VIEW IF NOT EXISTS squardron_id  (id, squadron_id) AS SELECT id, squadron_id FROM aircrafts")
    create_view = CreateView(view, definition)
    a = create_view.compile()
    return a
