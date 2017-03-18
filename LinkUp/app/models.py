from app import app, db, UserMixin
from hashlib import md5

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=True)
    website = db.Column(db.String(64))
    bio = db.Column(db.String(120))
    events = db.relationship('Event', backref='author', lazy='dynamic')
    followed = db.relationship('User',
                                    secondary=followers,
                                    primaryjoin=(followers.c.follower_id == id),
                                    secondaryjoin=(followers.c.followed_id == id),
                                    backref=db.backref('followers', lazy='dynamic'),
                                    lazy='dynamic'
                                )
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    # This method is to be changed to give sugestions
    @staticmethod
    def make_unique_username(username):
        if User.query.filter_by(username=username).first() is None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.query.filter_by(username=new_username).first() is None:
                break
                version +=1
        return new_username

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_events(self):
        # this query is to be edited
        return Event.query.join(followers, (followers.c.followed_id == Event.user_id)).filter(followers.c.follower_id == self.id).order_by(Event.id.desc())

    # def events(self, user):
    #     return self.events

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.social_id.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Event(db.Model):
    __searchable__ = ['name', 'venu', 'description', 'category']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(120))
    venu = db.Column(db.String(64))
    date = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    admission = db.Column(db.String(20), default='free')
    category = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Event %r>' % (self.name)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    latitue = db.Column(db.DECIMAL(6,4)) # -90 tp 90 degrees south pole to north pole
    longitude = db.Column(db.DECIMAL(7,4)) # -180 to 180 degress west to east

    def __repr__(self):
        return '<Location %r>' % (self.name)

if enable_search:
    whooshalchemy.whoosh_index(app, Event)
