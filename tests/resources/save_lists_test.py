import json
import unittest
from copy import deepcopy
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
          " destination": "Miami",
          " number_of_days": 2
        },
        "items": [
          {
            "is_checked": True,
            "item_id": 3,
            "quantity": 1
          }
        ]
      }
    }

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()

  def test_it_saves_the_packing_list(self):
    payload = deepcopy(self.payload)

    response = self.client.post(
      '/api/v1/packing_list/new', json=(payload),
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)
