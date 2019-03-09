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
    '''Shows all categories associated with a user in the database'''
    # edit to add user logic
    categories = session.query(Category).all()
    return render_template("categories.html", categories = categories)
    # return "Categories page"

# Create new category
@app.route('/category/new', methods = ['GET', 'POST'])
def newCategory():
    # if 'username' not in login_session:
    #    return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'],
            # add user_name here
            )
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')

# Edit category
@app.route('/category/edit/<int:category_id>', methods = ['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
    	Category).filter_by(id=category_id).one()
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if editedCategory.user_id != login_session['user_id']:
    #     return "<script>function myFunction() {alert('You are not authorized to edit this category. Please create your own category in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)

# delete category
@app.route('/category/delete/<int:category_id>', methods = ['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
    	Category).filter_by(id=category_id).one()
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if restaurantToDelete.user_id != login_session['user_id']:
    #     return "<script>function myFunction() {alert('You are not authorized to delete this category. Please create your own category in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.query(Item).filter_by(category_id=category_id).delete()
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)

# show items within category
@app.route('/category/<int:category_id>')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    # creator = getUserInfo(category.user_id)
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    # if 'username' not in login_session or creator.id != login_session['user_id']:
    #     return render_template('publicmenu.html', items=items, restaurant=restaurant, creator=creator)
    # else:
    #    return render_template('menu.html', items=items, restaurant=restaurant, creator=creator)
    return render_template('category.html', items=items, category=category) # , creator=creator)

# Create new item in a category
@app.route('/category/<int:category_id>/item/new', methods = ['GET', 'POST'])
def newCategoryItem(category_id):
    # if 'username' not in login_session:
    #     return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    # if login_session['user_id'] != category.user_id:
    #     return "<script>function myFunction() {alert('You
    #     are not authorized to add items to this category.
    #     Please create your own category in order to add items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                description=request.form['description'],
                category_id=category_id) # , user_id=category.user_id)
        session.add(newItem)
        session.commit()
        flash('New Item,  %s, Successfully Created' % (newItem.name))
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)

# Edit item in a category
@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
    # if 'username' not in login_session:
    #     return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    # if login_session['user_id'] != categor.user_id:
    #     return "<script>function myFunction() {alert('You
    #     are not authorized to edit items in this category.
    #     Please create your own category in order to edit items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id, item_id=item_id, item=editedItem)

# delete item in a category
@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteItem.html', item = itemToDelete, category_id=category_id)

# Categories API
@app.route('/category/JSON')
def showCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(category=[r.serialize for c in categories])

# Items API
@app.route('/category/<int:category_id>/item/JSON')
def showItems(category_id):
    return "Items in category {} JSON".format(category_id)

# Login
@app.route('/login')
def showLogin():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# logout
@app.route('/logout')
def logout():
    return "Logout page"

# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host="0.0.0.0", port = 8000)
