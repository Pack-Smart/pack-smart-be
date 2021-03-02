import datetime
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import ItemLists, CustomItem
from datetime import datetime
from uuid import uuid4

class ItemListResource(Resource):
  def patch(self):
    items = request.get_json()['data']['item']

    if len(items) > 1:
      custom_items = []
      item_lists = []
      for item in items:
        if 'category' in item:
          custom_items.append(item)
        else:
          item_lists.append(item)
      
      db.session.bulk_update_mappings(CustomItem, custom_items)
      db.session.commit()

      db.session.bulk_update_mappings(ItemLists, item_lists)
      db.session.commit()

    else:
      if 'category' in items[0]:
        db.session.query(CustomItem).filter(CustomItem.id == items[0]['id']).update(items[0])
        db.session.commit()
      else:
        db.session.query(ItemLists).filter(ItemLists.id == items[0]['id']).update(items[0])
        db.session.commit()

  def delete(self):
    item_list_id = request.get_json()['data']['item']['id']
    item_list = db.session.query(ItemLists).filter(ItemLists.id == item_list_id).first()

    if bool(item_list):
      item_list.delete()
      return jsonify({"success": "Packing list item has been deleted"})
    else:
      return jsonify({"error": "Packing list item does not exists"})