import os
import ctypes
import json
import re
import random
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
if os.path.exists("env.py"):
    import env

#------------------#
# Validation rules #
#----------------- #

def validate_name(username):
    # Validates usernames.
    # Only allow letters, hyphens and underscores. No spaces.
    return re.match("^[a-zA-Z0-9-_]{5,15}$", username)


def validate_question(question):
    # Validates question titles
    # Only allow printable characters and spaces but not mathematical operators. Up to 255 characters.
    # Allow the "-" sign as the only mathematical operator
    return re.match(r"^[^+\*/><]{5,255}$", question)


def validate_question_text(question_text):
    # Validates question text
    # Only allow printable characters and spaces but not mathematical operators. Up to 1020 characters.
    # Allow the "-" sign as the only mathematical operator
    return re.match(r"^[^+\*/><]{5,1020}$", question_text)


app = Flask (__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

#---------- Home ----------#

@app.route("/")
@app.route("/get_questions")
def get_questions():
    admin = "9dyhnxe8u4"
    questions = list(mongo.db.questions.find().sort("_id", -1))
    created_by = [created_by['created_by'] for created_by in questions]
    is_friends = [is_friends['is_friends'] for is_friends in questions]
    # Find a random "question of the day" to head the home page
    q_o_t_d = []
    for qs in questions:
        q_o_t_d.append(qs["_id"])
    random_q = random.choice(q_o_t_d)
    lead_question = mongo.db.questions.find_one({"_id": random_q})
    what_is_friend = lead_question["is_friends"]
    if lead_question["is_friends"] == "on":
        return get_questions()       

    if "user" in session:
        profile = mongo.db.users.find_one({"username": session["user"]}) # Get the session user for _id matching
        profile_friends = profile["friends"] # Get the list of ObjectId from the friends array under the session user's profile
        friends = mongo.db.users.find({"_id": {"$in": profile_friends}}) # Insert each ObjectId to get the friend's user profile
        friend_list = [friend['username'] for friend in friends] # For each of the ObjectId find the username associated
        matched = [matched for matched in created_by if matched in friend_list] # Look to see if any friends match to the created_by list
        matched = list(dict.fromkeys(matched)) # Remove duplicates from the list
     
        return render_template("questions.html", questions=questions, admin=admin, matched=matched, q_o_t_d=lead_question)

    else: # If user is not logged in then no need to match for friendships
        return render_template("questions.html", questions=questions, admin=admin, q_o_t_d=lead_question)


#---------- Login ----------#

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # see if user wants to be permanently logged in
        permanent = request.form.get("remember")
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                session.permanent = permanent
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


#----------------------------------------#
# CRUD | Create | Read | Update | Delete #
#----------------------------------------#

#---------- Create ----------#

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # check to see if user wants to be permanently logged in on registration
        permanent = request.form.get("remember")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        session["non_registered_user"] = request.form.get("username").lower()
        if request.form.get("username") == "" or not validate_name(
           request.form.get("username").lower()):
            flash("Use only letters, numbers, dashes and underscores")
            return redirect(url_for("register", store_user=session["non_registered_user"]))
        if password == confirm:     
            register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password")),
                "fname": request.form.get("fname"),
                "lname": request.form.get("lname"),
                "bday": request.form.get("bday"),
                "state": request.form.get("state"),
                "country": request.form.get("country"),
                "sex": request.form.get("sex"),
                "friends": []
            }
            mongo.db.users.insert_one(register)

            # put the new user into 'session' cookie
            session["user"] = request.form.get("username").lower()
            session.permanent = permanent
            flash("Registration Successful!")
            return redirect(url_for("profile", username=session["user"]))
    
        else:
            session["non_registered_user"] = request.form.get("username").lower()
            flash("Passwords don't match, try again.")
            
            return render_template("register.html", store_user=session["non_registered_user"])

    return render_template("register.html")


@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    replies = 0
    if request.method == "POST":
        title = request.form.get("question_title") 
        textarea = request.form.get("question_text")
        # Check to see if the title and text comply with the regex
        if request.form.get("question_title") == "" or not validate_question(
           request.form.get("question_title")):
           flash("Use only printable letters and numbers. Mathematical operators are not possible.")
           return render_template("add_question.html", title=title, text=textarea)
        if request.form.get("question_text") == "" or not validate_question_text(
            request.form.get("question_text")):
            flash("Use only printable letters.")
            return render_template("add_question.html", title=title, text=textarea)
        is_friends = "on" if request.form.get("is_friends") else "off"
        question = {
            "question_title": request.form.get("question_title"),
            "question_text": request.form.get("question_text"),
            "is_friends": is_friends,
            "created_by": session["user"],
            "added_on": datetime.now().strftime("%d %b %Y %H:%M.%S"),
            "pros": [],
            "cons": [],
            "replies": replies
        }
        mongo.db.questions.insert_one(question)
        flash("Question Successfully Added")
        return redirect(url_for("get_questions"))

    return render_template("add_question.html")


@app.route("/cons/<question_id>", methods=["POST"])
def cons(question_id):
    admin = "9dyhnxe8u4"
    user = session["user"] or None
    questions = list(mongo.db.questions.find().sort("added_on", -1))
    question_here = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    created_by = question_here["created_by"]
    if "user" in session:
        profile = mongo.db.users.find_one({"username": session["user"]}) # Get the session user for _id matching
        profile_friends = profile["friends"] # Get the list of ObjectId from the friends array under the session user's profile
        friends = mongo.db.users.find({"_id": {"$in": profile_friends}}) # Insert each ObjectId to get the friend's user profile
        friend_list = [friend['username'] for friend in friends] # For each of the ObjectId find the username associated
        matched = [x for x in friend_list if x == created_by] # Look to see if any friends match to the created_by list
        matched = list(dict.fromkeys(matched)) # Remove duplicates from the list

    if request.method == "POST":
        # Check to see if the title and text comply with the regex
        if request.form.get("con") == "" or not validate_question(
           request.form.get("con")):
           bad_con = request.form.get("con")
           flash("Sorry, you can't use mathematical operators here.")
           return render_template("view_question.html", bad_con=bad_con, question=question_here, matched=matched, admin=admin)

        con = {
                "con": request.form.get("con"),
                "user": user 
            }
        find_one_q = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
        replies = len(find_one_q['pros']) + len(find_one_q['cons']) + 1

        mongo.db.questions.update_one({"_id": ObjectId(question_id)},{"$push":{"cons": con}})
        mongo.db.questions.update_one({"_id": ObjectId(question_id)},{"$set":{"replies": replies}})        

    return redirect(url_for("view_question", question_id=question_id))


@app.route("/pros/<question_id>", methods=["POST"])
def pros(question_id):
    admin = "9dyhnxe8u4"
    user = session["user"] or None
    questions = list(mongo.db.questions.find().sort("added_on", -1))
    question_here = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    created_by = question_here["created_by"]
    if "user" in session:
        profile = mongo.db.users.find_one({"username": session["user"]}) # Get the session user for _id matching
        profile_friends = profile["friends"] # Get the list of ObjectId from the friends array under the session user's profile
        friends = mongo.db.users.find({"_id": {"$in": profile_friends}}) # Insert each ObjectId to get the friend's user profile
        friend_list = [friend['username'] for friend in friends] # For each of the ObjectId find the username associated
        matched = [x for x in friend_list if x == created_by] # Look to see if any friends match to the created_by list
        matched = list(dict.fromkeys(matched)) # Remove duplicates from the list

    if request.method == "POST":
        # Check to see if the title and text comply with the regex
        if request.form.get("pro") == "" or not validate_question(
           request.form.get("pro")):
           bad_pro = request.form.get("pro")
           flash("Sorry, you can't use mathematical operators here.")
           return render_template("view_question.html", bad_pro=bad_pro, question=question_here, matched=matched, admin=admin)
   
    if request.method == "POST":
        pro = {
                "pro": request.form.get("pro"),
                "user": user 
            }
        find_one_q = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
        replies = len(find_one_q['pros']) + len(find_one_q['cons']) + 1

        mongo.db.questions.update_one({"_id": ObjectId(question_id)},{"$push":{"pros": pro}})
        mongo.db.questions.update_one({"_id": ObjectId(question_id)},{"$set":{"replies": replies}})

    return redirect(url_for("view_question", question_id=question_id))


@app.route("/add_friend/<profile>", methods=["GET", "POST"])
def add_friend(profile):
    user_profile = mongo.db.users.find_one({"username": profile})
    username = user_profile["username"]
    logged_in_user = session["user"]
    pending_request = mongo.db.friend_requests.find_one({'$or':
    [
        {'$and':[{"friend_request_from": logged_in_user},
        {"friend_request_to": username}]},
        {'$and':[{"friend_request_from": username},
        {"friend_request_to": logged_in_user}]}        
    ]})
    already_friends = mongo.db.friends.find_one({'$or':
    [
        {'$and':[{"is_friends_1": logged_in_user},
        {"is_friends_2": username}]},
        {'$and':[{"is_friends_1": username},
        {"is_friends_2": logged_in_user}]}
    ]})
    if request.method == "POST":
        #check if the user is already friends or has a friend request pending
        if pending_request:
            flash("Friend request pending")
            return render_template("view_profile.html", profile=username, 
            is_friends=already_friends, pending_request=pending_request)
        if already_friends:
            flash("You're already friends!")
            return render_template("view_profile.html", profile=username, 
            is_friends=already_friends, pending_request=pending_request) 
        #if no friend request pending, then new friend request is posted    
        friend_request = {
            "friend_request_from": session["user"],
            "friend_request_to": username
        }
        mongo.db.friend_requests.insert_one(friend_request)
        flash("Friend request sent")
        return redirect(url_for("view_profile", profile=username, 
            is_friends=already_friends, pending_request=pending_request))


#---------- Read ----------#

@app.route("/view_question/<question_id>")
def view_question(question_id):
    questions = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
    admin = "9dyhnxe8u4"
    created_by = questions["created_by"]
    if "user" in session:
        profile = mongo.db.users.find_one({"username": session["user"]}) # Get the session user for _id matching
        profile_friends = profile["friends"] # Get the list of ObjectId from the friends array under the session user's profile
        friends = mongo.db.users.find({"_id": {"$in": profile_friends}}) # Insert each ObjectId to get the friend's user profile
        friend_list = [friend['username'] for friend in friends] # For each of the ObjectId find the username associated
        matched = [x for x in friend_list if x == created_by] # Look to see if any friends match to the created_by list
        matched = list(dict.fromkeys(matched)) # Remove duplicates from the list

        return render_template("view_question.html", question=questions, matched=matched, admin=admin)
    else:
        matched = []
        return render_template("view_question.html", question=questions, matched=matched, admin=admin)


#---------- Search and Filters ----------#

@app.route("/filters", methods=["GET", "POST"])
def filters():
    sort = request.form.get("sort", "latest")
    admin = "9dyhnxe8u4"
    questions = list(mongo.db.questions.find().sort("_id", -1))
    created_by = [created_by['created_by'] for created_by in questions]
    # Find the question of the day - a random open question that appears at the top of the list, changes on refresh
    q_o_t_d = []
    for qs in questions:
        q_o_t_d.append(qs["_id"])
    random_q = random.choice(q_o_t_d)
    lead_question = mongo.db.questions.find_one({"_id": random_q})
    what_is_friend = lead_question["is_friends"] # Avoid questions that have "is_friends" set to "on"
    if lead_question["is_friends"] == "on" and lead_question["created_by"] != session["user"]:
        return filters()       

    if "user" in session:
        user = session["user"] or None
        user_profile = mongo.db.users.find_one({"username": user})
        profile_friends = user_profile["friends"]
        friends = mongo.db.users.find({"_id": {"$in": profile_friends}})
        friend_list = [friend['username'] for friend in friends] # For each of the ObjectId find the username associated
        matched = [matched for matched in created_by if matched in friend_list] # Look to see if any friends match to the created_by list
        matched = list(dict.fromkeys(matched)) # Remove duplicates from the list
    
    # Sort depending on user request
    if request.method == "POST":
        if "user" not in session:
            matched = []    
        if sort == "oldest":
            questions = list(mongo.db.questions.find().sort("_id", 1))
        if sort == "latest":
            questions = list(mongo.db.questions.find().sort("added_on", -1))
        if sort == "names":
            questions = list(mongo.db.questions.find().sort("created_by", 1))
        if sort == "friends":
            questions = list(mongo.db.questions.find({"created_by": {"$in": friend_list}}).sort("added_on", -1))
        if sort == "popular":
            questions = list(mongo.db.questions.find().sort("replies", -1))
        if sort == "unanswered":
            questions = list(mongo.db.questions.find().sort("replies", 1))
       
    return render_template("questions.html", questions=questions, matched=matched, admin=admin, q_o_t_d=lead_question)


@app.route("/filter_name", methods=["GET", "POST"])
def filter_name():
    user = session["user"] or None
    sort = request.form.get("sort", "latest")
    questions = list(mongo.db.questions.find({"created_by": user}))
    if len(questions) > 0:
        q_o_t_d = []
        for qs in questions:
            q_o_t_d.append(qs["_id"])
        random_q = random.choice(q_o_t_d)
        lead_question = mongo.db.questions.find_one({"_id": random_q})
        what_is_friend = lead_question["is_friends"]
    else:
        questions = list(mongo.db.questions.find())
        q_o_t_d = []
        for qs in questions:
            q_o_t_d.append(qs["_id"])
        random_q = random.choice(q_o_t_d)
        lead_question = mongo.db.questions.find_one({"_id": random_q})
        what_is_friend = lead_question["is_friends"]
    if lead_question["is_friends"] == "on" and lead_question["created_by"] != session["user"]:
        return filter_name()
    if len(questions) < 1:
        questions = ""
        flash("You have none of your own questions yet, consider starting one.")       
        return render_template(filter_name.html, questions=questions, q_o_t_d=lead_question)
    if request.method == "POST":     
        if sort == "oldest":
            questions = list(mongo.db.questions.find({"created_by": user}).sort("_id", 1))
        if sort == "latest":
            questions = list(mongo.db.questions.find({"created_by": user}).sort("added_on", -1))
        if sort == "popular":
            questions = list(mongo.db.questions.find({"created_by": user}).sort("replies", -1))
        if sort == "unanswered":
            questions = list(mongo.db.questions.find({"created_by": user}).sort("replies", 1))

    return render_template("filter_name.html", questions=questions, q_o_t_d=lead_question)


@app.route("/search", methods=["GET", "POST"])
def search():
    admin = "9dyhnxe8u4"
    query = request.form.get("query")
    questions = list(mongo.db.questions.find({"$text": {"$search": query}}))
    created_by = [created_by['created_by'] for created_by in questions]
    is_friends = [is_friends['is_friends'] for is_friends in questions]

    if "user" in session:
        profile = mongo.db.users.find_one({"username": session["user"]}) # Get the session user for _id matching
        profile_friends = profile["friends"] # Get the list of ObjectId from the friends array under the session user's profile
        friends = mongo.db.users.find({"_id": {"$in": profile_friends}}) # Insert each ObjectId to get the friend's user profile
        friend_list = [friend['username'] for friend in friends] # For each of the ObjectId find the username associated
        matched = [matched for matched in created_by if matched in friend_list] # Look to see if any friends match to the created_by list
        matched = list(dict.fromkeys(matched)) # Remove duplicates from the list
     
        return render_template("search_questions.html", questions=questions, admin=admin, matched=matched)

    else: # If user is not logged in then no need to match for friendships
        return render_template("search_questions.html", questions=questions, admin=admin)


@app.route("/search_profiles", methods=["GET", "POST"])
def search_profiles():
    if "user" in session:
        user = session["user"] or None
        user_profile = mongo.db.users.find_one({"username": user})
        search_profiles = request.form.get("search_profiles")
        profiles = mongo.db.users.find({"$text": {"$search": search_profiles}})

        # Check if the logged in user is friends with any of the found profiles
        # Check all the profiles that are found against current friends
    
        searched_profiles = list(mongo.db.users.find({"$text": {"$search": search_profiles}}))
        profile_usernames = []
        
        for username in searched_profiles:
            profile_usernames.append(username["username"]) # Find a list of all the names that came up in the search
        profile_friends = user_profile["friends"] # Get the list of ObjectId from the friends array under the session user's profile
        friends = mongo.db.users.find({"_id": {"$in": profile_friends}}) # Insert each ObjectId to get the friend's user profile
        friend_list = [friend['username'] for friend in friends] # For each of the ObjectId find the username associated
        matched = [matched for matched in profile_usernames if matched in friend_list] # Look to see if any friends match to the created_by list
        matched = list(dict.fromkeys(matched)) # Remove duplicates from the list
        # Check if there is a pending friends request from the logged in user (display pause)
        from_user = list(mongo.db.friend_requests.find({"friend_request_from": user_profile["username"]})) 
        request_from = []
        for profile in from_user:
            request_from.append(profile["friend_request_to"]) # For each request to a profile
        requested = [requested for requested in profile_usernames if requested in request_from]
        # Check if there is a pending friends request from the found profiles (allow accept or decline)
        to_user = list(mongo.db.friend_requests.find({"friend_request_to": user_profile["username"]}))
        request_to = []
        for profile in to_user:
            request_to.append(profile["friend_request_from"]) # For each request from a profile
        requested_to = [requested_to for requested_to in profile_usernames if requested_to in request_to]
        # For everything else allow logged in user to send a friend request
        result_list = []
        send_request = False # Default state
        for one_profile in profile_usernames:
            if (one_profile in matched) or (one_profile in requested) or (one_profile in requested_to):
                result_list.append((one_profile,True))
            else:
                result_list.append((one_profile,False))

        return render_template("search_profiles.html", profiles=profiles, user=user_profile, friends=matched, 
        requested=requested, requested_to=requested_to, result_list=result_list)
    else:
        return redirect(url_for("login")) 


@app.route("/view_profile/<profile>", methods=["GET", "POST"])
def view_profile(profile):
    admin = "9dyhnxe8u4"
    user_profile = mongo.db.users.find_one({"username": profile})
    username = user_profile["username"]
    questions = list(mongo.db.questions.find(
        {"created_by": username}))
    if "user" not in session:
        return render_template("view_profile.html", profile=user_profile, questions=questions)
    current_user = mongo.db.users.find_one({"username": session["user"]})
    logged_in_user = current_user["username"]
    if logged_in_user != user_profile["username"]:
        # If user is logged in, they can add friends etc
        # check to see if users are already friends with this profile
        already_friends = mongo.db.friends.find_one({'$or':
        [
            {'$and':[{"is_friends_1": current_user["username"]},
            {"is_friends_2": username}]},
            {'$and':[{"is_friends_1": username},
            {"is_friends_2": current_user["username"]}]}
        ]})
        # check to see if user has sent a friend request to this profile
        pending_request = mongo.db.friend_requests.find_one({'$or':
        [
            {'$and':[{"friend_request_from": current_user["username"]},
            {"friend_request_to": username}]},
            {'$and':[{"friend_request_from": username},
            {"friend_request_to": current_user["username"]}]}        
        ]})
        # Check to see if logged in user is trying to "view" their profile and redirect them to "profile"
        return render_template("view_profile.html", profile=user_profile, 
        friends=already_friends, pending_request=pending_request, user=current_user["username"], 
        questions=questions, admin=admin, user_id=current_user)
    #  If user is logged in, they get to see their own profile   
    else:
        return redirect(url_for("profile", username=logged_in_user))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    admin = "9dyhnxe8u4"
    # Get questions that the user has input themselves
    questions = mongo.db.questions.find(
        {"created_by": session["user"]})
    user = session["user"] or None
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    user_profile = mongo.db.users.find_one({"username": user})
    friend_request = mongo.db.friend_requests.find_one({"friend_request_to": user})
    
    if session["user"] == admin:
        messages = mongo.db.messages.find()
        return render_template("profile.html", username=username, profile=user_profile, 
        friend_request=friend_request, questions=questions, admin=admin, messages=messages)
    
    if session["user"]:
        messages = None
        return render_template("profile.html", username=username, profile=user_profile, 
        friend_request=friend_request, questions=questions, admin=admin, messages=messages)

    return redirect(url_for("login"))


#---------- Update ----------#

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


@app.route("/friend_requests/<user>/<action>", methods=["GET", "POST"])        
def friend_requests(user, action):
    if user:
        logged_in_user = mongo.db.users.find_one({"_id": ObjectId(user)})
        logged_user = logged_in_user["username"]
        requested_from = []
        # fetch all requests for current user
        requests = list(mongo.db.friend_requests.find({"friend_request_to": logged_user}))
        # project list of requestors profiles 
        requests_from = list(map(lambda x: x['friend_request_from'], requests))
        # fetch all requestors profiles
        profiles = mongo.db.users.find({"username": {"$in":requests_from}})
        # transform list of requestors profiles into dict
        requestors = {profile['username']: profile for profile in profiles}
        
        if request.method == "POST":
            if action == 'accept_friend':
                user_name = mongo.db.users.find_one({"username": session["user"]})
                user_id = user_name["_id"] 
                accept_friend = request.form.get("accept")
                requestors_user = mongo.db.users.find_one({"username": accept_friend})
                requestors_id = requestors_user["_id"]                
                friendship = {
                    "is_friends_1": accept_friend,
                    "is_friends_2": logged_user
                }
                request_accepted = {
                    "friend_request_from": accept_friend,
                    "friend_request_to": logged_user
                }
                mongo.db.friend_requests.delete_one(request_accepted)
                mongo.db.friends.insert_one(friendship)
                mongo.db.users.find_one_and_update({"_id": user_id},
                    {"$push": {"friends": requestors_id}})
                mongo.db.users.find_one_and_update({"_id": requestors_id},
                    {"$push": {"friends": user_id}})
                flash("Friend request accepted")
                
                return redirect(url_for("friend_requests", user=user_id, action=action))
            
            if action == 'decline_friend':
                user_name = mongo.db.users.find_one({"username": session["user"]})
                user_id = user_name["_id"] 
                decline_friend = request.form.get("decline")
                request_declined = {
                    "friend_request_from": decline_friend,
                    "friend_request_to": logged_user
                }
                mongo.db.friend_requests.delete_one(request_declined)
                flash("Friend request declined")
                return redirect(url_for("friend_requests", user=user_id, action=action))
    
        return render_template("friend_requests.html", requests=requests, requestors=requestors, 
        logged_in=logged_in_user, user=logged_user)

    return redirect(url_for("login"))


@app.route("/edit_question/<question_id>", methods=["GET", "POST"])
def edit_question(question_id):
    admin = "9dyhnxe8u4"
    user = session["user"] or None
    created_byId = mongo.db.questions.find_one({"_id" : ObjectId(question_id)})
    created_by = created_byId["created_by"]
    if user == created_by or user == admin:
        if request.method == "POST":
            if request.form.get("question_title") == "" or not validate_question(
            request.form.get("question_title")):
                question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
                flash("Use only printable letters and numbers. Mathematical operators are not possible.")
                return render_template("edit_question.html", question=question, admin=admin)
            if request.form.get("question_text") == "" or not validate_question_text(
                request.form.get("question_text")):
                question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
                flash("Use only printable letters.")
                return render_template("edit_question.html", question=question, admin=admin)

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
    return render_template("edit_question.html", question=question, admin=admin)


@app.route("/finish_question/<question_id>", methods=["GET", "POST"])
def finish_question(question_id):
    admin = "9dyhnxe8u4"
    user = session["user"] or None
    questions = list(mongo.db.questions.find().sort("added_on", -1))
    created_byId = mongo.db.questions.find_one({"_id" : ObjectId(question_id)})
    created_by = created_byId["created_by"]
    if user == created_by or user == admin:
        if request.method == "POST":
            finish = {
                "$set": {
                    "finished": request.form.get("finish")
                }
            }

        mongo.db.questions.update_one({"_id": ObjectId(question_id)},{"$set":{"finished": True}})
    return redirect(url_for("get_questions"))


#---------- Delete ----------#

@app.route("/remove_friend/<profile>", methods=["GET", "POST"])
def remove_friend(profile):
    user_profile = mongo.db.users.find_one({"username": profile}) # Find the profile of the user being looked at
    profile_id = user_profile["_id"] # Find the ID of the profile of the user being looked at
    username = user_profile["username"] # Find the username of the ID of the profile being looked at
    remove_friend_profile = mongo.db.users.find_one({"friends": ObjectId(profile_id)}) # Finds the profile of the logged in user
    friends_of_user = user_profile["friends"] # Find the list of friends of the profile being looked at
    logged_in_user = session["user"] # Name of the logged in user
    logged_in = mongo.db.users.find_one({"username": logged_in_user}) # Profile of the logged in user
    logged_id = logged_in["_id"] # ID of the logged in user
    friends_of_logged_in = logged_in["friends"] # List of friends of the logged in user
    remove_friend_user = mongo.db.users.find_one({"friends": ObjectId(logged_id)}) # Find the friend in the array with this ID
    # Find the friendship in the collection Friends
    already_friends = mongo.db.friends.find_one({'$or':
    [
        {'$and':[{"is_friends_1": logged_in_user}, # Logged in username
        {"is_friends_2": username}]}, # The profile being looked at
        {'$and':[{"is_friends_1": username}, # The inverse of the first statement
        {"is_friends_2": logged_in_user}]}
    ]})
        
    if request.method == "POST":
        mongo.db.users.find_one_and_update(
            {"_id": profile_id}, # The ID of the profile being looked at
            {"$pull": {"friends": logged_id}}) # Removes this friend (user that is logged in)
        mongo.db.users.find_one_and_update(
            {"_id": logged_id}, # The ID of the logged in user
            {"$pull": {"friends": profile_id}}) # Removes the profile that is being looked at
        mongo.db.friends.remove(already_friends)

    flash("Successfully removed friend")      
    return redirect(url_for("profile", username=logged_in_user))


@app.route("/delete_question/<question_id>", methods=["GET", "POST"])
def delete_question(question_id):
    admin = "9dyhnxe8u4"
    user = session["user"] or None
    created_byId = mongo.db.questions.find_one({"_id" : ObjectId(question_id)})
    created_by = created_byId["created_by"]
    if user == created_by or user == admin:
        if request.method == "POST":
            mongo.db.questions.delete_one({"_id": ObjectId(question_id)})
            flash("Question Successfully Deleted")
    else:
        return redirect(url_for("get_questions"))
        
    return redirect(url_for("get_questions"))


#---------- Help and Policies ----------#

@app.route("/help")
def help():

    return render_template("help.html")


@app.route("/send_message", methods=["GET", "POST"])
def send_message():
    if "user" in session: 
        if request.method == "POST":
            message = request.form["message"]
            submit = {
                "type": message,
                "message": request.form.get("message_text"),
                "username": session["user"]
            }

            mongo.db.messages.insert_one(submit)
            flash("Message Sent")

            return redirect(url_for("get_questions"))
    else:
        return redirect(url_for("login"))    

    return render_template("send_message.html")


@app.route("/policies/terms")
def terms():

    return render_template("policies/terms.html")


@app.route("/policies/privacy")
def privacy():

    return render_template("policies/privacy.html")


#---------- Logout ----------#

@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


#---------- Logout ----------#

@app.errorhandler(404)
def page_not_found(error):

    return render_template("error/page_not_found.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
