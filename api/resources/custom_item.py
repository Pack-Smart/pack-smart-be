from typing import AsyncIterable
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import PackingLists, CustomItem

class CustomItemResource(Resource):
    
    def post(self):
      data = request.get_json()
      
      custom_item = CustomItem(
        item=data["data"]["attributes"]["item"],
        quantity=data["data"]["attributes"]["quantity"],
        is_checked=False,
        category=data["data"]["attributes"]["category"],
        packing_list_id=data["data"]["attributes"]["packing_list_id"]
      )

      custom_item.insert()

      return {
      "message": "Custom Item Saved!",
      "status_code": 200
    }