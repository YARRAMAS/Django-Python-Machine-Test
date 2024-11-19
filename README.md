# MachineTest-DjangoRestFramework
# Django REST API Machine Test
This project is designed to build a RESTful API system for managing users, clients, and projects. It includes features for registering clients, fetching client information, editing/deleting client data, adding projects, and assigning users to projects. The system uses PostgreSQL as the database.

# Requirements
Python 3.x
PostgreSQL
Django 5.x
Django REST Framework

pip install -r requirements.txt
Install PostgreSQL

Ensure PostgreSQL is installed and running on your machine. You can download and install it from PostgreSQL official website.

After installation, ensure that PostgreSQL service is running.

# How to Set Up the Database Design
Create PostgreSQL Database
Create a PostgreSQL Database

# You need to create a database to store the application data. Run the following commands in your PostgreSQL shell or pgAdmin:

CREATE DATABASE machine_test;
Create a Database User (Optional)

If you want to use a specific user for your project, create a new user in PostgreSQL:

CREATE USER machine_user WITH PASSWORD 'yourpassword';
Grant Permissions to the User

Grant the necessary permissions for the new user:

GRANT ALL PRIVILEGES ON DATABASE machine_test TO machine_user;
Set Up the Database Configuration in Django

In the settings.py file of your Django project, configure the database settings as follows:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'machine',
        'USER': 'emp',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# How to Run the Code
Migrations
Run Migrations to Set Up the Database Schema

After setting up the database and configuring it in settings.py, you need to apply the migrations to create the tables in the PostgreSQL database:

python manage.py migrate
This will create all the required tables based on the models defined in the Django application.

Creating Superuser (Optional)
To access the Django admin interface, create a superuser:

python manage.py createsuperuser
Follow the prompts to create a superuser account.

Running the Server
To run the Django development server, execute the following command:


python manage.py runserver
By default, the server will start at http://127.0.0.1:8000/. You can now access the API endpoints from your browser or through an API client like Postman.

# API Endpoints
1. Register a Client
POST /clients/

2. List All Clients
GET /clients/

3. Retrieve Client Information
GET /clients/:id/

4. Update Client Information
PUT/PATCH /clients/:id/
I
5. Delete Client
DELETE /clients/:id/
Response: 204 No Content
6. Create New Project for a Client
POST /clients/:id/projects/

7. List All Projects Assigned to the Logged-in User
GET /projects/

# Conclusion
This Django REST API provides a complete system to manage clients, projects, and users, with full CRUD capabilities and user assignments. The system is built using Django and PostgreSQL, with Django REST Framework handling the API endpoints.
