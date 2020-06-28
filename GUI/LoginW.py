
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class LoginWindow(QWidget):
    button = None
    textfield = None
    label = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.setWindowTitle("Car park authorisation")
        self.createButton()
        self.createTextField()
        self.createLabel()
        self.createLayout()

    def createLayout(self):
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.label, 0, Qt.AlignCenter)
        vbox.addWidget(self.textfield, 0, Qt.AlignCenter)
        vbox.addWidget(self.button, 0, Qt.AlignCenter)
        vbox.addStretch()
        self.setLayout(vbox)

    def createButton(self):
        self.button = QPushButton(self)
        self.button.setGeometry(20, 20, 120, 20)
        self.button.setText('Войти')

    def createTextField(self):
        self.textfield = QLineEdit(self)
        self.textfield.setGeometry(20, 20, 120, 20)
        self.textfield.setMaximumSize(120, 25)

    def createLabel(self):
        self.label = QLabel(self)
        self.label.setGeometry(20, 20, 120, 20)
        self.label.setText('Введите логин')
        self.label.move(200, 200)
