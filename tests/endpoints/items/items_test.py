import json
import unittest
from copy import deepcopy

from api import create_app, db
from manage import db_seed
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class GetListItemsTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    db_seed
    self.client = self.app.test_client()

    self.payload ={
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


  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()

  def test_it_returns_a_list_of_items(self):
    payload = deepcopy(self.payload)
    response = self.client.post(
      '/api/v1/list/new',
      json=payload,
      content_type='application/json'
    )
    # import pdb; pdb.set_trace()

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    import pdb; pdb.set_trace()
    assert_payload_field_type_value(self, data, 'success', bool, True)