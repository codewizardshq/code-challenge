from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from application.config import Config
from application import create_app
from application import db
# db = SQLAlchemy()
app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

import application.models

if __name__ == '__main__':
    manager.run()