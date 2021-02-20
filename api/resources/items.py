import datetime
import json

import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import db
from api.database.models import Item


# def _user_payload(user):
#     return {
#         'id': user.id,
#         'username': user.username,
#         'email': user.email,
#         'links': {
#             'get': f'/api/v1/users/{user.id}',
#             'patch': f'/api/v1/users/{user.id}',
#             'delete': f'/api/v1/users/{user.id}',
#             'index': '/api/v1/users',
#         }
#     }