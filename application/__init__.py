import os
from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# Globally accessible libraries


def create_app():
    """Initialize the core application."""
    from .config import Config
    app = Flask(__name__, static_folder='../dist/static')
    app.config.from_object(Config())
    app.logger.info('>>> {}'.format(Config.FLASK_ENV))

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        # from . import routes
        # from .client import client_bp
        from .api import api_bp

        app.register_blueprint(api_bp)

        # Register Blueprints
        @app.route('/')
        def index_client():
            # ipdb.set_trace()
            dist_dir = app.config['DIST_DIR']
            entry = os.path.join(dist_dir, 'index.html')
            return send_file(entry)

        return app

db = SQLAlchemy()

# db = SQLAlchemy(app)
# db.init_app(app)

# Model = db.Model

# migrate = Migrate(app, db)
# db.create_all(app)


