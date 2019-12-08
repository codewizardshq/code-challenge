"""
Global Flask Application Setting

See `.flaskenv` for default settings.
 """

import os
import ipdb

class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'development')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql://root:password@localhost/code_challenge_db')
    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)

    if FLASK_ENV == 'development':
        DIST_DIR = os.path.join(ROOT_DIR, 'public')
        SQLALCHEMY_TRACK_MODIFICATIONS = True
    else:
        DIST_DIR = os.path.join(ROOT_DIR, 'dist')
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not os.path.exists(DIST_DIR) and FLASK_ENV != 'development':
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR),
            'If running for production please run yarn build first.',
            'If running for development ensure you have created a .flaskenv file.',
            'Check readme.md for more details.')



