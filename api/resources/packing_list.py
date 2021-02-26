import datetime
import json
import bleach
from flask import request, jsonify
from flask_restful import Resource, abort
from api import db
from api.database.models import Users, PackingLists, ItemLists
from datetime import datetime
from uuid import uuid4
from sqlalchemy import or_


class PackingListResource(Resource):

  def post(self):
    data = request.get_json()
    user_id = data['data']['userID']
    list_title = data['data']['tripDetails']['title']
    number_of_days = data['data']['tripDetails']['number_of_days']
    destination = data['data']['tripDetails']['destination']

    packing_list = PackingLists(
      list_title=list_title,
      user_id=user_id,
      num_of_days=number_of_days,
      destination=destination
    )

    packing_list.insert()

    return "Packing List Saved!"
