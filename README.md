# RESTFul APIs with Flask

## Description
The project demos how to write a couple of RESTful APIs on Vic courses registrations  

## Table Schema
users
```commandline
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
 ```
courses
```commandline
    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    course_type = Column(String)
    teacher = Column(String)
    hours = Column(Integer)
    tution = Column(Float)
```

## Database
SQLite is an embedded, server-less relational database management system. It is an in-memory open-source library with zero configuration and does not require any installation.
DB Browser for SQLite (DB4S) is a high quality, visual, open source tool to create, design, and edit database files compatible with SQLite.

## Operation on database
Activate venv

Initialize Database
```commandline
flask db_create
flask db_seed
flask db_drop
```

## Start service 
```commandline
flask run --host 0.0.0.0 --port 8080
```

## Mail Server 
https://mailtrap.io/home

## Deployment
Export dependencies to requirements.txt
```commandline
pip freeze > requirements.txt
```
