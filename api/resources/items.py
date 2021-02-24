import datetime
import json
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import Item
from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects import postgresql
from sqlalchemy import or_

def _item_payload(item):
  return {
    "name": item.name,
    "item_id": item.id,
    "quantity": 0,
    "is_checked": False
  }

class ItemsResource(Resource):

  def post():
      ## not fully done need to talk to the front end and finish passing in the variables
    data = request.get_json()
    weathers = data['data']['attributes']['weather']
    user_categories = data['data']['attributes']['categories']
    genders = data['data']['attributes']['gender']

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
          "tripDetails": data['data']['attributes']['tripDetails'],
          "categories": categories
        }
      }
    }

    return jsonify(category_obj)

