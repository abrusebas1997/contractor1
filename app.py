from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

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
def mugs_index():
	# Shows all mugs
	return render_template("mugs_index.html", mugs=mugs.find())

@app.route("/mugs", methods=["POST"])
def playlists_submit():
	mug = {
		"mug_name": request.form.get("mug_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
		"color": request.form.get("color")

	}
	mug_id = mugs.insert_one(mug).inserted_id
	print(mug_id)
	return redirect(url_for("mugs_show", mug_id = mug_id))


@app.route("/mugs/<mug_id>")
def mugs_show(mug_id):
	mug = mugs.find_one({'_id' : ObjectId(mug_id)})
	return render_template("mugs_show.html", mug = mug)

@app.route("/mugs/new")
def mugs_new():
	return render_template("mugs_new.html", mug ={}, title ="New Mug")

@app.route("/mugs/<mug_id>/edit")
def mugs_edit(mug_id):
	mug = mugs.find_one({"_id" : ObjectId(mug_id)})
	return render_template("mugs_edit.html", mug = mug, title = "Edit Mug")

@app.route("/mugs/<mug_id>", methods = ['POST'])
def mugs_update(mug_id):
	updated_mug = {
		"mug_name": request.form.get("mug_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
		"color": request.form.get("color")
	}

	mugs.update_one( {"_id" : ObjectId(mug_id)}, {"$set" : updated_mug})
	return redirect(url_for("mugs_show", mug_id = mug_id))


@app.route("/mugs/<mug_id>/delete", methods=["POST"])
def mugs_delete(mug_id):
	mugs.delete_one({"_id" : ObjectId(mug_id)})
	return redirect(url_for("mugs_index"))


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
