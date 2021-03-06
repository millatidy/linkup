#!env/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Event, Location

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def test_user_model(self):
        u1 = User(nickname='john', social_id='hkjasdf')
        u2 = User(nickname='man', social_id='haksdlf')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        u1 = User.query.get(1)
        u2 = User.query.get(2)
        assert u1.nickname == 'john'
        assert u2.nickname == 'man'

    def test_follow(self):
        u1 = User(nickname='john', social_id='hkjasdf')
        u2 = User(nickname='man', social_id='haksdlf')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'man'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'john'
        u = u1.unfollow(u2)
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    # def test_follow_posts(self):
    #     # make four users
    #     u1 = User(nickname='john', email='john@example.com')
    #     u2 = User(nickname='susan', email='susan@example.com')
    #     u3 = User(nickname='mary', email='mary@example.com')
    #     u4 = User(nickname='david', email='david@example.com')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     # make four posts
    #     utcnow = datetime.utcnow()
    #     p1 = Post(body="post from john", author=u1, timestamp=utcnow + timedelta(seconds=1))
    #     p2 = Post(body="post from susan", author=u2, timestamp=utcnow + timedelta(seconds=2))
    #     p3 = Post(body="post from mary", author=u3, timestamp=utcnow + timedelta(seconds=3))
    #     p4 = Post(body="post from david", author=u4, timestamp=utcnow + timedelta(seconds=4))
    #     db.session.add(p1)
    #     db.session.add(p2)
    #     db.session.add(p3)
    #     db.session.add(p4)
    #     db.session.commit()
    #     # setup the followers
    #     u1.follow(u1)  # john follows himself
    #     u1.follow(u2)  # john follows susan
    #     u1.follow(u4)  # john follows david
    #     u2.follow(u2)  # susan follows herself
    #     u2.follow(u3)  # susan follows mary
    #     u3.follow(u3)  # mary follows herself
    #     u3.follow(u4)  # mary follows david
    #     u4.follow(u4)  # david follows himself
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     db.session.commit()
    #     # check the followed posts of each user
    #     f1 = u1.followed_posts().all()
    #     f2 = u2.followed_posts().all()
    #     f3 = u3.followed_posts().all()
    #     f4 = u4.followed_posts().all()
    #     assert len(f1) == 3
    #     assert len(f2) == 2
    #     assert len(f3) == 2
    #     assert len(f4) == 1
    #     assert f1 == [p4, p2, p1]
    #     assert f2 == [p3, p2]
    #     assert f3 == [p4, p3]
    #     assert f4 == [p4]

    def test_check_saved_location(sefl):
        # changes must be made in the models.py otherwise test fails
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        l1 = Location(name='Harare', latitude="88", longitude='-90')
        assert not (Location.check_saved_location(l1.name, l1.latitude, l1.longitude))
        db.session.add(l1)
        db.session.commit()
        e1 = Event(name="Event 1", author=u,  venu=l1)
        l2 = Location(name='Harare', latitude="88", longitude='-90') # use l1 coordinates
        assert (Location.check_saved_location(l2.name, l2.latitude, l2.longitude))
        l3 = Location(name='Ruwa', latitude="-90", longitude='88') # revese coordinates
        assert not (Location.check_saved_location(l3.name, l3.latitude, l3.longitude))
        db.session.add(l3)
        db.session.commit()
        p2 = Event(name="Event 2", author=u,  venu=l1)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
