# optimhire
python 3.8.0
docker-compose 1.29.2

to run with docker-compose:
    - install docker-compose
    - run docker-compose up


to run without docker-compose:
    - install pip
    - install virtualenv or virtualenvwrapper
    - create a virtual environment
    - run pip install -r requirement.txt
    - run python manage.py runserver
    - the application will be running on port 8000



The application automatically creates a user with the following credentials:
email: naranjo.chuy@gmail.com
password : 123456

You can use insomnia to test the endpoints inside there is a json file to import it

The application has two endpoints:
POST method
/ api / login /
data to send
{
      "email": "naranjo.chuy@gmail.com",
      "password": "123456"
}

GET method
needs a bearer token which is returned by login
/ api / current-exchange-rate


