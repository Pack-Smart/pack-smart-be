import datetime
import json
# import code; code.interact(local=dict(globals(), **locals()))

import flask
import bleach

from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
# from api import db
# from api.database.models import Item

# import pdb; pdb.set_trace()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello!</h1>"


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

app.run()

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


# @app.route('/api/v1/lists/new', methods=['GET'])
# def index():
#     items = Item.query.order_by(Item.name.asc()).all()
