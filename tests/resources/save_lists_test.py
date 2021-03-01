import json
import unittest
from copy import deepcopy
from api.database.models import Users, Item
import psycopg2
from api import create_app, db
from tests import db_drop_everything

class SavePackingListTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.payload = {
      "data": {
        "userID": 1,
        "tripDetails": {
          "title": "Vice City",
          "destination": "Miami",
          "duration": 2
        },
        "items": [
          {
            "is_checked": True,
            "item_id": 1,
            "quantity": 1
          },
          {
            "is_checked": True,
            "item_id": 2,
            "quantity": 15
          }
        ]
      }
    }

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()

  def test_it_saves_the_packing_list(self):
    user_1 = Users(username='kd9madrid')
    user_1.insert()

    item_1 = Item(item='Hat',category='Accessory',weather='Hot',gender='All')
    item_2 = Item(item='Watch',category='Accessory',weather='All',gender='All')

    item_1.insert()
    item_2.insert()


    payload = deepcopy(self.payload)

    response = self.client.post(
      '/api/v1/packing_lists/new', json=(payload),
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))

    self.assertEqual('Packing List Saved!', data['message'])
    self.assertEqual(200, data['status_code'])




