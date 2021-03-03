import json
import unittest
from copy import deepcopy
from api.database.models import PackingLists, Users, ItemLists, Item, CustomItem

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

    self.item_1 = Item(item='Hat',category='Accessory',weather='Hot',gender='All')
    self.item_1.insert()
    self.item_2 = Item(item='Watch',category='Accessory',weather='All',gender='All')
    self.item_2.insert()

    item_list_1 = ItemLists(packing_list_id=self.packing_list_1.id, item_id=self.item_1.id, quantity=5, is_checked=True)
    item_list_1.insert()
    item_list_2 = ItemLists(packing_list_id=self.packing_list_1.id, item_id=self.item_2.id, quantity=6, is_checked=False)
    item_list_2.insert()

    custom_item_1 = CustomItem(item="toy car", quantity=1, is_checked=False, category="toy",  packing_list_id=self.packing_list_1.id)
    custom_item_1.insert()

    custom_item_2 = CustomItem(item="car", quantity=1, is_checked=False, category="transportaion",  packing_list_id=self.packing_list_1.id)
    custom_item_2.insert()

    self.payload = {
        "data": {
            "item": {
                "id": custom_item_1.id,
                "category": "toy"
            }
        }
    }   

  def tearDown(self):
    db.session.remove()
    db_drop_everything(db)
    self.app_context.pop()


  def test_custom_item_can_be_deleted(self):
    payload = deepcopy(self.payload)

    #Assertions before delete
    all_item_lists = db.session.query(ItemLists).all()
    self.assertEqual(2, len(all_item_lists))

    all_custom_items = db.session.query(CustomItem).all()
    self.assertEqual(2, len(all_custom_items))

    #Calling route
    response = self.client.delete(
      '/api/v1/item_list/update', json=(payload),
      content_type='application/json'
    )

    #Assertions after delete
    self.assertEqual(200, response.status_code)
    data = json.loads(response.data.decode('utf-8'))
    success = "Packing list item has been deleted"

    self.assertEqual(success, data["success"])

    all_item_lists = db.session.query(ItemLists).all()
    self.assertEqual(2, len(all_item_lists))

    all_custom_items = db.session.query(CustomItem).all()
    self.assertEqual(1, len(all_custom_items))

  def test_error_message_if_packing_list_does_not_exists(self):
    payload = deepcopy(self.payload)

    # Fist call to delete the item list
    response = self.client.delete(
        '/api/v1/item_list/update', json=(payload),
        content_type='application/json'
    )

    self.assertEqual(200, response.status_code)

    # Second call trying to delete what is not there anymore
    response = self.client.delete(
        '/api/v1/item_list/update', json=(payload),
        content_type='application/json'
    )
    self.assertEqual(200, response.status_code)
    
    data = json.loads(response.data.decode('utf-8'))
    error = "Packing list item does not exists"
  
    self.assertEqual(error, data['error'])