
from ORM.BaseModel import *
from ORM.Company import Company
from ORM.BodyType import *
from peewee import *


class CarModel(BaseModel):
    id = AutoField()
    model_name = CharField()
    company_id = ForeignKeyField(Company)
    bodytype_id = ForeignKeyField(BodyType)
    price = IntegerField()

    @staticmethod
    def add(model_name, company_id,  bodytype_id, price):
        company = Company.get(Company.id == company_id)
        model = CarModel.create(model_name=model_name,
                                price=price,
                                bodytype_id=bodytype_id,
                                company_id=company.id)
        return model

    @staticmethod
    def find(id):
        if CarModel.select().where(CarModel.id == id).exists():
            return CarModel.get(CarModel.id == id)

    @staticmethod
    def getAllModel() -> list:
        query = CarModel.select()
        ls = []
        for model in query:
            ls.append(model)
        return ls
