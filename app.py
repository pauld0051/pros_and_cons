import os
import ctypes
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
if os.path.exists("env.py"):
    import env


app = Flask (__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_questions")
def get_questions():
    questions = mongo.db.questions.find().sort("added_on", -1)
    return render_template("questions.html", questions=questions)


@app.route("/filters", methods=["GET", "POST"])
def filters():
    sort = request.form.get("sort", "latest")
    if sort == "oldest":
        questions = mongo.db.questions.find().sort("added_on", 1)
    if sort == "latest":
        questions = mongo.db.questions.find().sort("added_on", -1)
    if sort == "names":
        questions = mongo.db.questions.find().sort("created_by", 1)        
    
    return render_template("questions.html", questions=questions)


@app.route("/filter_name", methods=["GET", "POST"])
def filter_name():
    names = session["user"]
    questions = mongo.db.questions.find(
        {"created_by": session["user"]})
    return render_template("filter_name.html", questions=questions)


@app.route("/filters_name", methods=["GET", "POST"])
def filters_name():
    sort = request.form.get("sort", "latest")
    if sort == "oldest":
        questions = mongo.db.questions.find({"created_by": session["user"]}).sort("added_on", 1)
    if sort == "latest":
        questions = mongo.db.questions.find({"created_by": session["user"]}).sort("added_on", -1)
    if sort == "names":
        questions = mongo.db.questions.find({"created_by": session["user"]}).sort("created_by", 1)        
    
    return render_template("filter_name.html", questions=questions)



@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    questions = mongo.db.questions.find({"$text": {"$search": query}})     
    return render_template("questions.html", questions=questions)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "fname": request.form.get("fname"),
            "lname": request.form.get("lname"),
            "bday": request.form.get("bday"),
            "city": request.form.get("city"),
            "country": request.form.get("country"),
            "sex": request.form.get("sex"),

        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        is_friends = "on" if request.form.get("is_friends") else "off"
        question = {
            "question_title": request.form.get("question_title"),
            "question_text": request.form.get("question_text"),
            "is_friends": is_friends,
            "created_by": session["user"],
            "added_on": datetime.now().strftime("%d %b %Y %H:%M.%S")
        }

        mongo.db.questions.insert_one(question)
        flash("Question Successfully Added")
        return redirect(url_for("get_questions"))

    return render_template("add_question.html")


@app.route("/edit_question/<question_id>", methods=["GET", "POST"])
def edit_question(question_id):
    if request.method == "POST":
        is_friends = "on" if request.form.get("is_friends") else "off"
        submit = {
            "$set": {
                "question_title": request.form.get("question_title"),
                "question_text": request.form.get("question_text"),
                "is_friends": is_friends,
                "edited_on": datetime.now().strftime("%d %b %Y %H:%M.%S")
                }
        }    

        mongo.db.questions.update_one({"_id": ObjectId(question_id)}, submit)
        flash("Question Successfully Edited")

    question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    return render_template("edit_question.html", question=question)


@app.route("/edit_profile")
def edit_profile():
   
    return render_template("edit_profile.html")





@app.route("/delete_question/<question_id>")
def delete_question(question_id):
    mongo.db.questions.remove({"_id": ObjectId(question_id)})
    flash("Question Successfully Deleted")
    return redirect(url_for("get_questions"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
