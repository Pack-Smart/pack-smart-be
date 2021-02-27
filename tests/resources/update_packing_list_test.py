import json
import unittest
from copy import deepcopy
from api.database.models import PackingLists, Users

from api import create_app, db
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class UpdatePackingList(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()
    self.user_1 = Users(username='kevxo')
    self.user_1.insert()

    self.payload = {
      "list_title": "To Jupiter",
      "num_of_days": 4,
      "destination": "Jupiter"
    }

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()

  def test_it_updates_packing_list(self):
    packing_list_1 = PackingLists(list_title='To Mars', user_id=1, num_of_days=6, destination="Mars")
    packing_list_1.insert()

    response = self.client.patch(
      '/api/v1/packing_lists/1', json=(self.payload),
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)
    data = json.loads(response.data.decode('utf-8'))

    self.assertEqual(1, data['list_id'])
    self.assertEqual('To Jupiter', data['title'])
    self.assertEqual(4, data['num_of_days'])
    self.assertEqual('Jupiter', data['destination'])


