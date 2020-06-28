from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Server.Client import *
from GUI.OrderW import OrdersWindow


class AutoparkWindow(QWidget):
    acButton = None
    ordButton = None
    fdButton = None
    fdLabel = None
    fdEdit = None
    rmvButton = None
    table = None
    bodyTypeDict = {}
    programChanged = False
    companyDict = {}
    customerDict = {}
    carIdToRow = {}
    orderWindow = None

    def __init__(self, _orderWindow=OrdersWindow):
        super().__init__()
        self.orderWindow = _orderWindow
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.setWindowTitle("Cars")
        self.addCarButton()
        self.ordersButton()
        self.findWidgets()
        self.removeButton()
        self.fillBodyTypeInBox()
        self.fillCompanyInBox()
        self.fillCustomerInBox()
        self.initTable()
        self.createLayout()
        self.handler()

    def handler(self):
        self.fdEdit.textChanged.connect(self.redrawTable)

    def redrawTable(self):
        if not self.fdEdit.text() or self.fdEdit.text() is None:
            self.FillTableFromDataBase()

    def fillBodyTypeInBox(self):
        bodytypes = handleGetRequest('Get all bodytypes')
        for bodytype in bodytypes.items():
            self.bodyTypeDict[int(bodytype[0])] = bodytype[1]

    def fillCompanyInBox(self):
        companies = handleGetRequest('Get all companies')
        for company in companies.items():
            self.companyDict[int(company[0])] = company[1]

    def fillCustomerInBox(self):
        customers = handleGetRequest('Get all customers')
        for customer in customers.items():
            self.customerDict[int(customer[0])] = customer[1]

    def addCarButton(self):
        self.acButton = QPushButton(self)
        self.acButton.setGeometry(20, 20, 120, 60)
        self.acButton.setText('Добавить Машину')

    def addCar(self):
        self.programChanged = True
        count = self.table.rowCount()
        self.table.insertRow(count)
        idWidget = QTableWidgetItem("")
        idWidget.setFlags(Qt.ItemIsSelectable or Qt.ItemIsEditable)
        self.table.setItem(count, 0, idWidget)
        boxCompany = QComboBox()
        self.FillBoxBodyType(None, boxCompany)
        self.table.setCellWidget(count, 1, boxCompany)
        self.table.setItem(count, 2, QTableWidgetItem(""))
        boxCompany = QComboBox()
        self.FillBoxCompany(None, boxCompany)
        self.table.setCellWidget(count, 3, boxCompany)
        boxCustomer = QComboBox()
        self.FillBoxCustomer(None, boxCustomer)
        self.table.setCellWidget(count, 4, boxCustomer)
        self.table.setItem(count, 5, QTableWidgetItem("0"))
        self.table.setItem(count, 6, QTableWidgetItem("0"))
        self.table.setItem(count, 7, QTableWidgetItem("0"))
        self.programChanged = False

    @staticmethod
    def showError(text, additionalInfo):
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setText(text)
            msg.setWindowTitle("Ошибка")
            msg.setDetailedText(additionalInfo)
            msg.setStandardButtons(QMessageBox.Ok)

            retval = msg.exec_()
        except Exception as ex:
            print("Невозможно удалить машину, которая существует в заказах")

    def removeCar(self):
        try:
            row = self.table.currentRow()
            carId = int(self.table.item(row, 0).text())
            if handleDeleteRequest(f'Remove car {carId}'):
                self.table.removeRow(row)
                del self.orderWindow.carDict[carId]
                self.orderWindow.FillTableFromDataBase()
            else:
                AutoparkWindow.showError("Ошибка удаления машины", "Машина все еще есть в заказах")
        except Exception as ex:
            AutoparkWindow.showError("Ошибка удаления машины", str(ex))

    def findCar(self):
        text = self.fdEdit.text()
        if text != "":
            cars_by_carmodels = handleFindRequest(f'Find carmodels {text}')
            cars_by_bodytypes = handleFindRequest(f'Find bodytype {text}')
            cars_by_companys = handleFindRequest(f'Find company {text}')
            cars_by_customers = handleFindRequest(f'Find customer {text}')
            if cars_by_carmodels is not None:
                cars = cars_by_carmodels
            elif cars_by_bodytypes is not None:
                cars = cars_by_bodytypes
            elif cars_by_companys is not None:
                cars = cars_by_companys
            elif cars_by_customers is not None:
                cars = cars_by_customers
            else:
                return

            self.clearTable()
            self.table.insertRow(len(cars))
            for car in cars:
                self.AddCarInTable(car['id'], car['bodytype_id'], car['carmodel'], car['company_id'],
                                    car['customer_id'], car['year'], car['rating'], car['available'])

    def clearTable(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

    def ordersButton(self):
        self.ordButton = QPushButton(self)
        self.ordButton.setGeometry(100, 100, 120, 100)
        self.ordButton.setMinimumSize(200, 50)
        self.ordButton.setText('Заказы')

    def findWidgets(self):
        self.fdLabel = QLabel(self)
        self.fdLabel.setText("Поиск")
        self.fdLabel.move(20, 20)
        self.fdEdit = QLineEdit(self)
        self.fdEdit.setGeometry(20, 20, 200, 32)
        self.fdButton = QPushButton(self)
        self.fdButton.setGeometry(20, 20, 120, 60)
        self.fdButton.setText('Найти машину')

    def removeButton(self):
        self.rmvButton = QPushButton(self)
        self.rmvButton.setGeometry(20, 20, 120, 60)
        self.rmvButton.setText('Удалить машину')

    def createLayout(self):
        vbox = QVBoxLayout()
        findBox = QHBoxLayout()
        findBox.addWidget(self.fdLabel)
        findBox.addWidget(self.fdEdit)
        findBox.addWidget(self.fdButton)
        vbox.addLayout(findBox)
        vbox.addWidget(self.table, 0, Qt.AlignTop)
        hbox = QHBoxLayout()
        hbox.addWidget(self.acButton)
        hbox.addWidget(self.rmvButton)
        vbox.addLayout(hbox)
        vbox.addStretch()
        vbox.addWidget(self.ordButton, 0, Qt.AlignCenter)
        vbox.addStretch()
        self.setLayout(vbox)

    def initTable(self):
        self.createTable()
        self.table.cellChanged.connect(self.OnTableChanged)
        self.FillTableFromDataBase()

    def createTable(self):
        self.table = QTableWidget(self)
        self.table.setGeometry(20, 20, 800, 600)
        self.table.setMinimumSize(400, 400)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Id",
                                              "Bodytype",
                                              "Carmodel",
                                              "Company",
                                              "Customer",
                                              "Year"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 145)
        self.table.setColumnWidth(2, 181)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 169)
        self.table.setColumnWidth(5, 80)
        self.table.cellChanged.connect(self.OnTableChanged)
        self.FillTableFromDataBase()

    def AddCarInTable(self, car_id, bodytype_id, carmodel_id, company_id, customer_id, year, rating, available):
        i = 0
        count = self.table.rowCount()
        self.table.insertRow(count)
        self.carIdToRow[car_id] = count
        idWidget = QTableWidgetItem(str(car_id))
        idWidget.setFlags(Qt.ItemIsSelectable)
        self.table.setItem(count, i, idWidget)
        i = i + 1
        boxBodyType = QComboBox()
        boxBodyType.setMinimumWidth(161)
        self.FillBoxBodyType(bodytype_id, boxBodyType)
        self.table.setCellWidget(count, i, boxBodyType)
        i = i + 1
        self.table.setItem(count, i, QTableWidgetItem(carmodel_id))
        i = i + 1
        boxCompany = QComboBox()
        boxCompany.setMinimumWidth(100)
        self.FillBoxCompany(company_id, boxCompany)
        self.table.setCellWidget(count, i, boxCompany)
        i = i + 1
        boxCustomer = QComboBox()
        self.FillBoxCustomer(customer_id, boxCustomer)
        self.table.setCellWidget(count, i, boxCustomer)
        i = i + 1
        self.table.setItem(count, i, QTableWidgetItem(str(year)))
        i = i + 1
        self.table.setItem(count, i, QTableWidgetItem(str(rating)))
        i = i + 1
        self.table.setItem(count, i, QTableWidgetItem(str(available)))

    def onBodyTypeChanged(self):
        self.OnTableChanged(self.table.currentRow(), 0)

    def onCompanyChanged(self):
        self.OnTableChanged(self.table.currentRow(), 0)

    def onCustomerChanged(self):
        self.OnTableChanged(self.table.currentRow(), 0)

    def OnTableChanged(self, row, column):
        if self.programChanged:
            return None
        self.programChanged = True
        boxBodyType = self.table.cellWidget(row, 1)
        boxCompany = self.table.cellWidget(row, 3)
        boxCustomer = self.table.cellWidget(row, 4)
        if boxCustomer is None or boxCompany is None or boxBodyType is None:
            return
        boxCustomer.setFixedWidth(149)
        companyId = boxCompany.currentData()
        bodytypeId = boxBodyType.currentData()
        customerId = boxCustomer.currentData()
        item = self.table.item(row, 0).text()
        if self.table.item(row, 5).text() == "" or not self.table.item(row, 5).text().isdigit():
            self.table.item(row, 5).setText("0")
        if self.table.item(row, 6).text() == "" or not self.table.item(row, 6).text().isdigit():
            self.table.item(row, 6).setText("0")
        if self.table.item(row, 7).text() == "" or not self.table.item(row, 7).text().isdigit():
            self.table.item(row, 7).setText("0")

        new_car = dict()
        new_car['id'] = 0
        new_car['carmodel'] = self.table.item(row, 2).text()
        #new_car['rating'] = int(self.table.item(row, 6).text())
        new_car['year'] = int(self.table.item(row, 5).text())
        #new_car['available'] = int(self.table.item(row, 7).text())
        new_car['bodytype_Id'] = bodytypeId
        new_car['company_Id'] = companyId
        new_car['customer_Id'] = customerId

        if item:
            new_car['id'] = int(self.table.item(row, 0).text())
            handleUpdateRequest('Update car', new_car)
        else:
            car = handleAddRequest('Add car', new_car)

            self.table.item(row, 0).setText(str(car['id']))
            self.carIdToRow[car['id']] = row
            self.orderWindow.carDict[car['id']] = self.table.item(row, 2).text()
        self.FillTableFromDataBase()
        self.orderWindow.FillTableFromDataBase()
        self.programChanged = False

    def FillBoxBodyType(self, bodytype_id, box=QComboBox):
        box.currentIndexChanged.connect(self.onBodyTypeChanged)
        count = 0
        index = 0
        for id in self.bodyTypeDict:
            if bodytype_id is not None:
                if id == int(bodytype_id):
                    index = count
            box.addItem(self.bodyTypeDict[id], id)
            count = count + 1
        box.setCurrentIndex(index)

    def FillBoxCompany(self, company_id, box=QComboBox):
        box.currentIndexChanged.connect(self.onCompanyChanged)
        count = 0
        index = 0
        for id in self.companyDict:
            if company_id is not None:
                if id == int(company_id):
                    index = count
            box.addItem(self.companyDict[id], id)
            count = count + 1
        box.setCurrentIndex(index)

    def FillBoxCustomer(self, customer_id, box=QComboBox):
        box.currentIndexChanged.connect(self.onCustomerChanged)
        count = 0
        index = 0
        for id in self.customerDict:
            if customer_id is not None:
                if id == int(customer_id):
                    index = count
            box.addItem(self.customerDict[id], id)
            count = count + 1
        box.setCurrentIndex(index)

    def FillTableFromDataBase(self):
        self.programChanged = True
        self.clearTable()
        messages = handleGetRequest('Get all cars')
        self.orderWindow.carDict = {}
        for message in messages.items():
            self.AddCarInTable(message[0], message[1][0], message[1][1], message[1][2], message[1][3], message[1][4],
                                message[1][5], message[1][6])
            self.orderWindow.carDict[int(message[0])] = message[1][1]
        self.programChanged = False
