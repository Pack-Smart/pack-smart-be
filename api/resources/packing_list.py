import datetime
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import Users, PackingLists, ItemLists, Item
from datetime import datetime
from uuid import uuid4

def _packing_list_payload(packing_list):
      return {
    "list_id": packing_list.id,
    "title": packing_list.title,
    "duration": packing_list.num_of_days,
    "destination": packing_list.destination
  }

class PackingListResource(Resource):

  def get(self, user_id):
    if bool(db.session.query(Users).filter(Users.id == user_id).first()):
        packing_lists = db.session.query(PackingLists).filter(PackingLists.user_id==user_id).all()
        packing_lists_formatted = []

        for packing_list in packing_lists:
            packing_lists_formatted.insert(-1, _packing_list_payload(packing_list))

        packing_lists_object = {
            "data": {
            "id": datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4()),
            "type": "Packing_Lists",
            "attributes": {
            "PackingLists": packing_lists_formatted
            }
        }
    }
        return jsonify(packing_lists_object)
    else:
        return jsonify({"error": "User does not exists"})

class PackingListsResource(Resource):

  def post(self):
    data = request.get_json()
    user_id = data['data']['userID']
    title = data['data']['tripDetails']['title']
    number_of_days = data['data']['tripDetails']['duration']
    destination = data['data']['tripDetails']['destination']
    items_mappings = data['data']['items']

    packing_list = PackingLists(
      title=title,
      user_id=user_id,
      num_of_days=number_of_days,
      destination=destination
    )

    packing_list.insert()

    for item in items_mappings:
      item["packing_list_id"] = packing_list.id

    db.session.bulk_insert_mappings(ItemLists, items_mappings)
    db.session.commit()

    return {
      "data": {
        "listId": packing_list.id,
        "message": "Packing List Saved!",
        "status_code": 200
      }
    }


def _item_list_payload(item_list, item):
  return {
    "id": item_list.id,
    "item_id": item.id,
    "name": item.item,
    "quantity": item_list.quantity,
    "is_checked": item_list.is_checked
  }

def _custom_item_payload(item):
  return {
    "id": item.id,
    "item_id": item.id,
    "name": item.item,
    "quantity": item.quantity,
    "is_checked": item.is_checked
  }
class UserPackingListsResource(Resource):
  def get(self, packing_list_id):
    packing_list = db.session.query(PackingLists).filter(PackingLists.id == packing_list_id).first()
    item_lists = packing_list.item_lists
    custom_items = packing_list.custom_items
    categories = {}

    for item_list in item_lists:
      if item_list.items.category in categories:
        categories[item_list.items.category].append(_item_list_payload(item_list, item_list.items))
      else:
        categories[item_list.items.category] = []
        categories[item_list.items.category].append(_item_list_payload(item_list, item_list.items))

    for item in custom_items:
      if item.category in categories:
        categories[item.category].append(_custom_item_payload(item))
      else:
        categories[item.category] = []
        categories[item.category].append(_custom_item_payload(item))

    category_obj = {
        "data": {
        "id": datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4()),
        "type": "Item_List",
        "attributes": {
          "categories": categories,
          "tripDetails": {
            "listId": packing_list.id,
            "title": packing_list.title,
            "duration": packing_list.num_of_days,
            "destination": packing_list.destination
          }
        }
      }
    }

    return jsonify(category_obj)

  def patch(self, packing_list_id):
    update_packing_list = {
      'title': request.get_json()['title'],
      'num_of_days': request.get_json()['duration'],
      'destination': request.get_json()['destination']
    }

    db.session.query(PackingLists).filter(PackingLists.id == packing_list_id).update(update_packing_list)
    db.session.commit()

    packing_list = db.session.query(PackingLists).filter(PackingLists.id == packing_list_id).first()
    packing_list_payload = _packing_list_payload(packing_list)

    return packing_list_payload, 200



  def delete(self, packing_list_id):
    packing_list = db.session.query(PackingLists).filter(PackingLists.id == packing_list_id).first()

    if bool(packing_list):
      packing_list.delete()
      return jsonify({"success": "Packing list has been deleted"})
    else:
      return jsonify({"error": "Packing list does not exists"})

