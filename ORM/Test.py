from ORM.Autopark import Autopark
from ORM.BaseModel import BaseModel
from ORM.BodyType import BodyType
from ORM.Company import Company
from ORM.Customer import Customer
from ORM.CarModel import *
from ORM.Order import Order
import peewee
import datetime



def test_add_autopark():
    Autopark.add(1, 2005)

def test_add_carmodel():
    CarModel.add("CX-9", 1,  1, 3000)

test_add_autopark()

