from peewee import *
from ORM.BaseModel import BaseModel
from ORM.Autopark import Autopark

class Customer(BaseModel):
    id = AutoField()
    full_name = CharField()


    @staticmethod
    def add(full_name):
        customer=Customer.create(full_name=full_name)
        return customer



    @staticmethod
    def getAllCustomer() -> list:
        query = Customer.select()
        ls = []
        for customer in query:
            ls.append(customer)
        return ls

    @staticmethod
    def find(id):
        if Customer.select().where(Customer.id == id).exists():
            return Customer.get(Customer.id == id)
