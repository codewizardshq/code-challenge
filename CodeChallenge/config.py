import os


class DefaultConfig:
    SECRET_KEY = "SUPERSECURE"
    APP_DIR = os.path.dirname(__file__)

    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_TOKEN_LOCATION = ["cookies"]

    # ensure JWT cookie is only sent to API routes
    JWT_ACCESS_COOKIE_PATH = "/api/"
    JWT_REFRESH_COOKIE_PATH = "/token/refresh"
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_SECRET_KEY = "super-secret"

    # https://www.epochconverter.com/
    CODE_CHALLENGE_START = ""
    RATELIMIT_HEADERS_ENABLED = True

    MAIL_SERVER = "localhost"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = "CodeWizardsHQ <no-reply@codewizardshq.com>"
    MAIL_SUPPRESS_SEND = True

    @property
    def ROOT_DIR(self):
        return os.path.dirname(self.APP_DIR)

    @property
    def DIST_DIR(self):
        return os.path.join(self.ROOT_DIR, "dist")


class ProductionConfig(DefaultConfig):
    # read as much as possible from envvars
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    CODE_CHALLENGE_START = os.environ.get("CODE_CHALLENGE_START")
    MAIL_SUPPRESS_SEND = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class DevelopmentConfig(ProductionConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://cc-user:password@localhost" \
                              "/code_challenge_local"
    JWT_COOKIE_SECURE = False
    CODE_CHALLENGE_START = os.environ.get("CODE_CHALLENGE_START", "1578596347")
    JWT_SECRET_KEY = "SuperSecret"
    SECRET_KEY = "flaskSecretKey"
    JWT_COOKIE_CSRF_PROTECT = False

    @property
    def DIST_DIR(self):
        return os.path.join(self.ROOT_DIR, "public")
