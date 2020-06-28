import sys

from PyQt5.QtWidgets import *

from GUI.LoginW import LoginWindow
from GUI.AutoparkW import AutoparkWindow
from GUI.OrderW import OrdersWindow
from Server.Client import *


class MainW(QMainWindow):
    ActiveWindow = None
    LoginWindow = None
    AutoparkWindow = None
    OrdersWindow = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.LoginWindow = LoginWindow()
        self.OrdersWindow = OrdersWindow()
        self.AutoparkWindow = AutoparkWindow(self.OrdersWindow)
        self.buttonHandler()
        self.ActiveWindow = self.LoginWindow

    def buttonHandler(self):
        self.LoginWindow.button.clicked.connect(self.loginButton)
        self.AutoparkWindow.ordButton.clicked.connect(self.OrdersWindow.show)
        self.AutoparkWindow.ordButton.clicked.connect(self.AutoparkWindow.close)
        self.AutoparkWindow.abButton.clicked.connect(self.AutoparkWindow.addCar)
        self.AutoparkWindow.rmvButton.clicked.connect(self.AutoparkWindow.removeCar)
        self.AutoparkWindow.fdButton.clicked.connect(self.AutoparkWindow.findCar)
        # self.OrdersWindow.rmvButton.clicked.connect(self.OrdersWindow.removeOrder)
        self.OrdersWindow.addButton.clicked.connect(self.OrdersWindow.addOrder)
        self.OrdersWindow.retButton.clicked.connect(self.AutoparkWindow.show)
        self.OrdersWindow.retButton.clicked.connect(self.OrdersWindow.close)

    def loginButton(self):
        librarians = handleGetRequest("Get logins")
        login = self.LoginWindow.textfield.text()
        if login and login in librarians.values():
            self.AutoparkWindow.show()
            self.LoginWindow.close()
        else:
            MainW.showError("Данного логина не существует")

    @staticmethod
    def showError(text):
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setText(text)
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)

            retval = msg.exec_()
        except Exception as ex:
            print("Ошибка авторизации")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainW()
    mw.ActiveWindow.show()
    sys.exit(app.exec())
