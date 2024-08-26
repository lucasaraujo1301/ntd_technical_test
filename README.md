# Overview
This is a project build for NTD Software technical test.

# What do you need
To run this project you will need have some tools on you computer:
- Docker
- Python 3.10 or higher

# Steps
To run this project you will need to follow the following steps:
- cp .env.example .env
- docker-compose up -d db 
- docker-compose up app
> **_NOTE:_** Just for you information, I put the command `docker-compose up -d db` to you log be not polluted, if you want to see the logs from database as well, just run `docker-compose up`.

In other terminal run the follow command to create a superuser, will ask to type the email and password:
- docker-compose run --rm app sh -c "python manage.py createsuperuser"

After run the application and create your superuser, go to `http://localhost:8000/api/docs/` to check de API's docs and have fun!