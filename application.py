#
# used for ElasticBeanstalk
#

import os

from CodeChallenge import create_app

FLASK_ENV = os.getenv("FLASK_ENV")

if FLASK_ENV == "development":
    cfg = "DevelopmentConfig"
elif FLASK_ENV == "testing":
    cfg = "TestingConfig"
else:
    cfg = "ProductionConfig"


application = create_app(cfg)

if __name__ == "__main__":
    application.run()
