import datetime
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import ItemLists, Item
from datetime import datetime
from uuid import uuid4

class ItemList(Resource):
  def patch(self, item_list_id):
    item_list = db.session.query(ItemLists).filter(ItemLists.id == item_list_id).first()
    import pdb ; pdb.set_trace()