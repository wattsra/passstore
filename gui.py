from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from passhandler import *
from databaseinterface import *
import sys

'''
ToDO:
Design and Implement GUI:
Save new password
Load services stored in table
Load specific password
load all passwords for specific service
'''


# temp variables
database = r"pass-store2.db"


class Controller:
    def __init__(self):
        pass
    def start_menu(self):
        self.startmenu = StartMenu()
        #self.startmenu.switch_window.connect(self.show_username)
        self.startmenu.switch_window.connect(self.close_startmenu)
        self.startmenu.switch_window.connect(self.load_passwords)
        self.startmenu.show()
    def close_startmenu(self):
        self.startmenu.close()

    def next_menu(self):
        self.nextmenu = NextMenu()
        #self.nextmenu.switch_window.connect(self.show_username)
        #self.nextmenu.switch_window.connect(self.close_startmenu)
        self.nextmenu.show()

    def load_passwords(self):
        self.loadpasswords = LoadPasswords()
        self.loadpasswords.show()


class StartMenu(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Robbie's Password Manager")
        layout = QtWidgets.QGridLayout()
        self.image = QtWidgets.QLabel(self)
        self.pixmap = QPixmap('source.gif')
        self.image.setPixmap(self.pixmap)
        layout.addWidget(self.image)
        self.label = QtWidgets.QLabel("\nWelcome to Robbie's easy Password Manager\nWhat would you like to do?:\n")
        self.button = QtWidgets.QPushButton("Save New Password")
        self.button.clicked.connect(self.nextmenu)
        self.button = QtWidgets.QPushButton("Load Password")
        self.button.clicked.connect(self.load_passwords)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def nextmenu(self):
        self.switch_window.emit()

    def load_passwords(self):
        self.switch_window.emit()
        ## Load all passwords using databaseinterface.py


class LoadPasswords(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Second Menu")
        layout = QtWidgets.QGridLayout()
        self.allservices = select_service_table(database)
        for service in self.allservices:
            self.serv = '\t'.join(map(str, service))
            self.labels = QtWidgets.QLabel(self.serv)
            layout.addWidget(self.labels)
            self.setLayout(layout)

class NextMenu(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Second Menu")
        layout = QtWidgets.QGridLayout()
        self.label = QtWidgets.QLabel(
            "\nIs this working?\n")
        self.button = QtWidgets.QPushButton("Looks like a yes to me!")
        self.button.clicked.connect(self.close)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

class SavePasswordMenu(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        ## Implement Save Password Gui here.

    #def


##Initial at gui below. to be implemented in QT

# def starting_window():
#     layout = QVBoxLayout()
#     layout.addWidget(QLabel(
#         "\nWelcome to Robbie's easy Password Manager\nWhat would you like to do?:\n"))
#     save_new_button = QPushButton('Save New Password')
#     save_new_button.clicked.connect(on_button_clicked)
#     layout.addWidget(save_new_button)
#     layout.addWidget(QPushButton('Retrieve Stored Password'))
#     window.setLayout(layout)
#     window.show()
# def on_button_clicked():
#     layout = new_service_window()
#     window.setLayout(layout)
#     window.show()
#     # alert = QMessageBox()
#     # alert.setText("What is the name of the service you would like to save a password for?:\n")
#     # alert.exec_()
#
# def new_service_window():
#     layout = QVBoxLayout()
#     layout.addWidget(QLabel(
#         "\nNew Layout\n"))
#     save_new_button = QPushButton('Save New Password')
#     save_new_button.clicked.connect(on_button_clicked)
#     layout.addWidget(save_new_button)
#     layout.addWidget(QPushButton('Retrieve Stored Password'))
#     return layout
#
# app = QApplication([])
# window = QWidget()
# layout = starting_window()
#
# app.exec_()






# app = QApplication([])
#
# label = QLabel('Hello World!')
#
# label.show()
#
# app.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.start_menu()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



