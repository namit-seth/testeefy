# TESTEEFY
#### Video Demo:  https://youtu.be/c4Bd9kE2ClI
## Description:
Testeefy is a quizing platform in which _examiners_ can create and publish tests in diffrent subjects. And various cantidates can attempt the test and check their knowledge of the particular topic.
## Files:
### app.py
includes the backend server code written in python(flask) manages the entire website. This has a number of routes rangeing from "/"(index) to "/test/create" to create test. this is the inteface between the user and the database to make sure only valid data is entered and the right pages are delivered to the client.
### helpers.py
has the repetitive code such as _login_required_ to make sure that the user is loged in before visting a certain page and _apology_ to return an apology if the minimum requirements have not been met. for eq for login id and password are required if the user fails to provide the same an apology highlighting the issue will be delivered.
### Project.db
This is main database for the entire project it store data including the user name and password to each of option and the response given by the candidate.
## Folders :
### static
incldues the dependencies of the webpages in the website such as images , stylesheet and javascript code.
### templates
include the html template for every webpage. theese templates are compiled by flask before being displayed to the user.

## Routes :
### /
it is the index page that breifly describes the project to the user. also tells them its features.
### /logout/
logs out the user. if any user is logged in it clears the session and logs them out.
### /register/
new user regestration. for a new user to register using their email id they have to register using the route.
### /login/
check the credentials entered by the user and validates them with the details in the database to check if the entered email is register or not if yes then if the entered password is correct or not.
### /tests/
for a examiner displayes all the tests they have created and for the candidate the various subjects in which they can attempt the tests,
### /test/create/
allows the examiner to create new tests. it has the option to add & delete options / questions, select the correct option.
### /tests/<subject>
displays all the tests for the given subject. if the subject is not supported then it returns a apology message using the apology function defined in the helpers.py file
### /test
this the page where the actual test happen. the test "id" is pluged in the url using the get method and the candidate sees the questions and the related questions
### /test/submit
when the user submits the attempted question and selected options are sent here using the post method. this function processes the data and produces a result with the help of the calc_result function and saves the attempts and the result in the database.
### /result
if an id is not provied then it displays all the tests they have attempted if an id is provied then it displays the results for all the attempts of that particular test id.
### /attempt
displays the attempted options.
