import json
import unittest
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
          "gender": ["All", "Female"],
          "weather": ["All", "%hot%"],
          "destination": "Miami",
          "tripDetails": {
              "title": "Night life",
              "destination": "Vice city",
              "number_of_days": "7"
            },
          "number_of_days": "7",
          "categories": ["Clothing", "Accessories", "Toiletries", "Essentials", "Wedding", "Beach", "Child 0-2"]
        }
      }
    }

  def test_it_returns_a_list_of_items(self):
    payload = deepcopy(self.payload)

    response = self.client.post(
      '/api/v1/list/new', json=(payload),
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))

    cat_len = len(data['data']['attributes']['categories'])
    self.assertEqual(6, cat_len)

    access_len = len(data['data']['attributes']['categories']['Accessories'])
    self.assertEqual(6, access_len)

    first_access = data['data']['attributes']['categories']['Accessories'][0]
    self.assertEqual(False, first_access['is_checked'])
    self.assertEqual('Belts', first_access['name'])
    self.assertEqual(0, first_access['quantity'])

    beach_len = len(data['data']['attributes']['categories']['Beach'])
    self.assertEqual(5, beach_len)

    child_0_2_len = len(data['data']['attributes']['categories']['Child 0-2'])
    self.assertEqual(27, child_0_2_len)
