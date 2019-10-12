from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()
teas = db.teas


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
		"tea_name": request.form.get("tea_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
        "flavor": request.form.get("flavor")
	}
	tea_id = teas.insert_one(tea).inserted_id
	print(tea_id)
	return redirect(url_for("teas_show", tea_id = tea_id))

@app.route("/teas/<tea_id>")
def teas_show(tea_id):
	tea = teas.find_one({'_id' : ObjectId(tea_id)})
	return render_template("teas_show.html", tea = tea)

@app.route("/teas/new")
def teas_new():
	return render_template("teas_new.html", tea ={}, title ="New tea")

@app.route("/teas/<tea_id>/edit")
def teas_edit(tea_id):
	tea = teas.find_one({"_id" : ObjectId(tea_id)})
	return render_template("teas_edit.html", tea = tea, title = "Edit tea")

@app.route("/teas/<tea_id>", methods = ['POST'])
def teas_update(tea_id):
	updated_tea = {
		"tea_name": request.form.get("tea_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
        "flavor": request.form.get("flavor")

	}

	teas.update_one( {"_id" : ObjectId(tea_id)}, {"$set" : updated_tea})
	return redirect(url_for("teas_show", tea_id = tea_id))


@app.route("/teas/<tea_id>/delete", methods=["POST"])
def teas_delete(tea_id):
	teas.delete_one({"_id" : ObjectId(tea_id)})
	return redirect(url_for("teas_index"))


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
