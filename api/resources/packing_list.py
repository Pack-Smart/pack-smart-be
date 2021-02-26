import datetime
import json

from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import PackingLists, Users
from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.dialects import postgresql

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