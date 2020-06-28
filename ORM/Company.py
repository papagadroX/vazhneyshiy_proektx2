from peewee import *
from ORM.BaseModel import BaseModel

class Company(BaseModel):
    id = AutoField()
    company_name = CharField()

    @staticmethod
    def add(company_name):
        company_name=Company.create(company_name=company_name)
        return company_name

    @staticmethod
    def find(id):
        if Company.select().where(Company.id == id).exists():
            return Company.get(Company.id == id)

    @staticmethod
    def getAllCompany() -> list:
        query = Company.select()
        ls = []
        for company in query:
            ls.append(company)
        return ls
