# Project: Catalog Web Application

This application allows users to capture categories and items within those categories. Users cannot access either items or categories created by other users

## Design

The project uses python in a flask framework to access either a
SQLite3 or PostgreSQL database. Depending on database used the database engine string in both the `application.py` and the `database_setup.py` file will need to be commented/uncommented. 

### Pages

There are nine pages:

1. categories.html - lists all categories
2. category.html - lists all items in a single category
3. newCategory.html - adds a new category
4. editCategory.html - for editing category information
5. deleteCategory.html - for deleting a category
6. newItem.html - for adding a new item to a
   category
7. editItem.html - for editing an item within a category
8. deleteItem.html - for deleting an item within a category
9. login.html - for logging in to the application

### Routes

Routes are structured as follows:

* / or /categories - shows all categories
* /category/new - add a category
* /category/<int:category_id>/edit - edit an existing
  category
* /category/<int:category_id>/delete - delete an existing
  category
* /categories/JSON - retrieve a serialized list of
  category data
* /category/<int:category_id> - shows all items in
  a single category
* /category/<int:category_id>/new - add an item to a
  category
* /category/<int:category_id>/<int:item_id>/edit - edit
  an item in a category
* /category/<int:category_id>/<int:item_id>/delete -
  delete an item in a category
* /category/<int:category_id>/JSON - retrieve a
  serialized list of items and their attributes from a category
* /login - login to the application

### Database

The SQLlite3 database, `category.db` (or postgres database, category) contains three
tables, `Category`, `Item`, and `User`. These are set up using the `database_setup.py` script as described below.

### Python scripts

The python script consists of two modules, one that performs
database setup via SQLAlchemy ORM `database_setup.py` and
another that contains routes and functionality, `application.py`

## Getting Started

### Prerequisites

1. [Python 2](https://www.python.org/download/releases/python-2715/) - The code uses ver 2.7.15
2. [Sqlite3](https://www.sqlite.org/) - SQLite3 database
3. [SQLAlchemy](https://www.sqlalchemy.org) - SQLAlchemy for
   creating and accessing the database.
4. [flask](http://flask.pocoo.org) - A web microframework
   for Python.

### Installing

 1. Download the latest version of Python from the link in Prerequisites.
 2. Download and install SQLite3 or download and configure PostgreSQL.
 3. Install SQLAlchemy via pip: `pip install sqlalchemy`
 4. Install Flask via pip: `pip install flask`
 5. Clone this repository.
 6. Use command `python database_setup.py` to create the database. Postgres will require setting up the database `catalog` with user `catalog`.

## Instructions

* Use command `python application.py` to run the application
  database locally.
* Access the application on http://localhost:8000/ if run locally or on the appropriate URI if hosted.

## Authors

* Ken Brooks, Treadwell Media Group
