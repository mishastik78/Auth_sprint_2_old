from .config import v1 as api_v1, api
from .account import acc

api.add_namespace(acc)
