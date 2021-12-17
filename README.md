# Planet-Watches
django-angular ecommerce project - created for an interview.

This project consists of a Django backend and an angular front-end. It use an Sqlite database.:

### Deployment notes
#### Backend
Set python env

`pip install -r requirements.txt`

Create database
`python manage.py migrate`

Load initial data
`python manage.py loaddata initial_data.json`

Run server
`python manage.py runserver 8010`

#### Frontend
Install requirements
`npm install`

Run server
`ng serve`

### Demo Site
https://planet-watches.herokuapp.com/
