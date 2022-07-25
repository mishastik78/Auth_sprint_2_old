from flask_restx import Model, SchemaModel, fields

role_create_model = Model(
    'Role',
    {
        'id': fields.String(readonly=True),
        'name': fields.String(required=True),
        'description': fields.String(required=False),
    },
)

role_patch_model = SchemaModel(
    'Role_patch',
    {
        'type': 'object',
        'properties': {
            'id': {'type': 'string'},
            'new_name': {'type': 'string'},
            'new_description': {'type': 'string'},
        },
        'oneOf': [{'required': ['id', 'new_name']}, {'required': ['id', 'new_description']}]
    })

role_delete_model = Model(
    'Role_delete',
    {
        'id': fields.String(required=True)
    }
)

role_assign_model = Model(
    'AssignRole',
    {
        'user_id': fields.String(required=True),
        'role_id': fields.String(required=True),
    }

)

user_roles = Model(
    'UserRoles',
    {
        'id': fields.String,
        'email': fields.String,
        'roles': fields.List(fields.Nested(role_create_model))
    }
)
