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
    "title": packing_list.list_title,
    "num_of_days": packing_list.num_of_days,
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
    list_title = data['data']['tripDetails']['title']
    number_of_days = data['data']['tripDetails']['number_of_days']
    destination = data['data']['tripDetails']['destination']
    items = data['data']['items']

    packing_list = PackingLists(
      list_title=list_title,
      user_id=user_id,
      num_of_days=number_of_days,
      destination=destination
    )

    packing_list.insert()

    for item in items:
      item_list = ItemLists(
        item_id=item['item_id'],
        packing_list_id=packing_list.id,
        quantity=item['quantity'],
        is_checked=item['is_checked']
      )

      item_list.insert()

    return {
      "message": "Packing List Saved!",
      "status_code": 200
    }


class UserPackingListsResource(Resource):
  def get(self, packing_list_id):
        pass

  def delete(self, packing_list_id):
    packing_list = db.session.query(PackingLists).filter(PackingLists.id == packing_list_id).first()
    
    if bool(db.session.query(PackingLists).filter(PackingLists.id == packing_list_id).first()):
      packing_list.delete()
      return jsonify({"success": "Packing list has been deleted"})
    else:
      return jsonify({"error": "Packing list does not exists"})

      