# django_vue_app

Inside main folder ->

## Environment setup

```
python -m venv <env-name>
```

## Environment activation

```
<env-name>\Scripts\activate
```

## Install dependencies

```
pip install -r requirements.txt
```

## Run development server

```
python manage.py runserver
```

## Run tests

```
python manage.py test
```
## Endpoints

| Endpoint | Input  | Output |
| --- | --- | --- |
| boards/ |  | id, name |
| boards/add | name | |
| boards/update | id, name |  |
| boards/lists | id | id, name, order, archived |
| boards/add/list | id, name | |
| boards/update/list | id, name | |
| boards/change/list | id, nr | |
| boards/archive/list | id | |
| boards/delete/list | id | |
| boards/cards | id | id, name, description, order, archived, term |
| boards/add/card | id, name, description, term | |
| boards/update/card | *id, *description, *term | |
| boards/archive/card | id | |
| boards/delete/card | id | |