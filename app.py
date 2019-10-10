from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Mondale')
client = MongoClient(host=host)
db = client.get_default_database()
mugs = db.mugs
# users = db.users

app = Flask(__name__)

# @app.route("/login")
# def login:
# 	auth = request.authorization
# 	return ""

@app.route("/")
def teas_index():
	# It's going to show the types of tea we have
	return render_template("teas_index.html", teas=teas.find())

@app.route("/teas", methods=["POST"])
def playlists_submit():
	tea = {
		"tea_flavor": request.form.get("tea_flavor"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),


	}
	tea_id = teas.insert_one(tea).inserted_id
	print(tea_id)
	return redirect(url_for("teas_show", tea_id = tea_id))
