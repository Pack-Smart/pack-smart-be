import datetime
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import ItemLists
from datetime import datetime
from uuid import uuid4

class ItemListResource(Resource):
  def patch(self):
    items_mappings = request.get_json()['data']['items']

    db.session.bulk_update_mappings(ItemLists, items_mappings)
    db.session.commit()

  def delete(self):
    item_list_id = request.get_json()['data']['item']['id']
    item_list = db.session.query(ItemLists).filter(ItemLists.id == item_list_id).first()

    if bool(item_list):
      item_list.delete()
      return jsonify({"success": "Packing list item has been deleted"})
    else:
      return jsonify({"error": "Packing list item does not exists"})