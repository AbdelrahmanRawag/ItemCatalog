from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

client_id = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# return Categories and Items
@app.route('/')
def Categories():
    categories = session.query(Category).all()
    items = session.query(CategoryItem).limit(len(categories)).all();
    return render_template('categories.html', categories=categories, items=items)


# Show the category by the id
@app.route('/Category/<int:category_id>/')
def Categoryy(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(category_id=category_id).all()
    categories = session.query(Category).all()
    return render_template('category.html', categories=categories, items=items, category=category)


# show Specific item
@app.route('/CategoryItem/<int:categoryitem_id>/')
def CategoryItemm(categoryitem_id):
    item = session.query(CategoryItem).filter_by(id=categoryitem_id).one()
    return render_template('item.html', item=item)

# create new item
@app.route('/CategoryItem/new', methods=['GET', 'POST'])
def CreateCategoryItem():
    if 'username' not in login_session:
        return redirect('Categories')
    if request.method == 'POST':
        catitem = CategoryItem(name=request.form['name'], description=request.form['Description'],
                               category_id=request.form['category'], user_id=login_session['user_id'])
        session.add(catitem)
        session.commit()
        return redirect(url_for('CategoryItemm', categoryitem_id=catitem.id))
    else:
        categories = session.query(Category).all()
        return render_template('newItem.html', categories=categories)

# Delete item
@app.route('/CategoryItem/delete/<int:categoryitem_id>', methods=['GET', 'POST'])
def DeleteCategoryItem(categoryitem_id):
    if 'username' not in login_session:
        return redirect(url_for('Categories'))
    item = session.query(CategoryItem).filter_by(id=categoryitem_id).one()
    if login_session['user_id'] != item.user_id:
        return redirect(url_for('Categories'))
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('Categories'))
    else:
        return render_template('deleteItem.html', item=item)

# Edit item
@app.route('/CategoryItem/edit/<int:categoryitem_id>', methods=['GET', 'POST'])
def EditCategoryItem(categoryitem_id):
    if 'username' not in login_session:
        return redirect(url_for('Categories'))
    item = session.query(CategoryItem).filter_by(id=categoryitem_id).one()
    if login_session['user_id'] != item.user_id:
        return redirect(url_for('Categories'))
    if request.method == 'POST':
        item.name = request.form['name'];
        item.description = request.form['Description'];
        item.category_id = request.form['category']
        return redirect(url_for('CategoryItemm', categoryitem_id=item.id))
    else:
        categories = session.query(Category).all()
        return render_template('EditItem.html', categories=categories, item=item)

# google api connection
@app.route('/gconnect', methods=['POST'])
def gconnect():
    code = request.data
    try:
        print("91")

        # connect to oauthFlow
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        print("98")

        # exception if can't open the json file .
        response = make_response(json.dump('Failed To authorization code.', 401))
        print("Exception of FlowEchangeError")
        response.headers['Content-Type'] = 'application/json'
        return response

    # get the access_token from the credentials.
    access_token = credentials.access_token

    # putting the access_token to the API
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()

    # Get the data from the Google API
    result = json.loads(h.request(url, 'GET')[1])

    # check if there is any errors
    if result.get('error') is not None:
        print(120)
        response = make_response(json.dump(result.get('error'), 50))
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    # check if the id of the User  is the same
    if result['user_id'] != credentials.id_token['sub']:
        response = make_response(json.dump("Token's User Id doesnt match given user id", 401))
        response.headers['Content-Type'] = 'application/json'
        return response

    # check if the Token is right
    if result['issued_to'] != client_id:
        response = make_response(json.dump("Token's Client doesnt match given user id", 401))
        print("Token's Client Id Does not match")
        response.headers['Content-Type'] = 'application/json'
        return response

    # check if already logged in
    stored_credential = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credential is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dump("Current user is already connected", 200))
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the credaintail and user_token
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get User Info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # save User Information
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserid(data['email'])
    if user_id is None:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    return redirect(url_for('Categories'))

# google api Disconnection
@app.route('/gdisconnect')
def disconnect():
    accesstoken = login_session.get('access_token')
    if accesstoken is None:
        response = make_response(json.dump('Curent User not connected', 401))
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('Categories'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('Categories'))


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserid(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
