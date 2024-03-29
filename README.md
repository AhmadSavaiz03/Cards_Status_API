# Cards_Status_API

<b>Overview</b><br/>
This project is designed as a backend service for a credit card issuer, aimed at providing an internal API to return the status of a user's card. The project includes all the necessary functionality for taking data from partners' company CSV files and processing these "cards" accordingly. It has an API endpoint to return the card's status.

<b>Getting Started</b><br/>
<b>Prerequisites:</b><br/>
Python 3.9+
PostgreSQL
Docker

<b>Set Up a Virtual Environment:</b><br/>
python -m venv venv
venv\Scripts\activate

<b>Install Dependencies:</b><br/>
pip install -r requirements.txt

<b>Configure PostgreSQL:</b><br/>
Create a PostgreSQL database and user.
Enter these commands in the environment after:
flask db init
flask db migrate -m "Create cards table"
flask db upgrade

<b>Using Docker:</b><br/>
docker build -t backend_project .
docker run -p 5000:5000 backend_project

<b>API Reference:</b><br/>
Endpoint: /get_card_status
Method: GET
Parameters:
card_id: String, unique identifier of the card.
user_phone: String, 9-digit phone number of the user without country code.

I have also created test_api.py testing on sqlite and test_api2.py testing on postgresql database for my own reference. They can also be used to check functionality.

<b>The Journey:</b><br/>
The framework I used was Flask with Python because it has better data handling libraries like pandas, it is simple but powerful, it has more extensive documentation, and they are the stacks I am most comfortable with. However, I have not used Flask before I found it intuitive as it is similar to PHP. I created a prior front-end project which I combined with this project to see how the backend works on a web page. Flask supported SQLAlchemy and I could have used MySQL or SQLite which I have used before but I decided to go for PostgreSQL as it offers better scalability and is better for handling data from multiple sources. I was also excited about learning new things throughout the project.

For the structure of the project, I got inspiration from GitHub and YouTube Flask projects and Chat GPT. There was a circular dependency error that I encountered for which I created extensions.py. Another error I encountered was in the migrations. My card model was not being implemented on the database I had created. Initially, I thought it was a database issue because unlike other SQL the database has to be created outside visual code through a PostgreSQL terminal. I later found it was an issue with the migration file created and I had to edit it manually. Other issues I faced included the testing. The with app.app_context(): feature to allow programs to know they are running within the app was also new to me and I frequently ran into errors by wrongfully placing initializations outside or inside it. Another interesting stump I faced was importing CSV files as for some reason I was not able to relatively address so I went for absolute addressing. I also had to learn dockerization but that was a relatively simple concept.

As of right now one of the tests in test_api2.py is returning false which still has me confused. I have written some code for celery which can be used for the automation of CSV file processing but have not implemented it into the program yet. I also have a config.py to scale up the project but have not implemented it on the program. As for possible improvements most importantly this program needs to be tested more. After that is done it can be automated and tested with a stream of data. After that test using actual data and then ensure that while deploying we encrypt it using HTTP protocol. I learned how to use Heroku but that is one of the final steps so I did not do anything with it.
