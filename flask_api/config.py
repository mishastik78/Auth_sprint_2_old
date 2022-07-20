from os import environ
from datetime import timedelta

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
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(weeks=4)

# REST-X
RESTX_MASK_SWAGGER = False

# Redis
REDIS_HOST = environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(environ.get('REDIS_PORT', 6379))
REDIS_URL = 'redis://default:redispw@localhost:55000' # f'redis://{REDIS_HOST}:{REDIS_PORT}'


# Logger
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': '%(levelprefix)s %(client_addr)s - \'%(request_line)s\' %(status_code)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'DEBUG',
        },
        'uvicorn.error': {
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
