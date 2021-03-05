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
- Text longer than 1020 characters

### Adding a pro or a con to a question

Only logged in users are able to add a pro or a con. Users who are not logged in are unable to "force" a pro or a con.

Pros and cons have the same validation criteria. A pro or con will be rejected if:

- Contains mathematical operators
- Is longer than 255 characters

### Adding a friendship

Users who are logged in are able to accept, decline and send friend requests. Users that try to force a friend request are redirected to the profile of the user they're sending the request to. Users that try to accept or decline friendships that they are not receiving (ie, have a url for an accept or decline friendship) are redirected back to the questions page. Only users who received the friendship request can act on them.

### Help Page

All users can view the help page, but only users who are logged in are able to send the administrator messages.

### 404 - page not found

A user, logged in, or otherwise, could try to enter their own URL, if this is not found, a 404 page is displayed.

### 403 - Forbidden

If a user attempts does something that is not able to be accepted into the database, a 403 page is displayed.

### 500 - Server Error

A 500 page is displayed if the server is not receiving requests at that time.

### 405 - Error

If a user attempts to force "add" a pro or con, a 405 error is displayed.