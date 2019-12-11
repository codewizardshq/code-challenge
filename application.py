#
# used for ElasticBeanstalk
#

import os

from CodeChallenge import create_app

FLASK_ENV = os.environ.get("FLASK_ENV")

if FLASK_ENV and FLASK_ENV == "development":
    cfg = "DevelopmentConfig"
else:
    cfg = "ProductionConfig"


application = create_app("DevelopmentConfig")

if __name__ == "__main__":
    application.run()
