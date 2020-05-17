import os
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '/s3/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
