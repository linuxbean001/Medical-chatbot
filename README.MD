# Medical
This is the django project which extracts data by using Natural Text. A Chatbot for doctors to find patients data.

## Prerequisites
Before you begin, ensure you have met the following requirements:

1. You have installed Python 3.8 or later
2. You have installed Django 3.2 or later
3. You have installed the required packages listed in requirements.txt

## Installing the project
To install the project, follow these steps:

1. Clone the repository to your local machine.
2. Create a new virtual environment for the project.
3. Activate the virtual environment.
4. Install the required packages by running **'pip 
install -r requirements.txt'**.
5. Set up the database by running **'python manage.py migrate'**.
6. First time adding data in models by running **'python manage.py first_data_update'**.
this will take some time to complete because data is comming from airtable through api.
7. Now some of Tables doesn't have data on airtabe or not even Tables are there.
8. So we have fill data on these models from our csv files by running some commands - 1. **'.\sqlite3.exe db.sqlite3'**
9. After that **'.mode csv'**.
10. Now 4 commands for 4 files 1. **'.import procedures.csv chatbot_procedure'**,  2.**'.import observations.csv chatbot_observations'**, 3. **'.import medications.csv chatbot_medication'**, 4. **'.import allergies.csv chatbot_allergy'**
11. Now we need to create superuser to see filled data in admin panel by command **'python manage.py createsuperuser'**.
12. After running command you need to fill Username,
Email and password.   
13. Start the development server by running **'python manage.py runserver'**.

## Usage
1. Start the development server by running python manage.py runserver.
2. Open your web browser and go to http://localhost:8000. You should see the homepage of the project.
3. To create a superuser account, run python manage.py createsuperuser in your terminal. Follow the prompts to enter your desired username, email, and password. This will give you access to the Django admin panel, where you can manage your project's data and configuration.
4. To access the admin panel, go to http://localhost:8000/admin in your web browser. Log in with the superuser account you just created. From there, you can manage your project's models, users, groups, and other settings.

## Important Points for usage
1. Chatbot will lock patient after taking "yes" or some similar words for confirmation.
2. If there is current or upcoming or similar words which indicates about present or future then chatbot will find data which has date of today or after today.
3. If you want to talk about any other patient then first you need to unlock patient by clicking on lock sign.

