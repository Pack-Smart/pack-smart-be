import datetime
from flask_cors import CORS
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