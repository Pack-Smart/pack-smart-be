import json
import unittest
from flask import requests
from copy import deepcopy

from api import create_app, db
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class GetListItemsTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.payload = {
      "data": {
      "id": 0,
      "type": "survey",
      "attributes": {
          "gender": ["all", "male"],
          "weather": ["all", "%hot%", "%rainy%"],
          "destination": "Miami",
          "number_of_days": "7",
          "categories": ["wedding", "beach", "child_all", "child_0-2"]
        }
      }
    }

  def test_it_returns_a_list_of_items(self):
    # it('returns_a_list_of_items', () => request(app))
    response = self.client.get(
      '/api/v1/list/new', data=json.dumps(self.payload),
      headers='application/json'
    )
    import pdb; pdb.set_trace()

    self.assertEqual(200, response.status_code)