import json
import unittest
from copy import deepcopy
from api.database.models import PackingLists, Users, ItemLists, Item

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

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()


  def test_packing_list_can_be_deleted(self):
    #Creating table info
    self.user_1 = Users(username='EternalFlame')
    self.user_1.insert()

    self.packing_list_1 = PackingLists(list_title='To Mars', user_id=1, num_of_days=6, destination="Mars")
    self.packing_list_1.insert()
    self.packing_list_2 = PackingLists(list_title='London', user_id=1, num_of_days=2, destination="UK")
    self.packing_list_2.insert()

    self.item_1 = Item(item='Hat',category='Accessory',weather='Hot',gender='All')
    self.item_1.insert()
    self.item_2 = Item(item='Watch',category='Accessory',weather='All',gender='All')
    self.item_2.insert()

    item_list_1 = ItemLists(packing_list_id=self.packing_list_1.id, item_id=self.item_1.id, quantity=5, is_checked=True)
    item_list_1.insert()
    item_list_2 = ItemLists(packing_list_id=self.packing_list_1.id, item_id=self.item_2.id, quantity=6, is_checked=False)
    item_list_2.insert()

    #Assertions before delete
    all_packing_lists = db.session.query(PackingLists).all()
    all_item_lists = db.session.query(ItemLists).all()

    self.assertEqual(2, len(all_packing_lists))
    self.assertEqual(2, len(all_packing_lists[0].item_lists))
    self.assertEqual(2, len(all_item_lists))

    #Calling route
    response = self.client.delete(
      f'/api/v1/packing_lists/{self.packing_list_1.id}'
    )

    #Assertions after delete
    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))
    success = "Packing list has been deleted"

    self.assertEqual(success, data["success"])

    all_packing_lists = db.session.query(PackingLists).all()
    all_item_lists = db.session.query(ItemLists).all()

    self.assertEqual(1, len(all_packing_lists))
    self.assertEqual(0, len(all_item_lists))

  def test_error_message_if_packing_list_does_not_exists(self):
      response = self.client.delete(
        '/api/v1/packing_lists/1'
      )

      data = json.loads(response.data.decode('utf-8'))
      error = "Packing list does not exists"
  
      self.assertEqual(error, data['error'])