from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine  # connect classes to database tables
DBSession = sessionmaker(bind = engine) # create connection
session = DBSession() # create session

# Show all categories (/categories and /)
@app.route('/')
@app.route('/category')
@app.route('/categories')
def showCategories():
    categories = session.query(Category).all()
    # return render_template("restaurants.html", restaurants = restaurants)
    # return "Categories page"
    return categories

# Create new category
@app.route('/category/new', methods = ['POST'])
def newCategory():
    return "New category page"

# Edit category
@app.route('/category/edit/<int:category_id>')
def editCategory(category_id):
    return "Edit category {} page".format(category_id)

# delete category
@app.route('/category/delete/<int:category_id>')
def deleteCategory(category_id):
    return "Delete category {} page".format(category_id)

# show items within category
@app.route('/category/<int:category_id>')
def showCategoryItems(category_id):
    return "Items page for category {}".format(category_id)

# Create new item in a category
@app.route('/item/new/<int:category_id>')
def newItem(category_id):
    return "New item page for category {}".format(category_id)

# Edit item in a category
@app.route('/item/edit/<int:category_id>/<int:item_id>')
def editItem(category_id, item_id):
    return "Edit item page for item {} in category {}".format(item_id, category_id)

# delete item in a category
@app.route('/item/delete/<int:category_id>/<int:item_id>')
def deleteItem(category_id, item_id):
    return "Delete item page for item {} in category {}".format(item_id, category_id)

# Categories API
@app.route('/category/JSON')
def showCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(category=[r.serialize for c in categories])

# Items API
@app.route('/item/JSON/<int:category_id>')
def showItems(category_id):
    return "Items in category {} JSON".format(category_id)

# login
@app.route('/login')
def login():
    return "Login page"

# logout
@app.route('/logout')
def logout():
    return "Logout page"


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port = 8000)
