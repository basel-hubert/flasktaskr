import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True


# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri (can be overridden via the DATABASE_URL env var, e.g. for tests)
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + DATABASE_PATH)

SQLALCHEMY_TRACK_MODIFICATIONS = True