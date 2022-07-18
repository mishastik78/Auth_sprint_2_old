from dotenv import load_dotenv
from os import environ

load_dotenv()

# Flask
FLASK_ENV = environ.get('FLASK_ENV', 'production')
USER_ID_FIELD = 'email'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = (f'postgresql://{environ.get("DB_USERNAME")}:{environ.get("DB_PASSWORD")}@'
                           f'{environ.get("DB_HOST")}:{environ.get("DB_PORT", 5432)}/{environ.get("DB_NAME")}')
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT Extended
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
JWT_TOKEN_LOCATION = 'headers'
JWT_ACCESS_TOKEN_EXPIRES = 60

# REST-X
RESTX_MASK_SWAGGER = False
