# speer_assessment

In this Application users can register themselves and add multiple notes.
Also, they can share notes among another users.

Framework - Django Rest Framework
Database - postgreSql

Make sure postgres is running locally 
create a database and put all db credentials in .env file
DB_NAME=speernotes
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

## How to run locally

Step 1: Create virtual enviornment 
### Windows 

#### python3 -m venv myvenv

To activate

#### myvenv\Scripts\activate

### Unix based (Ubuntu, etc)

#### python3 -m venv myvenv

To activate
#### source myvenv/bin/activate


Step 2: Install all libraries from requirements.txt

#### pip install -r requirements.txt


Step 3: Migrate to db

####  python manage.py migrate

Step 4: Start server

#### python manage.py runserver


Step 5: Now import postman collection and signup and login then start using notes apis

Step 6: You can also run test cases written

To run Auth test cases , execute this command
#### python manage.py test Auth

To run speernotes , execute this command
#### python manage.py test speernotes
