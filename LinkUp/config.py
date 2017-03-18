import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'klfsalkfafasdfwrtpuier'

# SQLAlchemy database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Whoosh Alchemy config
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAXIMUM_SEARCH_RESULTS = 5

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['tidymilla@gmail.com']

# pagination
EVENTS_PER_PAGE = 3

# Open Outhentication
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '414921905507297',
        'secret': '56b26cc69dfc31264b978be2a7cd7c4a'
    },
    'twitter': {
        'id': '16NHDpcGdThjE9xamlW8ADGHj',
        'secret': 'gf5YRGfDyHxTo81fky4X2ltNhXugnYpHRmqNfYVlaIugx3WpWo'
    },
    'google': {
        'id': '223978344432-uo73c742n4skbchtbjp797871f0rveij.apps.googleusercontent.com',
        'secret': '6SCMQCVHcIMGkpYX_lYWuv7A'
    }
}
