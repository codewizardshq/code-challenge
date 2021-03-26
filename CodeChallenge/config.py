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

    MAIL_SERVER = "smtp.mailgun.org"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = "CodeWizardsHQ <no-reply@codewizardshq.com>"
    MAIL_SUPPRESS_SEND = True
    MG_PRIVATE_KEY = os.getenv("MG_PRIVATE_KEY")
    MG_LIST = "codechallenge@school.codewizardshq.com"
    WORKER_PASSWORD = os.getenv("WORKER_PASSWORD")
    SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
    SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
    SLACK_OAUTH_TOKEN = os.getenv("SLACK_OAUTH_TOKEN")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

    # no trailing /
    EXTERNAL_URL = "https://challenge.codewizardshq.com"

    # this will not work out of box. a proper docker setup is required.
    # the Docker image used for this is included but the architecture
    # around it is closed source and part of the existing CWHQ platform.
    SANDBOX_API_URL = "http://localhost:3000/"

    ALLOW_RESET = False

    # number of days to leave CodeChallenge open
    # past the final rank
    CHALLENGE_ENDS = 1

    BULK_IMPORT_SENDER = "Kelli at CodeWizardsHQ <kelli@codewizardshq.com>"

    @property
    def ROOT_DIR(self):
        return os.path.dirname(self.APP_DIR)

    @property
    def DIST_DIR(self):
        return os.path.join(self.ROOT_DIR, "dist")


class ProductionConfig(DefaultConfig):
    # read as much as possible from envvars
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_COOKIE_SECURE = True
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CODE_CHALLENGE_START = os.getenv("CODE_CHALLENGE_START")
    MAIL_SUPPRESS_SEND = os.getenv("MAIL_SUPPRESS_SEND", False)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    JWT_ACCESS_TOKEN_EXPIRES = 604800
    ALLOW_RESET = os.getenv("ALLOW_RESET")
    EXTERNAL_URL = os.getenv("EXTERNAL_URL")
    SANDBOX_API_URL = os.getenv("SANDBOX_API_URL")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SHEET_ID = os.getenv("SHEET_ID")
    MG_LIST = os.getenv("MG_LIST")
    ANSWER_ATTEMPT_LIMIT = "5 per 1 minutes"
    VOTING_DISABLED = True


class DevelopmentConfig(ProductionConfig):
    EXTERNAL_URL = "http://localhost:8080"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql://cc-user:password@localhost/code_challenge_local",
    )
    JWT_COOKIE_SECURE = False
    CODE_CHALLENGE_START = os.getenv("CODE_CHALLENGE_START", "1618349460")
    JWT_SECRET_KEY = "SuperSecret"
    SECRET_KEY = "flaskSecretKey"
    JWT_COOKIE_CSRF_PROTECT = False
    ALLOW_RESET = True
    MAIL_SUPPRESS_SEND = False
    TESTING = True
    TEST_EMAIL_RECIPIENT = "sam@codewizardshq.com"

    @property
    def DIST_DIR(self):
        return os.path.join(self.ROOT_DIR, "dist")


class TestingConfig(DefaultConfig):
    # read as much as possible from envvars
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_COOKIE_SECURE = True
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CODE_CHALLENGE_START = os.getenv("CODE_CHALLENGE_START")
    MAIL_SUPPRESS_SEND = os.getenv("MAIL_SUPPRESS_SEND", False)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    JWT_ACCESS_TOKEN_EXPIRES = 604800
    ALLOW_RESET = os.getenv("ALLOW_RESET")
    EXTERNAL_URL = os.getenv("EXTERNAL_URL")
    SANDBOX_API_URL = os.getenv("SANDBOX_API_URL")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SHEET_ID = os.getenv("SHEET_ID")
    MG_LIST = os.getenv("MG_LIST")
    ANSWER_ATTEMPT_LIMIT = "5 per 1 minutes"
