"""
This file contains the functional tests for the routes.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import tempfile
import pytest
from config import basedir
from app import app,db,login
from app.models import User, Admin, Movie, Genre, MoviePoster, Post


@pytest.fixture(scope='module')
def test_client(request):
    #re-configure the app for tests
    app.config.update(
        SECRET_KEY = 'bad-bad-key',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        WTF_CSRF_ENABLED = False,
        DEBUG = True,
        TESTING = True,
    )
    db.init_app(app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()
 
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

@pytest.fixture
def new_user():
    user = User(username='Dwight', email='dwight.hanks@wsu.edu', password_hash='testing111')
    user.set_password('1234')
    return user

@pytest.fixture
def init_database(request,test_client):
    # Create the database and the database table
    db.create_all()
    # initialize the majors
    if Genre.query.count() == 0:
        genres = ['action', 'romance', 'comedy']
        for t in genres:
            db.session.add(Genre(name=t))
        db.session.commit()
    #add a user    
    user1 = User(username='Dwight', email='dwight.hanks@wsu.edu', password_hash='testing111')
    user1.set_password('testing111')
    # Insert user data
    db.session.add(user1)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()



def test_register_page(request,test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_register(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/register', 
                          data=dict(username='john', email='john@wsu.edu',password="bad-bad-password",password2="bad-bad-password"),
                          follow_redirects = True)
    assert response.status_code == 200

    s = db.session.query(User).filter(User.username=='john')
    assert s.count() == 1
    #assert b"Please log in to access this page." in response.data
    assert b"You have successfully registered!" in response.data
    #assert b"Sign In" in response.data   

def test_invalidlogin(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                          data=dict(username='Jerry', password='wrong', remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post('/login', 
                          data=dict(username='Dwight', password='1234', remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    #assert b"Hi, Dwight!" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    #assert b"Sign In" in response.data
    #assert b"Please log in to access this page." in response.data    

def test_newMovie(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs in,
    WHEN the '/createclass' page is requested (GET)  AND /createclass' form is submitted (POST)
    THEN check that response is valid and the class is successfully created in the database
    """
    #first login
    response = test_client.post('/login', 
                          data=dict(username='Dwight', password='1234',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    #assert b"Hi, Dwight!" in response.data
    
    #test the "create class" form 
    #response = test_client.get('/newMovie')
    #assert response.status_code == 200
    #assert b"Create a new movie" in response.data
    
    #test posting a class
    response = test_client.post('/newMovie', 
                          data=dict(title = 'Harry Potter', description = 'This is most famous movie'),
                          follow_redirects = True)
    assert response.status_code == 200
    #assert b"Your movie has been created!" in response.data
    #assert b"CptS 355 Roster" in response.data 
    c = db.session.query(Movie).filter(Movie.description == 'This is most famous movie')
    assert c.first().title == 'Harry Potter'
    assert c.count() == 1

    #finally logout
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
  #  assert b"Sign In" in response.data
   # assert b"Please log in to access this page." in response.data   


#def test_enroll(request,test_client,init_database):
#    """
#    GIVEN a Flask application configured for testing , after user logs in, and after a class is created
#    WHEN the '/enroll' form is submitted (POST)
#    THEN check that response is valid and the currently logged in user (student) is successfully added to roster
#    """
#    #first login
#    response = test_client.post('/login', 
#                          data=dict(username='sakire', password='1234',remember_me=False),
#                          follow_redirects = True)
#    assert response.status_code == 200
#   assert b"Hi, Sakire Arslan Ay!" in response.data
#   
    #create a class
#    response = test_client.post('/createclass', 
#                          data=dict(coursenum = '355', title = 'Programming Languages', major = 'CptS'),
#                         follow_redirects = True)
#    assert response.status_code == 200
#    c = db.session.query(Class).filter(Class.coursenum =='355')
#    assert c.count() == 1
#
    #enroll the logged in student in CptS 355
#    response = test_client.post('/enroll/'+str(c.first().id), 
#                        data=dict(),
#                        follow_redirects = True)
#   assert response.status_code == 200
#    assert b"You are now enrolled in class CptS 355!" in response.data
#    c = db.session.query(Class).filter(Class.coursenum =='355' and Class.major == 'CptS')
#    assert c.first().roster[0].username == 'sakire'
#
    #finally logout
#    response = test_client.get('/logout',                       
#                          follow_redirects = True)
#    assert response.status_code == 200
#    assert b"Sign In" in response.data
#    assert b"Please log in to access this page." in response.data   


# def test_login(request,test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/' page is requested (GET)
#     THEN check that the response is valid
#     """
#     response = test_client.post('/login', 
#                           data=dict(username='sakire', password='1234',remember_me=False),
#                           follow_redirects = True)
#     assert response.status_code == 200
#     assert b"Hi, Sakire Arslan Ay!" in response.data
