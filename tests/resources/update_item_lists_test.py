import json
import unittest
from copy import deepcopy
from api.database.models import PackingLists, Users, Item, ItemLists, CustomItem

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

    self.packing_list_1 = PackingLists(title='To Mars', user_id=1, num_of_days=6, destination="Mars")
    self.packing_list_1.insert()

    self.item_1 = Item(category = 'Accessories', weather = 'ALl', gender = 'All', item = 'Hats')
    self.item_1.insert()
    self.item_2 = Item(category = 'Toiletries', weather = 'ALl', gender = 'All', item = 'Birth Control')
    self.item_2.insert()
    self.item_3 = Item(category = 'Clothing', weather = 'ALl', gender = 'All', item = 'Pants')
    self.item_3.insert()
    self.item_4 = Item(category = 'Toiletries', weather = 'ALl', gender = 'All', item = 'Condom')
    self.item_4.insert()
    self.item_5 = Item(category = 'Accessories', weather = 'ALl', gender = 'All', item = 'Belts')
    self.item_5.insert()

    self.item_list_1 = ItemLists(packing_list_id = self.packing_list_1.id, item_id = self.item_1.id, quantity = 5, is_checked = False)
    self.item_list_1.insert()

    self.item_list_2 = ItemLists(packing_list_id = self.packing_list_1.id, item_id = self.item_5.id, quantity = 50, is_checked = True)
    self.item_list_2.insert()

    self.item_list_3 = ItemLists(packing_list_id = self.packing_list_1.id, item_id = self.item_2.id, quantity = 20, is_checked = True)
    self.item_list_3.insert()

    self.custom_item = CustomItem(item = 'Belt', quantity = 0, category = 'Accessories', is_checked = False, packing_list_id = self.packing_list_1.id)
    self.custom_item.insert()

    self.bulk_items_payload = {
      "data": {
        "item": [
          {
            "id": self.custom_item.id,
            "is_checked": True,
            "quantity": 32,
            "category": "something"
          },
          {
            "id": self.item_list_1.id,
            "is_checked": True,
            "quantity": 16
          }
        ]
      }
    }

    self.single_item_payload_custom = {
      "data": {
        "item": [
          {
            "id": self.custom_item.id,
            "is_checked": True,
            "quantity": 32,
            "category": "something"
          }
        ]
      }
    }

    self.single_item_payload_item_list = {
      "data": {
        "item": [
          {
            "id": self.item_list_1.id,
            "is_checked": True,
            "quantity": 32
          }
        ]
      }
    }

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()

  def test_it_can_update_item_lists_and_custom_items_in_bulk(self):

    self.assertEqual(5, self.item_list_1.quantity)
    self.assertEqual(False, self.item_list_1.is_checked)

    self.assertEqual(50, self.item_list_2.quantity)
    self.assertEqual(True, self.item_list_2.is_checked)

    self.assertEqual(20, self.item_list_3.quantity)
    self.assertEqual(True, self.item_list_3.is_checked)
    payload = deepcopy(self.bulk_items_payload)

    response = self.client.patch(
      '/api/v1/item_list/update', json=(payload),
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)

    self.assertEqual(16, self.item_list_1.quantity)
    self.assertEqual(True, self.item_list_1.is_checked)

    self.assertEqual(50, self.item_list_2.quantity)
    self.assertEqual(True, self.item_list_2.is_checked)

    self.assertEqual(20, self.item_list_3.quantity)
    self.assertEqual(True, self.item_list_3.is_checked)

  def test_it_can_update_single_item_list(self):
    
    self.assertEqual(5, self.item_list_1.quantity)
    self.assertEqual(False, self.item_list_1.is_checked)

    payload = deepcopy(self.single_item_payload_item_list)
    
    response = self.client.patch(
      '/api/v1/item_list/update', json=(payload),
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)

    self.assertEqual(32, self.item_list_1.quantity)
    self.assertEqual(True, self.item_list_1.is_checked)

  def test_it_can_update_single_custom_item(self):
      
    self.assertEqual(0, self.custom_item.quantity)
    self.assertEqual(False, self.custom_item.is_checked)

    payload = deepcopy(self.single_item_payload_custom)
  
    response = self.client.patch(
      '/api/v1/item_list/update', json=(payload),
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)

    self.assertEqual(32, self.custom_item.quantity)
    self.assertEqual(True, self.custom_item.is_checked)