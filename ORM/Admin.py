from peewee import *
from ORM.BaseModel import BaseModel


class Admin(BaseModel):
    id = AutoField()
    name = CharField()

    @staticmethod
    def getAllAdmin() -> list:
        query = Admin.select()
        ls = []
        for admin in query:
            ls.append(admin)
        return ls
