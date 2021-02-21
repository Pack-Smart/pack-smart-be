import datetime
import json
# import code; code.interact(local=dict(globals(), **locals()))

from flask import Flask
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import Item

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pack_smart_dev'
db = SQLAlchemy(app)



# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

def _item_payload(item):
  return {
    "name": item.name,
    "quantity": 0,
    "is_checked": False
  }

@app.route('/', methods=['GET'])
def home():
  items = db.session.query(Item).all()
  categories = {}

  for item in items:
    # import pdb; pdb.set_trace()
    if item.category in categories:
      categories[item.category].append(_item_payload(item))
    else:
      categories[item.category] = []
      categories[item.category].append(_item_payload(item))


  category_obj = {
    "data": {
      "id": 0,
      "type": "Survey_Results",
      "attributes": {
        "categories": categories
      }
    }
  }

  return jsonify(category_obj)

app.run()



# @app.route('/api/v1/lists/new', methods=['GET'])
# def index():
#     items = Item.query.order_by(Item.name.asc()).all()
