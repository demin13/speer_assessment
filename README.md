# Speer Assessment

This application, built using the Django Rest Framework, allows users to register, create multiple notes, and share notes with other users. The database used is PostgreSQL.

## Getting Started

### Prerequisites
- Ensure that PostgreSQL is running locally.
- Create a database and set the database credentials in the `.env` file.

    ```
    DB_NAME=speernotes
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

### Running Locally

1. **Create a Virtual Environment**

    #### Windows
   ```bash
   python3 -m venv myvenv
   myvenv\Scripts\activate
   ```

   #### Unix based (Ubuntu, etc)
   ```bash
   python3 -m venv myvenv
   source myvenv/bin/activate
   ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```


3. **Migrate to db**
   ```bash
   python manage.py migrate
   ```

4. **Start the Server**
   ```bash
   python manage.py runserver
    ```

5. **Import Postman Collection**
   * Sign up and log in to start using the notes APIs.

6. **To run Auth test cases , execute this command**
    ```bash
    python manage.py test Auth
    ```

7. **To run speernotes , execute this command**
    ```bash
    python manage.py test speernotes
    ```
