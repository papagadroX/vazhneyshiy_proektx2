from peewee import *
from ORM.BaseModel import BaseModel
from ORM.CarModel import CarModel
from ORM.Company import Company
from ORM.BodyType import *


class Autopark(BaseModel):
    id = AutoField()
    model_id = ForeignKeyField(CarModel)
    registration_year = IntegerField()
    model=None
    company=None
    body_type = None

    @staticmethod
    def add(model_id, registration_year):
        model = CarModel.get(CarModel.id == model_id)
        autopark = Autopark.create(model_id=model.id,
                                   registration_year=registration_year)
        return autopark

    @staticmethod
    def remove(id=None, model_id=None):
        query = None
        try:
            if model_id is not None:
                query = Autopark.get(Autopark.model_id == model_id)
            elif id is not None:
                query = Autopark.get(Autopark.id == id)
            query.delete_instance()
            return True
        except Exception as ex:
            query.database.rollback()
            raise ex

    @staticmethod
    def find(id):
        if Autopark.select().where(Autopark.id == id).exist():
            return Autopark.get(Autopark.id == id)



    def getCarModel(self) -> CarModel:
        self.model = CarModel.find(self.model_id)
        return self.model

    def getCompany(self) -> Company:
        model = CarModel.find(self.model_id)
        self.company = Company.find(model.company_id)
        return self.company
    def getBodyType(self) -> BodyType:
        model = CarModel.find(self.model_id)
        self.body_type = CarModel.find(model.bodytype_id)
        return self.body_type

    @staticmethod
    def find_by_model(model):
        auto = Autopark.select().where(Autopark.model_id == CarModel.select().where(CarModel.name == model)).dicts()
        if auto.exists():
            return auto

    @staticmethod
    def find_by_company(company):
        auto = Autopark.select().where(Autopark.model_id == CarModel.select().where(CarModel.company_id == CarModel.select().where(Company.company_name == company))).dicts()
        if auto.exists():
            return auto

    @staticmethod
    def update_carModel(id, new_model_id):
        Autopark.update(model_id=new_model_id).where(Autopark.id == id)

    @staticmethod
    def update_registration_year(id, new_registration_year):
        Autopark.update(registration_year=new_registration_year).where(Autopark.id == id).execute()

    @staticmethod
    def update_autopark(id, new_model_id, new_registration_year):
        Autopark.update(model_id=new_model_id, registration_year=new_registration_year).where(Autopark.id == id).execute()

    @staticmethod
    def getAllAutopark() -> list:
        query = Autopark.select()
        ls = []
        for auto in query:
            ls.append(auto)
        return ls




