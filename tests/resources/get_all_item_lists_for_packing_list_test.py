import json
import unittest
from copy import deepcopy
from api.database.models import PackingLists, ItemLists, Item, Users

from api import create_app, db
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type

class GetAllItemLists(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client()

    self.user_1 = Users(username = "Jose")
    self.user_1.insert()
    self.user_2 = Users(username = "Kevin")
    self.user_2.insert()

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


    self.packing_list_1 = PackingLists(title = "Hawaii Trip", user_id = 1, num_of_days = 7, destination = "Hawaii")
    self.packing_list_1.insert()

    self.packing_list_2 = PackingLists(title = "Paris Trip", user_id = 2, num_of_days = 20, destination = "Paris")
    self.packing_list_2.insert()

    self.item_list_1 = ItemLists(packing_list_id = 1, item_id = self.item_1.id, quantity = 5, is_checked = False)
    self.item_list_1.insert()

    self.item_list_2 = ItemLists(packing_list_id = 1, item_id = self.item_5.id, quantity = 50, is_checked = True)
    self.item_list_2.insert()

    self.item_list_3 = ItemLists(packing_list_id = 1, item_id = self.item_2.id, quantity = 20, is_checked = True)
    self.item_list_3.insert()

    self.item_list_4 = ItemLists(packing_list_id = 2, item_id = self.item_3.id, quantity = 4, is_checked = True)
    self.item_list_4.insert()

    self.item_list_5 = ItemLists(packing_list_id = 2, item_id = self.item_4.id, quantity = 100, is_checked = False)
    self.item_list_5.insert()

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()

  def test_it_returns_all_item_list_for_packing_list(self):
    response = self.client.get(
      f'/api/v1/packing_lists/{self.packing_list_1.id}'
    )

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))['data']

    self.assertEqual(2, len(data['attributes']['categories']['Accessories']))
    self.assertEqual(1, len(data['attributes']['categories']['Toiletries']))
    self.assertEqual('Hats', data['attributes']['categories']['Accessories'][0]['name'])
    self.assertEqual('Belts', data['attributes']['categories']['Accessories'][1]['name'])
    self.assertEqual('Birth Control', data['attributes']['categories']['Toiletries'][0]['name'])
    self.assertEqual(1, data['attributes']['tripDetails']['packing_list_id'])
    self.assertEqual('Hawaii Trip', data['attributes']['tripDetails']['title'])
    self.assertEqual(7, data['attributes']['tripDetails']['num_of_days'])
    self.assertEqual('Hawaii', data['attributes']['tripDetails']['destination'])

