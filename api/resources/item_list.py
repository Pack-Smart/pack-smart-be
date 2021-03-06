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

      return jsonify({"success": "Items have been updated"})

    else:
      if 'category' in items[0]:
        db.session.query(CustomItem).filter(CustomItem.id == items[0]['id']).update(items[0])
        db.session.commit()
        return jsonify({"success": "Item has been updated"})
      else:
        db.session.query(ItemLists).filter(ItemLists.id == items[0]['id']).update(items[0])
        db.session.commit()
        return jsonify({"success": "Item has been updated"})

  def delete(self):
    item = request.get_json()['data']['item']
    if "category" in item:
      item = db.session.query(CustomItem).filter(CustomItem.id == item["id"]).first()
    else:
      item = db.session.query(ItemLists).filter(ItemLists.id == item["id"]).first()

    if bool(item):
      item.delete()
      return jsonify({"success": "Packing list item has been deleted"})
    else:
      return jsonify({"error": "Packing list item does not exists"})