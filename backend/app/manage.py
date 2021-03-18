"""
manage.py
- provides a command line utility for interacting with the
  application to perform interactive debugging and setup
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api.app import create_app
from api.models import db, Alias, Device, Place, Value, Measurement, Unit

app = create_app()

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

# migration utility command
manager.add_command('db', MigrateCommand)

# enable python shell with app context
@manager.shell
def shell_ctx():
    return dict(
        app=app,
        db=db,
        Alias=Alias,
        Device=Device,
        Place=Place,
        Measurement=Measurement,
        Unit=Unit,
        Value=Value
    )

if __name__ == '__main__':
    manager.run()