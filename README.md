# Pros and Cons - A social media phenomena

[![Pros and Cons Logo](https://raw.githubusercontent.com/pauld0051/pros_and_cons/master/static/images/pros_and_cons_logo.png "Pros and Cons Logo")](https://pros-and-cons-1.herokuapp.com/)

Site: <https://pros-and-cons-1.herokuapp.com/>

## CONTENTS

- [Description](#description)

- [Known Bugs](#known-bugs)

## DESCRIPTION

**Pros and Cons** is a social media website aimed at bringing people from around the world together to answer user based questions on any topic imaginable. Users will have other users answer their question with the pros and cons of their upcoming decisions. The site will mimic similar social media sites and users can only answer questions when they are logged in. Users will be able to easily register and currently will not require any identification. All users will need to login to answer questions is a user name and password. Users will be able to allow public responses to their questions, or responses from their friends only.

**Known bugs:**

1. Materialize navbar links "flash" on click. This occurs in Firefox and appears to be due to either hardware acceleration or an extension installed on Firefox. During development Firefox was started in safemode which removed the issue completely. Some users may therefore experience the flashing when clicking links on the navigation pane at the top of the screen.

2. Materialize datepicker colouring: https://stackoverflow.com/a/59578282/13062685 special thanks to Kasia https://code-institute-room.slack.com/team/USVE7NATV

3. Script tags need to be loaded within the template close to where they are being used or, at the top of the template loading with the page. This was experimented on with the edit_profile.html template. In order to add the countries.json file to be read in JavaScript, a new country.js file was added in static/scripts. This was called on using Jinja template formatting in the same method as previously employed on the base.html template. However, when located at the bottom of the page before the endblock tags, meant the script would not run and subsequently failed to provide the desired outcome. this was possibly caused by interference with other loading scripts from the base.html template. When the script call was placed at the top of the page just outside the block content tags meant the script loaded too early and therefore id-tags were not read by the script file. To overcome this a setTimeout function was employed. While this worked, it was not an acceptable workaround. Moving the script just below the select tags where it was being called meant there was no need for a setTimeout function and the script would run effectively without further intervention.

4. A world-country picker and state was to be used from https://geodata.solutions/, however, due to templating issues the scripts would not load correctly rendering the dropdown boxes inoperable. A local JSON file was employed to replace this method. This has the upper advantage of being unlimited in use as well as not relying on external API for reliability.

5. Select tags using Materialize built in styling makes adding JavaScript DOM manipulation more difficult. This is because Materialize converts any new select element into a ul element, so it can apply custom styling to it. When using a document.createElement('option') command, instead of creating a new option, Materialize will create the styled dropdown option instead. To overcome this, jQuery is loaded in the base.html file at the top, along with Materialize CDN. This allows jQuery to be used on the edit_profile page without loading another instance of jQuery. From here, jQuery commands that Materialize use can be employed such as: ```$('#state').on('contentChanged', function () {
  $(this).formSelect(); });```
  from here the remainder of the jQuery and JavaScript for-loop can be coded and input int the select element at the appropriate location. Two sections of this code will appear, one for when a country change is made by the user (eventListener "change") and one for when the page loads, this means the user can change state if they have already selected a country.

6. User profile search requests to MongoDB are slightly limited in their capacity to search for usernames with digits. For example, if a username contains more than 1 digit in it then MongoDB's index function does not return that value. A username with just one digit in it at the end of the name is returned. For example admin1 will be returned if a search for "admin" was conducted. But admin12 will not be returned for the same search.

## NOTES

Using the user test4 and searching for "admin" a full range of friendships affiliations is available:

1. test4 is friends with admin. The searched profile in the collapsible shows a "check" symbol.
2. test4 has a pending friend request that was sent by test4 to admin2. The searched profile collapsible shows a "pause" symbol.
3. test4 has a pending friend request from admin1 and can therefore accept or decline that request from withing the collapsible by clicking the appropriate button.
4. test4 has no friendship affiliation at all or pending requests with admin11 therefore test4 can send a request to admin11 from the collapsible.

The difference in this technique compared with just viewing the profile is that there is a loop of profiles being presented to the screen. Viewing a profile has just one profile so all the same four variables can be tested without a loop. The final clause, where no friendship affiliation is found, is sorted with a tuple and then looped through in the frontend for the matches "True" or "False" against the username. 

## SECURITY

An admin user was set up using a random key generator to prevent the possible forcing entry using the "admin" username. The Jinja template allows a user that matches the "created_by" database tag to update or delete an entry. But an admin given a secret username will be able to also update and delete entries if deemed inappropriate. As more admins are employed, more admin names can be introduced into the backend. No admin will be given the title 'admin' as their username.

To prevent users from accessing certain areas of the page when they're not logged in Flask will check for session users. The homepage requires users to be logged in to check their friendships against those asking questions. If someone is not logged in they are given the impossible user name: wITbuhxpgAn0JZYyXCUr.

This works on two levels - 1) a username can not have capital letters in it. And 2) the name would be unlikely to be chosen by any user due to its randomness. 
