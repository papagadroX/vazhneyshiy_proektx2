from ORM.Autopark import *
from ORM.BodyType import *
from ORM.Company import *
from ORM.Customer import *
from ORM.CarModel import *
from ORM.Order import *
from ORM.BaseModel import *
from peewee import *
from ORM.Admin import *
import json

import socketserver
from playhouse.shortcuts import model_to_dict
# db.connect()
# db.create_tables([Admin])

class TcpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        size = 1024
        data = self.request.recv(size).strip()
        temp = data.decode().split(' ')

        if 'Update autopark' in data.decode():
            autoparks = data.decode().replace('Update autopark', "")
            new_autopark = json.loads(autoparks)
            Autopark.update_autopark(int(new_autopark['id']),
                             int(new_autopark['model_id']),
                             int(new_autopark['registration_year']),)

        if 'Update order' in data.decode():
            order = data.decode().replace('Update order', "")
            new_order = json.loads(order)
            Order.update_order(int(new_order['id']),
                                int(new_order['customer_id']),
                                int(new_order['autopark_id']))

        if 'Add autopark' in data.decode():
            books = data.decode().replace('Add autopark', "")
            new_autopark = json.loads(books)
            auto = Autopark.add(new_autopark['model_id'],
                            int(new_autopark['registration_year']),
                            )
            self.request.send(json.dumps(model_to_dict(auto)).encode())

        if 'Add order' in data.decode():
            orders = data.decode().replace('Add order', "")
            new_order = json.loads(orders)
            order = Order.add(int(new_order['customer_id']), int(new_order['autopark_id']))
            self.request.send(json.dumps(order.id).encode())

        if data.decode() == 'Get all customers':
            response = Customer.getAllCustomer()
            self.getCustomersObject(response)

        if data.decode() == 'Get all bodytypes':
            response = BodyType.getAllBodyType()
            self.getBodyTypeObject(response)

        if data.decode() == 'Get all orders':
            response = Order.getAllOrder()
            print(response)
            dicts = {}

            for i in response:
                dicts[i.id] = []
                dicts[i.id].append(i.customer_id.id)
                dicts[i.id].append(i.autopark_id.id)
            self.request.send(json.dumps(dicts).encode())

        if data.decode() == 'Get all autopark':
            response = Autopark.getAllAutopark()
            dicts = {}
            for i in response:
                dicts[i.id] = []
                dicts[i.id].append(i.model_id.id)
                dicts[i.id].append(i.registration_year)

            self.request.send(json.dumps(dicts).encode())

        if data.decode() == 'Get all models':
            response = CarModel.getAllModel()
            self.getModelObject(response)



        if data.decode() == "Get logins":
            response = Admin.getAllAdmin()
            self.getLoginObject(response)

        if 'Remove' in temp:
            obj_id = int(temp[2])
            if temp[1] == 'autopark' and Autopark.remove(obj_id):
                self.request.send('Done'.encode())
            if temp[1] == 'order' and Order.remove(obj_id):
                self.request.send('Done'.encode())

        if 'Find' in temp:
            text = ' '.join(temp[2:])
            if "model" in temp:
                items = Autopark.find_by_model(text)
                self.findObjects(items)
            elif "company" in temp:
                items = Autopark.find_by_company(text)
                self.findObjects(items)




    def findObjects(self, items):
        if items is not None:
            items = [item for item in items]
            reply = json.dumps(items)
            self.request.send(reply.encode())

    def getCustomersObject(self, objects):
        dicts = {}

        for object in objects:
            dicts[object.id] = object.full_name



        self.request.send(json.dumps(dicts).encode())

    def getModelObject(self, objects):
        dicts = {}
        for object in objects:
            dicts[object.id] = object.model_name
        self.request.send(json.dumps(dicts).encode())

    def getLoginObject(self, objects):
        dicts = {}
        for object in objects:
            dicts[object.id] = object.name
        self.request.send(json.dumps(dicts).encode())


    def getBodyTypeObject(self, objects):
        dicts = {}
        for object in objects:
            dicts[object.id] = object.body_type
        self.request.send(json.dumps(dicts).encode())


if __name__ == "__main__":
    HOST, PORT = 'localhost', 8081
    with socketserver.TCPServer((HOST, PORT), TcpHandler) as server:
        server.serve_forever()
