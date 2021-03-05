# Pros and Cons - A social media phenomena

[![Pros and Cons Logo](https://raw.githubusercontent.com/pauld0051/pros_and_cons/master/static/images/pros_and_cons_logo.png "Pros and Cons Logo")](https://pros-and-cons-1.herokuapp.com/)

Site: <https://pros-and-cons-1.herokuapp.com/>

## TESTING

## Manual Testing

Manual testing was done throughout the development process, as new features were implemented, to ensure of they worked as intended.

### Registration Page

The validation rules for the creation of an account were tested to ensure correct data was sent to the database. The following returned an error as expected:

- One of the fields missing
- Confirm password not matching password
- Username longer than 15 characters
- Password shorter than 5 characters
- Use of symbols and mathematical operators
- Username already registered for an existing account

If the fields validate, it was confirmed that an account is created.

If a user is already logged in, accessing the registration page redirects to the questions page.

### Login Page

To log into the application, a username attached to an existing user account must be entered, along with its associated password. If the username is not found in the database, or the password does not match, the login fails.

If the username exists and the password matches, the log in succeeds and the user session is created.

If a user is already logged in, accessing the login page redirects to the questions page.

### Questions Page

Non logged in users can view the questions page but can not access any of the controls, including submitting pros and cons to a question. If a user somehow forces a "pro" or a "con" a 405 error page is shown. Users can view a question collapsible, click the title to open the question, click on one of the usernames in either pros, cons or created by to view that user's profile. Users who are not logged in can not sort by "friends" and can not access the fliter_name.html page and are redirected to login.

Users that are currently in session are able to view questions and access controls such as:

- Post a pro or con to a question (opens the question in the browser)
- Sort questions, including "friends"
- Remove all questions that are not the user's
- Click "Finish", "Edit", "Delete" on their own posts (unless logged in as the administrator, then all posts have these buttons)
- If a user other than the post owner or administrator tries to force an "Finish", "Edit", or "Delete", the user is redirected to the questions page or login page if not logged in

### Profile Page

All users can view profile page, however, those that are not logged in can only view the profile and not see friendship associations. If a user who is not logged in tries to force a "friend request" accept or decline, they are redirected to the login page. Users who are logged in and try to "force" a friend request accept or decline are redirected to the questions page.

Users who are logged in and are the profile owner can view, accept and decline friend requests. Users who are logged in can edit their own profile too. Those who are not logged in are redirected to the login page. Because there is no specific "id" for editing a profile page, only the logged in user can edit their profile.

### Edit Profile

Only logged in users are able to edit their profile. Editing profiles produces only the profile of the user who is logged in.

Edits are rejected if:

- Names that are over 26 characters long
- Names, countries or states that contain mathematical symbols
- Birth dates that do not follow the format of %d %B, %Y

Note: Birth dates can be left blank or state "None".

The profile picture changes based on the user's choice of sex.

### Add Questions

Only users who have a current session are able to access the add question page. User's who are logged in are able to add a title and text and choose whether the question is friends only. However, a question will be rejected if:

- Contains mathematical operators
- A title longer than 255 characters
- Text longer than 1020 characters in the body of the question

### Adding a pro or a con to a question

Only logged in users are able to add a pro or a con. Users who are not logged in are unable to "force" a pro or a con.

Pros and cons have the same validation criteria. A pro or con will be rejected if:

- Contains mathematical operators
- Is longer than 255 characters

### Editing, Deleting and Finishing a question

Only logged in users who are the "created_by" session user or the administrator can edit, delete or finish any questions. Users who try to force and edit, delete or finish will be redirected to either the questions page or login if they are not currently logged in.

Editing questions follows the same rules as adding a question. Edits will be rejected if they:

- Contain mathematical operators
- Have a title longer than 255 characters
- Contain text longer than 1020 characters in the body of the question

### Adding a friendship

Users who are logged in are able to accept, decline and send friend requests. Users that try to force a friend request are redirected to the profile of the user they're sending the request to. Users that try to accept or decline friendships that they are not receiving (ie, have a url for an accept or decline friendship) are redirected back to the questions page. Only users who received the friendship request can act on them.

### Help Page

All users can view the help page, but only users who are logged in are able to send the administrator messages.

### Logout

The application successfully removes a user from the "session".

### Keep logged in

Users have the choice at registration or login to keep their "session" active. A user can then close their browser and reopen it at another time and still be logged in.

### 404 - page not found

A user, logged in, or otherwise, could try to enter their own URL, if this is not found, a 404 page is displayed.

### 403 - Forbidden

If a user attempts does something that is not able to be accepted into the database, a 403 page is displayed.

### 500 - Server Error

A 500 page is displayed if the server is not receiving requests at that time.

### 405 - Error

If a user attempts to force "add" a pro or con, a 405 error is displayed.

### Route by Route

Routes are tested in order they appear in the app.py file:

#### get_questions()

This is the first page that a user visiting the site might see, even if not logged in. Early issues that arose were key errors due to the session user not being a logged in user.

- Supplies the variable "admin" with the admin's unique username. If the admin is logged in, they can access all posts, add, delete, finish and edit all posts. Admin's can not edit profiles other than their own.
- Fetches all questions, checks who created the question and checks the user's friend list to deploy questions that are targeted only for friends.
- A random selector chooses any question that is not set to "friends only" to be featured at the top of the page below the search bar. If this random question has "friends" set to "on" then the process runs again until a post with that is open for public use can be found. There are plenty of posts that are open to the public that will always be found.
- Tests to see if a user is in session, and if so, tests against a list of friends to determine which posts can be seen by the logged in user. If a user is not logged in, this part is skipped and the questions that are displayed are only the open to the public questions.

This page was tested under all conditions - logged in users could see only open posts, users that are logged in but without friendships could only see open posts and finally, users with friendships and are logged in could see posts from friends. The admin user could see all posts regardless of status.

- Users that are logged in can not see the "finish", "edit" and "delete" buttons for posts they did not create.
- Users who had not logged in could not see the "finish", "edit" and "delete" buttons nor the add pro or cons submit buttons.
- All users were able to click on any post to open it in the tab.
- All users were able to click on any created by username to see their profile, this included all pros and cons.

#### login()

- Only users who were not in session could access the login page. A user that is logged in and attempts to access the login page is redirected to the get_questions page.
- If the login form is filled out and the user is not in session, a check of all users in the database to make sure the user exists. If the name exists, the route checks the password. Only if both exist and are correct will a user be able to login. If any field is wrong a message flashes: "Incorrect Username and/or Password"

The user of "Incorrect Username and/or Password" prevents hackers attempting to login under other people's usernames by continually attempting passwords. If the hacker is unaware if which field is incorrect, the hacker will not know if the username is correct and password wrong or vice versa.

#### register()

- If a user is in session they will be redirected to the questions page.
- If a user is not in session they need to complete the registration form before submitting. Any submission that does not meet the requirements will have an error message flashed up. Usernames that have been entered will remain. But passwords will need to be re-entered. All users are bound by the same validation rules:
  - One of the fields missing
  - Confirm password not matching password
  - Username longer than 15 characters
  - Password shorter than 5 characters
  - Use of symbols and mathematical operators
  - Username already registered for an existing account

#### add_question()

Only logged in users can access the add question page, if a user is not logged in and types the URL into a browser they are redirected to the login page.

If the user is in session then in order to submit the form, the user must have filled out all the fields appropriately. If a field is left blank, the frontend default browser provides the error and no submission can occur. The backend validation works even if the frontend does not. If the user uses a mathematical operator a message flashes up and the form is not submitted.

- The regex for both question title and text is: r"^[^\/\+\<\>\*]{5,255}$" with the only difference that the text is up to 1020 characters.
- The backend function: ```if request.form.get("question_text") == "" or not validate_funcs.validate_question_text(request.form.get("question_text")):``` checks if the form is blank or does not meet the criteria for a valid post.

#### pros() and cons()

Only logged in users are able to see the submission form for adding a pro or a con. However, if a user types the URL for a question they will get a 405 error page. Instructions on this page suggest the user logs in or uses the back button. To test this a current question's ID was added to this URL [http://pros-and-cons-1.herokuapp.com/pros/6040989f61e7e8310f344aa0](http://pros-and-cons-1.herokuapp.com/pros/6040989f61e7e8310f344aa0). This was tested both locally and on the deployed site at Heroku.

#### add_friend()

To add a friend a user must have first received a friend request. Two possibilities exist where a user logged in tries to force an add friend or a user not logged in attempts.

For example, if a user is logged in and is not friends with another user and just types a URL into the browser as follows: [http://pros-and-cons-1.herokuapp.com/add_friend/test3](http://pros-and-cons-1.herokuapp.com/add_friend/test3) this will return the user to the profile of the page they are trying to add as a friend. If a user is already a friend, this will still go directly to that friend's profile. If a user is not logged in, they will be redirected to the login page. If the user has a pending friend request that was sent to that user they will be redirected to the user's profile page. If a user has a pending friend request from the user the same occurs, they are redirected to their profile page. From there the user can either accept or decline the friend request.

To test this, set up four profiles:

- Profile_A
- Profile_B
- Profile_C
- Profile_D

From *Profile_A*, send a friend request to *Profile_B* and to *Profile_C*

From *Profile_B* - accept the friend request, these users are now friends. Now try to force the URL from *Profile_A*: [http://pros-and-cons-1.herokuapp.com/add_friend/profile_b](http://pros-and-cons-1.herokuapp.com/add_friend/profile_b). This can be attempted vice versa too.

This will result in the redirection back to the *Profile_B* profile page.

From *Profile_C* you can check both directions, you can force the URL from *Profile_C* [http://pros-and-cons-1.herokuapp.com/add_friend/profile_a](http://pros-and-cons-1.herokuapp.com/add_friend/profile_a) and from *Profile_A* [pros-and-cons-1.herokuapp.com/add_friend/profile_c](http://pros-and-cons-1.herokuapp.com/add_friend/profile_c). This covers a pending request to a profile and a pending request from a profile respectively.

Both will result in a redirection to the respective profile's page.

From *Profile_A* you can check *Profile_D* by adding the URL: [http://pros-and-cons-1.herokuapp.com/add_friend/profile_d](http://pros-and-cons-1.herokuapp.com/add_friend/profile_d). These two users are not friends so the same will have occur in reverse as well. This will result in a redirection to the respective profile page.

#### view_question()

All users, logged in or otherwise are able to view a question. This is more as a benefit for logged in users as they can add multiple pros and cons without continually needing to open a collapsed question.

If a user is not logged in and tries to force a URL that is for a question with "is_friends" set to "on" then they are redirected to the questions page.

If a user is logged in, but not the friend of the creator and "is_friends" is set to "on" then they are also redirected to the questions page.

If a user is logged in and is friends with the creator or is the administrator they can see the question as normal.

#### filters() and filter_name()

Filters are used to sort posts, users who are logged in or are logged out can sort posts. However, logged out users can not sort posts by "friends".

Because the filters URL is not specialised with an ID, users can not force the URL.

For users wishing to use the filter_name() function, they will need to be logged in. Those who are not, are redirected to the login page if they try to use the URL: [http://pros-and-cons-1.herokuapp.com/filter_name](http://pros-and-cons-1.herokuapp.com/filter_name).

#### search()

The search function works for any user, logged in or otherwise. If a user is not logged in or is not the friend of a question owner who has the "is_friends" set to "on", then the question does not appear in the search. This was tested by making a post with the word "question" in it and setting it to is_friends to "on".

Conversely, a user who is logged in and is friends with the user who created the question and is_friends is set to "on", this question will appear in the search.

#### search_profiles()

Searching for profiles can only be done through the profile page of a logged in user. If a user tries to force a search for profiles and are not logged in, they will be redirected to the login page: [http://pros-and-cons-1.herokuapp.com/search_profiles](http://pros-and-cons-1.herokuapp.com/search_profiles).

If a user is logged in and tries to force the search_profiles page through typing in the URL, then the post method is not activated and the user is redirected back to the questions page.

#### view_profile()

Any user can view all profiles. Only the user logged in can edit their own profile. A non-logged in user that attempts to force the URL [http://pros-and-cons-1.herokuapp.com/edit_profile/](http://pros-and-cons-1.herokuapp.com/edit_profile/) is redirected back to the login page. Those that are logged in are directed straight to their edit profile page if they attempt to force the edit_profile route.

#### profile()

If a user tries to put in a URL that is not to their own profile, they are redirected to their own profile regardless of the name in the URL: [http://pros-and-cons-1.herokuapp.com/profile/test4](http://pros-and-cons-1.herokuapp.com/profile/test4). Even if they choose to "edit" their profile, this will only edit the logged in user's profile. Any user that is not logged in will be redirected back to the login page.

#### edit_profile()

Only the user logged in can edit their own profile. A non-logged in user that attempts to force the URL [http://pros-and-cons-1.herokuapp.com/edit_profile/](http://pros-and-cons-1.herokuapp.com/edit_profile/) is redirected back to the login page. Those that are logged in are directed straight to their edit profile page if they attempt to force the edit_profile route. This does not matter if the user has attempted to force an edit of a profile from another user's page, they are still directed to their own profile for editing.

#### friend_requests()

If a user attempts to force seeing friend requests for another user, even if they are logged in, they are redirected to the questions page. Those that are not logged in are redirected back to the login page.

Those that try to decline friend requests that are not for them are redirected to the questions page if they are logged in or the login page if they are not: [https://pros-and-cons-1.herokuapp.com/friend_requests/5fecedfdfc5977f5080ea5bc/decline_friend](https://pros-and-cons-1.herokuapp.com/friend_requests/5fecedfdfc5977f5080ea5bc/decline_friend).

The same occurs for accepting a friend request too.

#### edit_question()

Only logged in users can edit a question. Any question that a user tried to edit and is not logged in, they are redirected back to the login page: [https://pros-and-cons-1.herokuapp.com/edit_question/6038257fdbb2162bce8aa5b6](https://pros-and-cons-1.herokuapp.com/edit_question/6038257fdbb2162bce8aa5b6).

Users that are logged in, but are not the owners of the question are redirected back to the questions page. This does not matter if the "is_friends" is set to "on" or "off".

#### finish_question()

Users that are not logged in and try to force a "finish" for a question are redirected back to the login page: [https://pros-and-cons-1.herokuapp.com/finish_question/603e624fdeb48600b204b20e](https://pros-and-cons-1.herokuapp.com/finish_question/603e624fdeb48600b204b20e).

Users that are logged in and try to force a "finish" question are redirected back to the questions page. The only method to finish a question is by hitting the "finish" button when visible.

#### remove_friend()

Only logged in users can access the remove friend button. If a user tries to force the URL and are not logged in, they are redirected back to the login page. Users that try to force the URL but are logged in, but have no friend association, are redirected back to their own profile page. Users with a friend association will not be able to remove the friend by this method. The only method is if a "post" request is completed. The test can be completed by attempting to force this URL: [https://pros-and-cons-1.herokuapp.com/remove_friend/test4](https://pros-and-cons-1.herokuapp.com/remove_friend/test4).

#### delete_question()

Only logged in users can access the delete question and only if they are an administrator or the user who created the post. Users that try to force the delete question link are redirected back to the login page if not logged in or back to the questions page if logged in and not the user who created the question or didn't use the post method.

This can be tested by trying to force a delete: [https://pros-and-cons-1.herokuapp.com/delete_question/6029562b3df6eb72f90e6034](https://pros-and-cons-1.herokuapp.com/delete_question/6029562b3df6eb72f90e6034).

#### send_message()

Only logged in users can send a message. The message must also be validated in exactly the same manner as a question text.

Users that are not logged in can not access the send message page. Those that are need to fill out the form in order to submit. But there can be no mathematical operators in the text. If a mathematical operator is used an error is returned but the user's text is not removed. The error states "Use only printable letters and numbers. Mathematical operators are not possible."

#### Routes containing an ID or profile name

During route by route testing URLs that don't exist were attempted. It was discovered that routes needed protection from users accidentally entering an incorrect ObjectId into a URL or by entering a username that does not exist for routes that require an ObjectId or correct username.

Some routes could be altered manually and incorrectly. In doing so, this throws a PyMongo error rather than a 404, page not found error. To circumnavigate that the length of an ID must be 24 characters, so any ID that is less than or greater than 24 characters will then cause the user to be redirected. If a user inputs a name that is not in MongoDB when viewing profiles or making friend requests etc, if the name does not exist, the user is redirected to the questions page.

## RESPONSIVE TESTING

Browsers used:

- Firefox
- Chrome
- Chrome Android
- Brave

Testing was conducted on a Huawei P20, 15in laptop and 32in desktop.

Multiple issues were discovered between mobile displays verses desktop displays. For instance:

- placeholders in search boxes overlapped the container they were in. Shortened placeholders were included for mobile displays.
- buttons to submit pros and cons overlapped their boxes. A new .right-align class was given to a div wrapping the submit buttons.
