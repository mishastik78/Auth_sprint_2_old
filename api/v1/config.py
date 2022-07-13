from flask import Blueprint
from flask_restx import Api


v1 = Blueprint('api_v1', __name__,)
api = Api(
    v1,
    version='1.0',
    title='Auth REST API',
    description='Auth REST API',
)
