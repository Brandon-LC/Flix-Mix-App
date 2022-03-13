from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Admin, Movie, Genre, MoviePoster, Post

#Tests we need to run:
#   models
#   methods
#   write/ read data
#   routes(test_routes.py)

class MovieModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='Dwight', email='dwight.hanks@wsu.edu', password_hash='testing111')
        u.set_password('testing111')
        self.assertFalse(u.get_password('test'))
        self.assertTrue(u.get_password('testing111'))

    def test_Movie(self):
        m1 = Movie(title='Harry Potter', description='This is most famous movie')
        db.session.add(m1)
        db.session.commit()
        u1 = User(username='Dwight', email='dwight.hanks@wsu.edu')
        c1 = Genre(name='action')
        db.session.add(u1)
        db.session.add(c1)
        db.session.commit()

#        self.assertEqual(u1.movies.count(), 1)
        self.assertEqual(m1.title, 'Harry Potter')
        self.assertEqual(m1.description, 'This is most famous movie')

#        u1.delete(c1)
        db.session.commit()

        p1 = MoviePoster(image='Harry Potter 1st', img_type='png')
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(p1.image, 'Harry Potter 1st')
        self.assertEqual(p1.img_type, 'png')
        
    def test_Genre(self):
        g1 = Genre(name='Action')
        db.session.add(g1)
        db.session.commit()
        t1 = Movie(title='Harry Potter 4th')
        db.session.add(t1)
        db.session.commit()

    def test_MoviePoster(self):
        p1 = MoviePoster(image='Harry Potter 1st', img_type='png')
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(p1.image, 'Harry Potter 1st')
        self.assertEqual(p1.img_type, 'png')

    def test_Post(self):
        us1 = User(username='Dwight', email='dwight.hanks@wsu.edu')
#        user_name = us1
        db.session.add(us1)
        db.session.commit()
        self.assertEqual(us1.username, 'Dwight')
#        self.assertFalse(us1.username('Adam'))
#        self.assertTrue(us1.username('Dwight'))
        mp1 = Movie(id=2, title='Harry Potter 2nd')
        db.session.add(mp1)
        db.session.commit()
        ds1 = Post(body='This is nice movie.')
        db.session.add(ds1)
        db.session.commit()

# comment: Professor said Admin is not need test, more important is testing relationship between each class

if __name__ == '__main__':
    unittest.main(verbosity=2)