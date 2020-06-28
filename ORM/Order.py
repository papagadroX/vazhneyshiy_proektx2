from peewee import *
from ORM.BaseModel import BaseModel
from ORM.Customer import Customer
from ORM.Autopark import Autopark

class Order(BaseModel):
    id = AutoField()
    customer_id = ForeignKeyField(Customer)
    autopark_id = ForeignKeyField(Autopark)

    @staticmethod
    def add(customer_id, autopark_id):
        customer=Customer.get(Customer.id == customer_id)
        autopark = Customer.get(Autopark.id == autopark_id)


        order = Order.create(customer_id=customer.id,
                             autopark_id=autopark.id)
        return order


    @staticmethod
    def remove(id=None):
        query = None
        try:
            if id is not None:
                query = Order.get(Order.id == id)
            query.delete_instance()
            return True
        except Exception as ex:
            query.database.rollback()
            raise ex

    @staticmethod
    def find(id):
        if Order.select().where(Order.id == id).exist():
            return Order.get(Order.id == id)

    @staticmethod
    def update_order(id, new_customer_id, new_autopark_id):
        Order.update(customer_id=new_customer_id, autopark_id=new_autopark_id).where(
            Order.id == id).execute()

    @staticmethod
    def getAllOrder() -> list:
        query = Order.select()
        ls = []
        for order in query:
            ls.append(order)
        return ls
