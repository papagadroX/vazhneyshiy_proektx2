from peewee import *
from ORM.BaseModel import BaseModel



class BodyType(BaseModel):
    id = AutoField()
    body_type = CharField()

    @staticmethod
    def add(body_type):
        type = BodyType.create(body_type=body_type)
        return type





    @staticmethod
    def getAllBodyType() -> list:
        query = BodyType.select()
        ls = []
        for type in query:
            ls.append(type)
        return ls