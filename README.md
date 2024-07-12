# Base-Course-Backend

This repository implements the backend for a course site.

The features developed contain user control, classes that are grouped by courses, which belong to categories. In addition, it is possible for users to save, record the viewing of lessons, comment and reply to comments.

Permissions are implemented to separate access for employees, authenticated users and anonymous users, also with a view to security and privacy (one user cannot know what the other has watched, for example).

Access by other applications is possible via a REST API, with CRUD for the models in the database.

An extensive range of tests has also been developed to prevent future modifications from breaking the functionality that has already been developed.

Feel free to contribute or use this project in your own projects, adjusting it as you wish and adding the functions you want for your application.

## How to use this application

After cloning the repository, create a virtual environment for Python and install the dependencies.

```[shell]
pip install -r requirements.txt
```

Create an .env file with the necessary information (available in .env.example).

Navigate to the backend directory configure and test the system

```[shell]
cd backend
python manage.py migrate
python manage.py test # this may take a while
python manage.py createsuperuser # enter user data
python manage.py runserver
```
