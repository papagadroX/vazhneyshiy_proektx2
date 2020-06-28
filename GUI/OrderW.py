
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Server.Client import *


class OrdersWindow(QWidget):
    addButton = None
    rmvButton = None
    retButton = None
    table = None
    programChanged = False
    autoparkDict = {}
    customerDict = {}

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.setWindowTitle("Orders")
        self.fillCarInBox()
        self.fillBuyerInBox()
        self.createTable()
        self.addOrdButton()
        self.rmvOrdButton()
        self.returnButton()
        self.createLayout()

    def fillBuyerInBox(self):
        buyers = handleGetRequest('Get all customers')
        for buyer in buyers.items():
            self.customerDict[int(buyer[0])] = buyer[1]

    def fillCarInBox(self):
        messages = handleGetRequest('Get all autopark')
        for message in messages.items():
            self.autoparkDict[int(message[0])] = message[1][1]

    def removeOrder(self):
        row = self.table.currentRow()
        orderId = int(self.table.item(row, 0).text())
        if handleDeleteRequest(f'Remove order {orderId}'):
            self.table.removeRow(row)

    def addOrder(self, row):
        self.programChanged = True
        carId = []
        buyerId = []
        count = self.table.rowCount()
        self.table.insertRow(count)
        boxCar = QComboBox()
        self.FillBoxCar(None, boxCar)
        self.table.setCellWidget(count, 1, boxCar)
        boxBuyer = QComboBox()
        self.FillBoxBuyer(None, boxBuyer)
        self.table.setCellWidget(count, 2, boxBuyer)
        for id in self.autoparkDict:
            carId.append(id)
        for id in self.customerDict:
            buyerId.append(id)

        new_order = {'car_id': carId[0], 'buyer_id': buyerId[0]}
        order = handleAddRequest('Add order', new_order)
        idWidget = QTableWidgetItem(str(order))
        idWidget.setFlags(Qt.ItemIsSelectable)
        self.table.setItem(count, 0, idWidget)
        self.programChanged = False

    def createTable(self):
        self.table = QTableWidget(self)
        self.table.setGeometry(20, 20, 800, 600)
        self.table.setMinimumSize(400, 400)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Id",
                                              "Car",
                                              "Buyer"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 75)
        self.table.setColumnWidth(1, 325)
        self.table.setColumnWidth(2, 325)
        self.table.cellChanged.connect(self.OnTableChanged)
        self.FillTableFromDataBase()

    def addOrdButton(self):
        self.addButton = QPushButton(self)
        self.addButton.setGeometry(20, 20, 120, 60)
        self.addButton.setText('Добавить заказ')

    def rmvOrdButton(self):
        self.removeButton = QPushButton(self)
        self.removeButton.setGeometry(20, 20, 120, 60)
        self.removeButton.setText('Удалить заказ')

    def returnButton(self):
        self.retButton = QPushButton(self)
        self.retButton.setGeometry(100, 100, 120, 100)
        self.retButton.setMinimumSize(200, 50)
        self.retButton.setText('Автомобили')

    def createLayout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.table, 0, Qt.AlignTop)
        hbox = QHBoxLayout()
        hbox.addWidget(self.addButton)
        hbox.addWidget(self.removeButton)
        vbox.addLayout(hbox)
        vbox.addStretch()
        vbox.addWidget(self.retButton, 0, Qt.AlignCenter)
        vbox.addStretch()
        self.setLayout(vbox)

    def AddOrderInTable(self, order_id, order_car_id, order_buyer_id):
        count = self.table.rowCount()
        self.table.insertRow(count)
        idWidget = QTableWidgetItem(str(order_id))
        idWidget.setFlags(Qt.ItemIsSelectable)
        self.table.setItem(count, 0, idWidget)
        boxCar = QComboBox()
        self.FillBoxCar(order_car_id, boxCar)
        self.table.setCellWidget(count, 1, boxCar)
        boxBuyer = QComboBox()
        self.FillBoxBuyer(order_buyer_id, boxBuyer)
        self.table.setCellWidget(count, 2, boxBuyer)

    def onCarChanged(self):
        self.OnTableChanged(self.table.currentRow(), 0)

    def onBuyerChanged(self):
        self.OnTableChanged(self.table.currentRow(), 0)

    def OnTableChanged(self, row, column):
        if self.programChanged:
            return None
        self.programChanged = True
        boxCar = self.table.cellWidget(row, 1)
        carId = boxCar.currentData()
        boxBuyer = self.table.cellWidget(row, 2)
        buyerId = boxBuyer.currentData()
        new_order = {}
        new_order['id'] = int(self.table.item(row, 0).text())
        new_order['car_id'] = carId
        new_order['buyer_Id'] = buyerId
        handleUpdateRequest('Update order', new_order)
        self.programChanged = False

    def FillBoxCar(self, car, box=QComboBox):
        box.currentIndexChanged.connect(self.onCarChanged)
        count = 0
        index = 0
        for id in self.autoparkDict:
            if car is not None:
                if id == int(car):
                    index = count
            box.addItem(self.autoparkDict[id], id)
            count = count + 1
        box.setCurrentIndex(index)

    def FillBoxBuyer(self, buyer, box=QComboBox):
        box.currentIndexChanged.connect(self.onBuyerChanged)
        count = 0
        index = 0
        for id in self.customerDict:
            if buyer is not None:
                if id == int(buyer):
                    index = count
            box.addItem(self.customerDict[id], id)
            count = count + 1
        box.setCurrentIndex(index)

    def clearTable(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

    def FillTableFromDataBase(self):
        self.programChanged = True
        self.clearTable()
        messages = handleGetRequest('Get all orders')
        for message in messages.items():
            self.AddOrderInTable(message[0], message[1][0], message[1][1])
        self.programChanged = False

