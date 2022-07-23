from flask_restx import Model, SchemaModel, fields

role_model = Model(
    'Role',
    {
        'id': fields.String(readonly=True),
        'name': fields.String(required=True),
        'description': fields.String(required=False),
    },
)

role_assign_model = SchemaModel(
    'AssignRole',
    {
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'name': {'type': 'string'},
        },
        'oneOf': [{'required': ['id']}, {'required': ['name']}]
    })

user_roles = Model(
    'UserRoles',
    {
        'id': fields.String,
        'email': fields.String,
        'roles': fields.List(fields.Nested(role_model))
    }
)
