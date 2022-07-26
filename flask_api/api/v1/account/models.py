from flask_restx import Model, SchemaModel, fields

create_model = Model(
    'Cridentials_new',
    {
        'email': fields.String(required=True, pattern=r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$'),
        'password': fields.String(required=True, pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)[A-Za-z\d\W]{8,20}$'),
    },
)
login_model = Model(
    'Cridentials',
    {
        'email': fields.String(required=True),
        'password': fields.String(required=True),
    },
)
changing_model = SchemaModel(
    'Changing',
    {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'pattern': r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$'},
            'password': {'type': 'string', 'pattern': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)[A-Za-z\d\W]{8,20}$'},
        },
        'anyOf': [{'required': ['email']}, {'required': ['password']}]
    })

tokens_model = Model(
    'Tokens',
    {
        'access_token': fields.String,
        'access_token_expired_utc': fields.DateTime(dt_format='rfc822'),
        'refresh_token': fields.String,
        'refresh_token_expired_utc': fields.DateTime(dt_format='rfc822'),
    }
)

history_model = Model(
    'History',
    {
        'action': fields.String,
        'datetime': fields.DateTime(dt_format='rfc822', attribute='created_at'),
    }
)
