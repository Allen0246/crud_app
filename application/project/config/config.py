import os



SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
  os.getenv('POSTGRES_USER'),
  os.getenv('POSTGRES_PASSWORD'),
  os.getenv('POSTGRES_HOST'),
  os.getenv('POSTGRES_PORT'),
  os.getenv('POSTGRES_DB')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')

BCRYPT_LOG_ROUNDS = 12  # Configuration for the Flask-Bcrypt extension
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG_TB_INTERCEPT_REDIRECTS = False
LOG_PATH = '{0}/log/'.format(os.getenv('FLASK_PATH'))
if isinstance(os.getenv('LOG_BACKUP_COUNT'), int):
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT')) # days
else:
    LOG_BACKUP_COUNT = 0
LOG_LEVEL = 10

# if os.getenv('LOG_LEVEL') == 'CRITICAL':
#     LOG_LEVEL = 50
# elif os.getenv('LOG_LEVEL') == 'ERROR':
#     LOG_LEVEL = 40
# elif os.getenv('LOG_LEVEL') == 'WARNING':
#     LOG_LEVEL = 30
# elif os.getenv('LOG_LEVEL') == 'INFO':
#     LOG_LEVEL = 20
# elif os.getenv('LOG_LEVEL') == 'DEBUG':
#     LOG_LEVEL = 10
# else:
#     LOG_LEVEL = 10


