import os

DB_NAME = "database.db"
SECRET_KEY = 'carazinho'

# Producao
DATABASE_URL = "postgresql://salaoonline_user:vLkCiPFYWEXDUd3M9DVeNYYBrNXRdkJU@dpg-ciou026nqql4qa0jg33g-a.oregon-postgres.render.com/salaoonline"

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'

# Connect to production database
#SQLALCHEMY_DATABASE_URI = DATABASE_URL

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False