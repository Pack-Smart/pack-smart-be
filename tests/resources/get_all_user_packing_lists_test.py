import json
import unittest
from copy import deepcopy
from api.database.models import PackingLists, Users

from api import create_app, db
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class GetAllUserPackingLists(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()
    self.user_1 = Users(username='EternalFlame')
    self.user_1.insert()

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()


  def test_it_returns_a_list_of_items(self):
    user_2 = Users(username='CrimsonGhost')
    user_2.insert()

    packing_list_1 = PackingLists(title='To Mars', user_id=1, num_of_days=6, destination="Mars")
    packing_list_1.insert()
    packing_list_2 = PackingLists(title='London', user_id=1, num_of_days=2, destination="UK")
    packing_list_2.insert()
    packing_list_3 = PackingLists(title='Tokyo', user_id=2, num_of_days=7, destination="Japan")
    packing_list_3.insert()

    response = self.client.get(
      f'/api/v1/users/{self.user_1.id}/packing_lists'
    )

    self.assertEqual(200, response.status_code)
    data = json.loads(response.data.decode('utf-8'))['data']
    
    self.assertEqual(2, len(data['attributes']['PackingLists']))
    self.assertEqual(packing_list_1.id, data['attributes']['PackingLists'][1]['list_id'])
    self.assertEqual(packing_list_1.title, data['attributes']['PackingLists'][1]['title'])
    self.assertEqual(packing_list_1.num_of_days, data['attributes']['PackingLists'][1]['num_of_days'])
    self.assertEqual(packing_list_1.destination, data['attributes']['PackingLists'][1]['destination'])

  def test_it_returns_user_does_not_exist_error(self):
    response = self.client.get(
      '/api/v1/users/2/packing_lists'
    )

    self.assertEqual(200, response.status_code)
    data = json.loads(response.data.decode('utf-8'))
    
    self.assertEqual('User does not exists', data['error'])

