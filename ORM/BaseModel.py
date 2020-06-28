from peewee import *


db = PostgresqlDatabase(database="postgres",
                        user="postgres",
                        password="12345678",
                        host="localhost")

class BaseModel(Model):
    database = db
    class Meta:
        database = db

