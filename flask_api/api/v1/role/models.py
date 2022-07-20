from flask_restx import Model, fields, SchemaModel


role_model = Model(
    'Role',
    {
        'id': fields.String(readonly=True),
        'name': fields.String(required=True),
        'description': fields.String(required=False),
    },
)

user_roles = Model(
    'UserRoles',
    {
        'id': fields.String,
        # 'email': fields.String,  for debug purposes
        'roles': fields.List(fields.Nested(role_model))
    }
)
