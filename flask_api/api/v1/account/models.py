from flask_restx import Model, fields, SchemaModel


auth_model = Model(
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
            'email': {'type': 'string'},
            'password': {'type': 'string'},
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
