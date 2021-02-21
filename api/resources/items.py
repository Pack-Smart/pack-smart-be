import datetime
import json
# import code; code.interact(local=dict(globals(), **locals()))

from flask import Flask
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import Item
from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.dialects import postgresql
from sqlalchemy import or_
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pack-smart-dev'
db = SQLAlchemy(app)



# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

def _item_payload(item):
  return {
    "name": item.name,
    "quantity": 0,
    "is_checked": False
  }

@app.route('/api/v1/list/new', methods=['GET'])
def list():
      ## not fully done need to talk to the front end and finish passing in the variables
      weathers = ['%hot%', 'all']
      user_categories = ['clothing']
      genders = ['all', 'female']
      
      items = db.session.query(Item).filter(
        or_(*[Item.weather.ilike(weather) for weather in weathers]), 
        or_(*[Item.category.like(category) for category in user_categories]),
        or_(*[Item.gender.like(gender) for gender in genders])
        )

      categories = {}
      for item in items:
        if item.category in categories:
          categories[item.category].append(_item_payload(item))
        else:
          categories[item.category] = []
          categories[item.category].append(_item_payload(item))

      category_obj = {
        "data": {
        "id": datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4()),
        "type": "Survey_Results",
        "attributes": {
         "categories": categories
        }
      }
    }

      return jsonify(category_obj)

@app.route('/', methods=['GET'])
def home():
  items = db.session.query(Item).all()
  categories = {}

  for item in items:
    if item.category in categories:
      categories[item.category].append(_item_payload(item))
    else:
      categories[item.category] = []
      categories[item.category].append(_item_payload(item))


  category_obj = {
    "data": {
      "id": datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4()),
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
