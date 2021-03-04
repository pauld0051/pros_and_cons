# Pros and Cons - A social media phenomena

[![Pros and Cons Logo](https://raw.githubusercontent.com/pauld0051/pros_and_cons/master/static/images/pros_and_cons_logo.png "Pros and Cons Logo")](https://pros-and-cons-1.herokuapp.com/)

Site: <https://pros-and-cons-1.herokuapp.com/>

## CONTENTS

- [Description](#description)
  - [UX](#ux)
    - [Goals](#site-goals)
    - [User Stories](#user-stories)
    - [Wireframes](#wireframes)
    - [Views and Data Structure](#views-and-data-structure)
    - [Design](#design)
      - [Typography](#typography)
      - [Color Scheme](#color-scheme)
  - [Features](#features)
    - [Existing Features](#existing-features)
      - [Account Registration](#account-registration)
      - [User Session](#user-session)
      - [Questions Page](#questions-page)
      - [Ask Questions](#ask-questions)
      - [Search Questions](#search-questions)
      - [Profile Page](#profile-page)
      - [Friends](#friends)
      - [Send Feedback](#send-feedback)
      - [Security](#security)
    - [Features Left to Implement](#features-left-to-implement)

- [Admin Responsibilities](#admin-responsibilities)

- [Known Bugs](#known-bugs)

## DESCRIPTION

**Pros and Cons** is a social media website aimed at bringing people from around the world together to answer user based questions on any topic imaginable. Users will have other users answer their question with the pros and cons of their upcoming decisions. The site will mimic similar social media sites and users can only answer questions when they are logged in. Users will be able to easily register and currently will not require any identification. All users will need to login to answer questions is a user name and password. Users will be able to allow public responses to their questions, or responses from their friends only.

## UX

### SITE GOALS

The basis for production of Pros and Cons was to have an all-inclusive social media site allowing users to ask questions and have responses from friends, family and even people they have yet to meet. User experience and ease of use were the main focuses for the site. This meant keeping away from an intrusive social media platform for one that requires very little input from users byt was still technically advanced and allows users to interact no matter their level of expertise.

The design and layout was inspired by current social media giants as well as the Code Institute's Task Manager application. This mean that there was a balance in form and user interactivity and functionality.

### USER STORIES

- As a user, I want to be able to easily join a web application without the need to provide email addresses.
- As a user, I want to be able to ask questions and view the replies as they occur.
- As a user, I want to be able to update my profile to reflect who I am and where I am from.
- As a user, I want to be able to delete a question if it is no longer required
- As a user, I want to be able to search through the questions and sort by popularity, time added, who added them and my own or friends' questions.
- As a user, I want to be able to search for friends' profiles based on their username, city, or country.
- As a user, I want to be able to edit questions that I have inputted.
- As a user, I want to add friends so they can see questions only designed for them.
- As a user, I want to unfriend people if the friendship has not worked out the way it was anticipated.
- As a user, I want to be able to add a pro or con as a reply to any question that was open for me to do so.
- As a user, I want to be able to feel safe on the social media platform and can reach out to administrators if required.
- As a user, I want to be able to login and stay logged in if I choose or choose to logout at any point.
- As a friend of the user, I want to be able to see just their questions.
- As a user, I want to be able to see who is answering my questions.

- Pros and Cons is a social media website that focuses on user's asking questions that they'd like to weigh up all possibilities before carrying out the said question; users can:

  - New Users can:

    - Register with a unique username and password without special characters

    - Stay logged in after registration without the need to continually sign in by simply clicking the checkbox at the bottom of the registration page

    - Check their password is correct before registering, a new user can not register if passwords do not match
  
  - Existing users who are logged in will be able to:

    - View the site and all questions that are open for public view or are friends with the logged in user

    - Sort all the questions by date added latest and oldest, friends only, user's posts only

    - Send and accept friend requests

    - Search for new friends by username, first name, last name, country and state

    - View friends profiles to see their questions

    - Adjust their profile to include their first name, last name, country and state as well as a hidden birthday

    - Change their profile picture based on sex/gender to either male, female, non-binary or rather not say, all fields in the profile are optional

    - Click on the home button to view all questions, including questions from the user's friends that are set to "friends only"

    - Click on any question on the questions page, read it and choose whether to add a pro or a con to that question

    - Adding a pro or a con opens the question to the browser so the user can add multiple pros and cons

    - Click on the person who created the question to see their profile

    - Send a friend request via the profile page of a viewed profile

    - Click on a question to open it in the browser or just browse the question from the homepage

    - Write a pro or a con on any browsed question on the homepage which then opens the question in the browser window for more pros and cons to be added

    - Write their own question via the "ask questions" link in the header

    - Add a title to the question and a body for more explanation

    - Set the question to public, allowing anyone to answer or to "friends only" meaning only friends can answer

    - View profiles of friends and unfriend them if needed

    - Finish a question they have started so that no more responses can be added

    - Edit or update a question the user started

    - Delete a question that the user started

    - Search for questions based on keywords

  - Users who are not logged in can:

    - View all open questions that do not have the "Friends Only" switch set to "on"

    - View the profile of the user who wrote the question

    - Search for questions
  
  - All users, logged in or not can:

    - View the site on mobile, tablet, desktop or any device with a web browser and an internet connection

To avoid excessive spamming or unsolicited messages, users must be logged in to add questions or pros and cons. Non-logged in users do not have a profile page, but can view registered users profiles, but can not add friendships.

### VIEWS AND DATA STRUCTURE

Pros and Cons was a relatively ambitious project to use the likes of MongoDB to produce a social media platform. Although some details did exist of previous attempts, none of these were used in the design or data structure. Instead, as user stories were being met, advancements were made for the routes on whether the user was creating, reading, updating, or deleting.

![Pros and Cons Flow Diagram](static/images/readme/question-flow.jpg)

Figure 1: *an example of a flow diagram showing the hierarchy of events for a user to view, edit, delete or respond to a question.*

Data validation was required for all user entries and updates. These varied depending on the type of input. All data validation processes were stored in a separate file, validate_funcs.py.

![Pros and Cons Validation techniques](static/images/readme/validation_technique.jpg)

Figure 2: *although other validation techniques were employed, they all ultimately prevent malicious code injection. All validation is done in both front and backend coding. The variation between the two regex codes is for the username to allow only letters or numbers, but questions are not allowed mathematical operators. The "[^" in username disallows these characters.*

User character input is limited to 255 characters for titles and pro and con replies, 1020 characters for textarea inputs, and up to 26 characters for names. This is consistent in both front and backend code. Birth dates are validated in the front end by using a Materialize date-picker and are subsequently validated at the backend by checking the format of the entry.

## DESIGN

The application was built using [Materialize](https://materializecss.com/) and its responsive grid system. The inspiration for the theme was inspired by [Code Institute](https://codeinstitute.net/)'s [Task Manager](https://flask-task-management-pd0051.herokuapp.com) application. Some of the Materialize styles were overwritten in a local CSS file: [style.css](static/css/style.css).

Fonts and colors were based entirely on Materialize's font structure to give the application a distinctive but yet familiar appeal.

### TYPOGRAPHY

Materialize uses [Roboto 2.0](https://fonts.google.com/specimen/Roboto?preview.text_type=custom) as a standard font.

### COLOUR SCHEME

Materialize uses a series of colour from a selective pallet: [Materialize Colour Schemes](https://materializecss.com/color.html)

#### Headings

All headings using a heading tag were one of the following colours:

- ![#1565c0](static/images/readme/1565c0.png) `#1565c0 - blue-text text-darken-3`
- ![#01579b](static/images/readme/01579b.png) `#01579b - light-blue-text text-darken 4`
- ![#c62828](static/images/readme/c62828.png) `#c62828 - red-text text-darken-3`

#### Text

Text colours use the standard Materialize and browser font colours as well as some minor changes for various text such as in the profile names. All icons are from the [Fontawesome](https://fontawesome.com/) library. The following colours were used:

- ![#607d8b](static/images/readme/607d8b.png) `#607d8b - blue-grey-text`
- ![#01579b](static/images/readme/01579b.png) `#01579b - light-blue-text text-darken 4`
- ![#212121](static/images/readme/212121.png) `#212121 - grey-text text-darken-4`
- ![#1565c0](static/images/readme/1565c0.png) `#1565c0 - blue-text text-darken-3`
- ![#ef5350](static/images/readme/ef5350.png) `#ef5350 - red-text lighten-1`


#### Buttons

Button colours were based on the following. All buttons contained white text or icons to help overcome those with colour-blindness:

- ![#1565c0](static/images/readme/1565c0.png) `#1565c0 - blue darken-3`
- ![#039be5](static/images/readme/039be5.png) `#039be5 - light-blue darken-1`
- ![#1e88e5](static/images/readme/1e88e5.png) `#1e88e5 - blue darken-1`
- ![#b71c1c](static/images/readme/b71c1c.png) `#b71c1c - red darken-4`
- ![#4caf50](static/images/readme/4caf50.png) `#4caf50 - green`
- ![#d32f2f](static/images/readme/d32f2f.png) `#d32f2f - red darken-2`
- ![#cfd8dc](static/images/readme/cfd8dc.png) `#cfd8dc - blue-grey lighten-4` (navigation)
- ![#26a69a](static/images/readme/26a69a.png) `#26a69a - teal lighten-1`

#### Cards and Panels

- ![#fafafa](static/images/readme/fafafa.png) `#fafafa - grey lighten-5`
- ![#e0f2f1](static/images/readme/e0f2f1.png) `#e0f2f1 - teal lighten-5`
- ![#b2dfdb](static/images/readme/b2dfdb.png) `#b2dfdb - teal lighten-4`

#### Navbar

- ![#e0f2f1](static/images/readme/e0f2f1.png) `#e0f2f1 - teal lighten-5`

All colour palettes were downloaded from [ColorHexa](https://www.colorhexa.com/) and resized in [Windows Paint 3D](https://www.microsoft.com/en-us/p/paint-3d/9nblggh5fv99?activetab=pivot:overviewtab).

## FEATURES

### EXISTING FEATURES

#### Account Registration

Users can register an account via the [registration](https://pros-and-cons-1.herokuapp.com/register) page.

- New users can register their account using letters and numbers for a username. There is no need to include an email at this time.
- The account name must pass validation and:
  - not include anything other than letters, numbers, hyphens and underscores and contain no spaces
  - not be the same as any previously registered name
  - be between 5 and 15 characters in length
  - have a validated password that is input twice for verification and be a minimum of 8 characters

#### User Session

- Existing users can log into their account using their chosen username and password
- If the "Remember me..." checkbox is ticked, the session will persist after the browser is closed
- Users can log out of their account and close the session
- If a user tries accessing certain pages or features from the application while logged out, they will be redirected to [login](https://pros-and-cons-1.herokuapp.com/login)

#### Questions Page

Whether logged in or not, users can view the [questions page](https://pros-and-cons-1.herokuapp.com/get_questions). This is where users can view questions and if logged in, users can answer questions with pros and cons. Logged in users can also sort the questions by "friends" or see their own questions they have asked.

Logged in users can sort questions by:

- Latest / the most recent asked questions
- Oldest / the oldest questions asked
- Friends / see only questions friends have asked
- Name / order posts created by users alphabetically
- Popular / posts with the most replies are at the top
- Needs answers / posts that have no replies are located at the top

Users that are not logged in can sort by the same categories, except for "Friends".

A separate button exists so logged in users can access their own questions only. From there they can sort their posts by:

- Latest
- Oldest
- Popular
- Needs answers

All questions are in a collapsed form and only the question title and a down-pointing chevron are visible. Users can click on the chevron to view individual posts and see the question text and any replies from within the opened accordion style collapsible. Users can also click on the title to open that question in the browser tab only. This allows for entry of pros and cons to the same item without refreshing back to a collapsed accordion. The opened question displays as though it is still accordion style, however, the chevron is replaced with a question mark and the question title is no longer in hyperlink-blue.

All questions have the same format:

- Question title
- Question text
- Two cards, side by side, one for Pros (on the left) and Cons (on the right)
- If users are logged in, they will see an input field for pros and cons with a submit button
- Users who are not logged in do not see any place for input or any submit buttons
- In italics, directly below the pros and cons cards shows who created the question, the date and time when the question was created and, if edited, the date and time of the latest edit
- A globe icon is depicted for all public questions and a friends icon for questions that are for friends only. Users who are not friends with the post owner will only be able to see their public posts
- Users that are logged in and are the post owner will see three buttons, Finish - Edit - Delete
  - Finish - this closes a question for further commenting. Italic text below the created by text states the question is closed for further commenting. Users can no longer submit pros and cons to this post and the post owner can no longer edit the post. However, they can delete the post if they see fit
  - Edit - users can edit their posts' title and text but are still bound by the rules of no mathematical operators in the text
  - Delete - removes the post and all replies in the pros and cons section. Users who attempt to access a post that is no longer available will get the 404 page error
- From the view question page, if a user had clicked on the title link from the questions page or a profile page, all users (logged in or not) can share the question to Facebook or to Twitter

An example question is set up here: [http://pros-and-cons-1.herokuapp.com/view_question/6040989f61e7e8310f344aa0](http://pros-and-cons-1.herokuapp.com/view_question/6040989f61e7e8310f344aa0). This can be viewed by anyone.

#### Ask Questions

The [ask questions](http://127.0.0.1:5000/add_question) link is only available to logged in users. Here a session user can input a question title and text. This is also where users can choose whether to make the post public or for friends only.

- Public posts / questions can be viewed by anyone and answered by logged in users
- Friends only / questions can only be viewed by the user's friends and the site creator for protection of all users

Users who are asking questions can use all characters except for mathematical operators as bound by a backend regex.

#### Search Questions

Users can search for keywords in question titles or text. The search is not case sensitive.

#### Profile Page

Only logged in users have access to their profile page. All users, logged in or otherwise, have access to view profiles by clicking on the "created by" link to the username on any question. Users who are logged in can also search for profiles from the profile page. A user can see if any friend requests have been received on their profile page. If a red "plus" symbol is flashing in the body of their profile page, a user can click on this to see all incoming friend requests. This is covered in detail in the [friends](#friends) section below.

Profile pages contain some information about the user:

- Profile picture / this is based on the chosen sex - female, male, non-binary or prefer-not-to-say
- Name / includes both first and last name if entered
- Country / includes the user's country if entered or remains blank or as not specified
- State / only included if the user's country has been entered or this field remains blank
- Birthday / only if the user is looking at their own profile, contains day-month-year
- A list of all questions that the user has asked

All information on the user is optional to add and can be done so by clicking the [edit profile](http://pros-and-cons-1.herokuapp.com/edit_profile/) link. Here users can add or edit:

- Profile picture / based on a chosen sex
- First name / can contain characters but not numbers or mathematical symbols and can be between 2 and 26 letters long
- Last name / is bound by the same regex format as first name
- Birthday / is set to the format %d %B, %Y or can be left blank
- Country / is bound by the same regex format as first name but can be selected from a list of countries found in [countries.json](https://github.com/pauld0051/pros_and_cons/blob/master/countries.json). The original file was adapted from Stefan Binder's [Full Country and State list of our planet](https://github.com/stefanbinder/countries-states).
- State / bound by the same rules as country and from the same [countries.json](https://github.com/pauld0051/pros_and_cons/blob/master/countries.json) file.

Users can also view the profiles of other users. The same information exists, except birthdays are not visible to any user. A list of questions that user has asked is available directly below their profile information. 

Logged in users can search for users by profile username, first name, last name, country or state. A list of users matching any of those descriptions is displayed on a page in collapsible accordion menus. Session users can view the profile from the accordion or click on the link in the title to visit the profile page. Users can send and accept friend requests from the accordion or view profile page.

Users who are friends with a viewed profile page owner can also remove that friendship if they deem necessary.

#### Friends

One of the biggest draw cards for a social media platform is the ability to make new friends and foster existing, real-world friendships. Pros and Cons currently offers a simple friendship status that allows "friends" to view posts that are for friends-only.

From any profile page, other than the logged in user's page, a series of icons may exist.

- Add friend / a logged in user can send a friend request to the owner of that profile
- If a pending friend request from the logged in user exists to the owner of a viewed profile, a "pause" icon will be displayed until that user responds to that friend request
- If a pending friend request from the owner of a viewed profile exists then two icons will be present:
  - Accept request / the logged in user and viewed profile owner are now friends
  - Decline request / the logged in user and viewed profile owners did not become friends, but there is still an option to do so
- If there are no pending friend requests or current friendships on a viewed profile, the logged in user can send a friend request by using the Add friend button

Session users can access friend requests from their profile page. A red, flashing "plus" button exists if friend requests have been received. From there the user can choose to accept or decline the invitation for friendship. A user can view the profile of the requestor and make their choice from their profile.

Session users can also remove friendships from a view-profile page if a friendship previously exists. This prevents that user from seeing questions that are set to "friends only".

**Known bugs:**

1. Materialize navbar links "flash" on click. This occurs in Firefox and appears to be due to either hardware acceleration or an extension installed on Firefox. During development Firefox was started in safemode which removed the issue completely. Some users may therefore experience the flashing when clicking links on the navigation pane at the top of the screen.

2. Materialize datepicker colouring: https://stackoverflow.com/a/59578282/13062685 special thanks to Kasia https://code-institute-room.slack.com/team/USVE7NATV

3. Script tags need to be loaded within the template close to where they are being used or, at the top of the template loading with the page. This was experimented on with the edit_profile.html template. In order to add the countries.json file to be read in JavaScript, a new country.js file was added in static/scripts. This was called on using Jinja template formatting in the same method as previously employed on the base.html template. However, when located at the bottom of the page before the endblock tags, meant the script would not run and subsequently failed to provide the desired outcome. This was possibly caused by interference with other loading scripts from the base.html template. When the script call was placed at the top of the page just outside the block content tags meant the script loaded too early and therefore id-tags were not read by the script file. To overcome this a setTimeout function was employed. While this worked, it was not an acceptable workaround. Moving the script just below the select tags where it was being called meant there was no need for a setTimeout function and the script would run effectively without further intervention.

4. A world-country picker and state was to be used from https://geodata.solutions/, however, due to templating issues the scripts would not load correctly rendering the dropdown boxes inoperable. A local JSON file was employed to replace this method. This has the upper advantage of being unlimited in use as well as not relying on external API for reliability.

5. Select tags using Materialize built in styling makes adding JavaScript DOM manipulation more difficult. This is because Materialize converts any new select element into a ul element, so it can apply custom styling to it. When using a document.createElement('option') command, instead of creating a new option, Materialize will create the styled dropdown option instead. To overcome this, jQuery is loaded in the base.html file at the top, along with Materialize CDN. This allows jQuery to be used on the edit_profile page without loading another instance of jQuery. From here, jQuery commands that Materialize use can be employed such as: ```$('#state').on('contentChanged', function () {
  $(this).formSelect(); });```
  from here the remainder of the jQuery and JavaScript for-loop can be coded and input int the select element at the appropriate location. Two sections of this code will appear, one for when a country change is made by the user (eventListener "change") and one for when the page loads, this means the user can change state if they have already selected a country.

6. User profile search requests to MongoDB are slightly limited in their capacity to search for usernames with digits. For example, if a username contains more than 1 digit in it then MongoDB's index function does not return that value. A username with just one digit in it at the end of the name is returned. For example admin1 will be returned if a search for "admin" was conducted. But admin12 will not be returned for the same search.

### NOTES

Using the user test4 and searching for "admin" a full range of friendships affiliations is available:

1. test4 is friends with admin. The searched profile in the collapsible shows a "check" symbol.
2. test4 has a pending friend request that was sent by test4 to admin2. The searched profile collapsible shows a "pause" symbol.
3. test4 has a pending friend request from admin1 and can therefore accept or decline that request from withing the collapsible by clicking the appropriate button.
4. test4 has no friendship affiliation at all or pending requests with admin11 therefore test4 can send a request to admin11 from the collapsible.

The difference in this technique compared with just viewing the profile is that there is a loop of profiles being presented to the screen. Viewing a profile has just one profile so all the same four variables can be tested without a loop. The final clause, where no friendship affiliation is found, is sorted with a tuple and then looped through in the frontend for the matches "True" or "False" against the username. 

## SECURITY

An admin user was set up using a random key generator to prevent the possible forcing entry using the "admin" username. 

To prevent users from accessing certain areas of the page when they're not logged in Flask will check for session users. The homepage requires users to be logged in to check their friendships against those asking questions.

## ADMIN RESPONSIBILITIES

The admin role plays a very special part in Pros and Cons. The admin is given a secret username but has unlimited access to all posts, profiles, questions, pros and cons as well as an ability to receive messages from users. An admin is the only user who can currently receive messages. For security reasons, these messages are only available to the admin user account and can only be accessed with the admin user account. At present, these messages will only be available from manually accessing them in MongoDB, however, a count is accessible on the admin user profile page. No other page has access to this count. Messages are deleted manually from MongoDB as they are actioned.

The admin user account can edit, delete or finish any questions that do not meet the standards accepted by Pros and Cons as a friendly and safe social media outlet. If users continually breach the site rules, their account may be removed from the MongoDB database. Currently this is done manually.
