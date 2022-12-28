import os


SECRET_KEY = os.getenv('SECRET_KEY') or 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
SECURITY_PASSWORD_SALT = 'my_precious_two'
'''
POSTGRES = {
    'user': 'e202735',
    'pw': 'primera',
    'db': 'dkpython',
    'host': 'vmlx-postgresql-desa',
    'port': '5432',
}
'''


SQLALCHEMY_TRACK_MODIFICATIONS = False

#postgresql://username:password@hostname/database
#SQLAlchemy_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/trivia"

'''
SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES['user']}:" \
                          f"{POSTGRES['pw']}@{POSTGRES['host']}:" \
                          f"{POSTGRES['port']}/{POSTGRES['db']}"

'''
SQLALCHEMY_DATABASE_URI = 'sqlite:///apfa.db'

# configuraciones. True para que el servidor pueda ser levantado en modo debug
DEBUG = True
# configuraciones para Flask User
#USER_REGISTER_URL = '/apfa/register'
#USER_LOGIN_URL = '/apfa/login'
#USER_UNAUTHENTICATED_ENDPOINT = 'auth.login'
#USER_UNAUTHORIZED_ENDPOINT = 'auth.login'
USER_ENABLE_EMAIL=False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

MAIL_USERNAME = 'gcasavieja@gmail.com'
MAIL_PASSWORD = 'wiwqfaixrtnfclxb'

MAIL_DEFAULT_SENDER = 'gcasavieja@gmail.com'
MAIL_SUBJECT = "Por favor, confirme su registro."



