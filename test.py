from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_tea_id = ObjectId("5d55cffc4a3d4031f42827a3")

sample_tea = {
	"tea_flavor" : "flavors",
	"description" : "This is a totally organic tea",
	"price": "4",
}

sample_form_data = {

    "tea_flavor" : sample_tea['tea_flavor'],
	"description" : sample_tea["description"],
	"price": sample_tea["price"]
}

class TeasTests(TestCase):
	def setUp(self):
		self.client = app.test_client()

		app.config["TESTING"] = True

	# def test_index(self):
	# 	result = self.client.get('/')
	# 	self.assertEqual(result.status, "200 OK")
	# 	self.assertIn(b'tea', result.data)

	def test_new(self):
		result = self.client.get("teas/new")
		self.assertEqual(result.status, "200 OK")
		self.assertIn(b"New tea", result.data)

	@mock.patch("pymongo.collection.Collection.find_one")
	def test_show_tea(self, mock_find):
		mock_find.return_value = sample_tea

		result = self.client.get(f"/teas/{sample_tea_id}")
		self.assertEqual(result.status, "200 OK")
		self.assertIn(b"Test tea", result.data)

	@mock.patch("pymongo.collection.Collection.find_one")
	def test_edit_tea(self, mock_find):
		mock_find.return_value = sample_tea

		result = self.client.get(f"/teas/{sample_tea_id}/edit")
		self.assertEqual(result.status, "200 OK")
		self.assertIn(b"Test tea", result.data)

	@mock.patch("pymongo.collection.Collection.insert_one")
	def test_submit_tea(self, mock_insert):

		result = self.client.post("/teas", data = sample_form_data)

		self.assertEqual(result.status, "302 FOUND")
		mock_insert.assert_called_with(sample_tea)

	@mock.patch("pymongo.collection.Collection.update_one")
	def test_update_tea(self, mock_update):
		result = self.client.post(f'/teas/{sample_tea_id}' , data = sample_form_data)

		self.assertEqual(result.status, "302 FOUND")
		mock_update.assert_called_with({"_id" : sample_tea_id}, {"$set": sample_tea})

	@mock.patch("pymongo.collection.Collection.delete_one")
	def test_delete_tea(self, mock_delete):
		form_data = {"_method": "DELETE"}
		result = self.client.post(f"/teas/{sample_tea_id}/delete", data = form_data)
		self.assertEqual(result.status, "302 FOUND")
		mock_delete.assert_called_with({"_id" : sample_tea_id})



if __name__ == '__main__':
    unittest_main()
