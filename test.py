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
