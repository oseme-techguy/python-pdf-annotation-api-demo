"""Base Model"""

from peewee import *
from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities


# myDB = pw.MySQLDatabase("mydb", host="mydb.crhauek3cxfw.us-west-2.rds.amazonaws.com", port=3306, user="user", passwd="password")


# Connect to a MySQL database on network.
# sql_db = MySQLDatabase('my_app', user='app', password='db_password',
#                      host='10.1.0.8', port=3316)
selected_database = MySQLDatabase(SETTINGS['sql']['connections']['database'],
                                host=SETTINGS['sql']['connections']['host'],
                                port=SETTINGS['sql']['connections']['port'],
                                user=SETTINGS['sql']['connections']['user'],
                                password=SETTINGS['sql']['connections']['password'])

class BaseModel(Model):
    """Base Model for the SQL db"""

    class Meta:
        database = selected_database
