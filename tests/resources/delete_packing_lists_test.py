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
    self,packing_list_1 = PackingLists(list_title='To Mars', user_id=1, num_of_days=6, destination="Mars")
    self.packing_list_1.insert()
    self.packing_list_2 = PackingLists(list_title='London', user_id=1, num_of_days=2, destination="UK")
    self.packing_list_2.insert()

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()


  def test_packing_list_can_be_deleted(self):

    all_packing_lists = db.session.query(PackingLists).all()
    import pdb; pdb.set_trace()
    
    response = self.client.get(
      f'/api/v1/packing_lists/{self.packing_list_2.id}'
    )

    self.assertEqual(200, response.status_code)