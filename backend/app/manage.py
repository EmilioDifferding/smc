"""
manage.py
- provides a command line utility for interacting with the
  application to perform interactive debugging and setup
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api.app import create_app
from api.models import db, Alias, Device, Place, Value, Measurement, Unit, User, Role

app = create_app()

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

def create_admin():
    user = User(name='smc_admin',email='emilio.differding@uner.edu.ar',password='smc-admin.357')
    db.session.add(user)
    db.session.commit()
    return 'ok'

# migration utility command
manager.add_command('db', MigrateCommand)

# manager.add_command('coso', create_admin)

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
        Value=Value,
        User=User,
        Role=Role
    )

if __name__ == '__main__':
    manager.run()