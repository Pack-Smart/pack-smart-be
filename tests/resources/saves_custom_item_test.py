import json
import unittest
from api.database.models import Users, PackingLists, CustomItem
import psycopg2
from api import create_app, db
from tests import db_drop_everything

class SaveCustomItemTest(unittest.TestCase):
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

  def test_it_saves_the_custom_item(self):
    user = Users(username='Jose')
    user.insert()

    packing_list = PackingLists(title='To Mars', user_id=user.id, num_of_days=6, destination="Mars")
    packing_list.insert()

    payload = {
        "data": {
            "type": "custom item",
            "attributes": {
                "item": "PS5",
                "quantity": 1,
                "category": "video games",
                "packing_list_id": packing_list.id
            }
        }
    }

    response = self.client.post(
      '/api/v1/custom_item/new', json=(payload),
      content_type='application/json'
    )

    self.assertEqual(200, response.status_code)

    data = json.loads(response.data.decode('utf-8'))

    item = db.session.query(CustomItem).first()
    
    self.assertEqual('Custom Item Saved!', data['message'])
    self.assertEqual(200, data['status_code'])
    self.assertEqual("PS5", item.item)
    self.assertEqual(1, item.quantity)
    self.assertEqual(False, item.is_checked)
    self.assertEqual("video games", item.category)
    self.assertEqual(1, item.packing_list_id)
