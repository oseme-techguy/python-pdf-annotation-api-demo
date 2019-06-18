"""Sql Helper class

"""

class Sql:

    def __init__(self, logger=None, database_connection=None, sql_model=None):
        self.database = database_connection
        self.database.create_tables([sql_model])
        self.sql_model = sql_model(logger, database_connection)

    def get_model_instance(self):
        return self.sql_model
