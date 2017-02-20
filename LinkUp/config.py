import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'klfsalkfafasdfwrtpuier'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

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
OAUTH_CREDENTIALS = [
        'facebook' :{
            'id': '',
            'secrete': ''
        },
        'twitter' :{
            'id': '16NHDpcGdThjE9xamlW8ADGHj',
            'secret': 'gf5YRGfDyHxTo81fky4X2ltNhXugnYpHRmqNfYVlaIugx3WpWo'
        },
        'google' :{
            'id': '',
            'secret': ''
        }
]
