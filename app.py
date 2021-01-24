import os
import ctypes
import json
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
        questions = mongo.db.questions.find().sort("added_on", -1)
    if sort == "latest":
        questions = mongo.db.questions.find().sort("added_on", 1)
    if sort == "names":
        questions = mongo.db.questions.find().sort("created_by", 1)        
    
    return render_template("questions.html", questions=questions)


@app.route("/filter_name", methods=["GET", "POST"])
def filter_name():
    names = session["user"]
    questions = mongo.db.questions.find(
        {"created_by": session["user"]})
    return render_template("filter_name.html", questions=questions)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    questions = mongo.db.questions.find({"$text": {"$search": query}})     
    return render_template("questions.html", questions=questions)


@app.route("/search_profiles", methods=["GET", "POST"])
def search_profiles():
    search_profiles = request.form.get("search_profiles")
    profiles = mongo.db.users.find({"$text": {"$search": search_profiles}})
    return render_template("search_profiles.html", profiles=profiles)


@app.route("/view_profile/<profile>", methods=["GET", "POST"])
def view_profile(profile):
    user_profile = mongo.db.users.find_one({"username": profile})
    username = user_profile["username"]

    return render_template("view_profile.html", username=username, profile=user_profile)


@app.route("/add_friend/<profile>", methods=["GET", "POST"])
def add_friend(profile):
    user_profile = mongo.db.users.find_one({"username": profile})
    username = user_profile["username"]
    pending_request = mongo.db.friend_requests.find_one({'$or':
    [
        {'$and':[{"friend_request_from": session["user"]},
        {"friend_request_to": username}]},
        {'$and':[{"friend_request_from": username},
        {"friend_request_to": session["user"]}]}        
    ]})
    already_friends = mongo.db.friends.find_one({'$or':
    [
        {'$and':[{"is_friends_1": session["user"]},
        {"is_friends_2": username}]},
        {'$and':[{"is_friends_1": username},
        {"is_friends_2": session["user"]}]}
    ]})
    if request.method == "POST":
        #check if the user is already friends or has a friend request pending
        if pending_request:
            flash("Friend request pending")
            return render_template("view_profile.html", username=username, profile=user_profile)
        if already_friends:
            flash("You're already friends!")
            return render_template("view_profile.html", username=username, profile=user_profile) 
        #if no friend request pending, then new friend request is posted    
        friend_request = {
            "friend_request_from": session["user"],
            "friend_request_to": username
        }
        mongo.db.friend_requests.insert_one(friend_request)
        flash("Friend request sent")
        return render_template("view_profile.html", username=username, profile=user_profile)
        

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
            "state": request.form.get("state"),
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
    user = session["user"] or None
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    user_profile = mongo.db.users.find_one({"username": user})
    friend_request = mongo.db.friend_requests.find_one({"friend_request_to": user})
    if session["user"]:
        return render_template("profile.html", username=username, profile=user_profile, 
        friend_request=friend_request)

    return redirect(url_for("login"))


@app.route("/friend_requests/<user>", methods=["GET", "POST"])        
def friend_requests(user):
    user = session["user"]
    find_request = mongo.db.friend_requests.find({"friend_request_to": user})
    if request.method == "POST":
        accept_friend = request.form.get("accept")
        decline_friend = request.form.get("decline")
        if accept_friend:
            friendship = {
                "is_friends_1": accept_friend,
                "is_friends_2": user
            }
            request_accepted = {
                "friend_request_from": accept_friend,
                "friend_request_to": user
            }
            mongo.db.friend_requests.remove(request_accepted)
            mongo.db.friends.insert_one(friendship)
            flash("Friend request accepted")
            
        else:
            request_declined = {
                "friend_request_from": decline_friend,
                "friend_request_to": user
            }
            mongo.db.friend_requests.remove(request_declined)
            flash("Friend request declined")

    return render_template("friend_requests.html", find_request=find_request)



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
    session = {}
    user = session.get("user", None)
    created_byId = mongo.db.questions.find_one({"_id" : ObjectId(question_id)})
    created_by = created_byId["created_by"]
    if user == created_by:
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
    else:
        return redirect(url_for("get_questions"))
    
    question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    return render_template("edit_question.html", question=question)


@app.route("/edit_profile/", methods=["GET", "POST"])
def edit_profile():
    with open('countries.json', encoding="utf8") as f:
               country = json.load(f)

    user = session["user"] or None
    if user: 
        user_profile = mongo.db.users.find_one({"username": user})
        users_id = user_profile["_id"]

        if request.method == "POST":
            sex = request.form['sex']
            submit = {
                "$set": {
                    "fname": request.form.get("fname"),
                    "lname": request.form.get("lname"),
                    "sex": sex,
                    "state": request.form.get("state"),
                    "country": request.form.get("country"),
                    "bday": request.form.get("bday")
                }
            }

            mongo.db.users.update_one({"_id": ObjectId(users_id)}, submit)
            flash("Profile Successfully Edited")
            user_profile = mongo.db.users.find_one({"_id": ObjectId(users_id)})
            return render_template("edit_profile.html", profile=user_profile, countries=country)
    
        else:
            return render_template("edit_profile.html", profile=user_profile, countries=country)
        
    return redirect(url_for("login"))


@app.route("/delete_question/<question_id>", methods=["GET", "POST"])
def delete_question(question_id):
    session = {}
    user = session.get("user", None)
    created_byId = mongo.db.questions.find_one({"_id" : ObjectId(question_id)})
    created_by = created_byId["created_by"]
    if user == created_by:
        if request.method == "POST":
            mongo.db.questions.remove({"_id": ObjectId(question_id)})
            flash("Question Successfully Deleted")
    else:
        return redirect(url_for("get_questions"))
        
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
