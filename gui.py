from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from passhandler import *
from databaseinterface import *
import sys
import time

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
service_id = 0
dbpassword = ""
#dbpassword = b"1234"
class Controller:
    def __init__(self):
        pass
    def start_menu(self):
        self.startmenu = StartMenu()
        self.startmenu.switch_to_servicewindow.connect(self.service_list)
        self.startmenu.switch_to_servicewindow.connect(self.close_startmenu)
        self.startmenu.show()

    def service_list(self):
        self.servicelist = ServiceList()
        self.servicelist.switch_to_startmenu.connect(self.start_menu)
        self.servicelist.switch_to_newpassword.connect(self.new_password)
        self.servicelist.switch_to_newservice.connect(self.new_service)
        self.servicelist.switch_to_service_passlist.connect(self.database_passwindowload)
        self.servicelist.switch_to_startmenu.connect(self.close_servicelist)
        self.servicelist.switch_to_newpassword.connect(self.close_servicelist)
        self.servicelist.switch_to_newservice.connect(self.close_servicelist)
        self.servicelist.switch_to_service_passlist.connect(self.close_servicelist)
        self.servicelist.show()

    def new_service(self):
        self.newservice = NewService()
        self.newservice.switch_to_servicewindow.connect(self.service_list)
        self.newservice.switch_to_startmenu.connect(self.start_menu)
        self.newservice.show()

    def new_password(self):
        self.newpassword = NewPassword() # Make class
        self.newpassword.switch_to_servicewindow.connect(self.service_list)
        self.newpassword.switch_to_databasepasswindowsave.connect(self.database_passwindowsave)
        self.newpassword.show()

    def database_passwindowload(self):
        self.databasepasswindowload = DatabasePassWindowLoad()
        self.databasepasswindowload.close_databasepasswindowload.connect(self.close_database_passwindowload)
        self.databasepasswindowload.show()

    def service_passlist(self):
        print(self.dbpassword)
        self.servicepasslist = ServicePassList(self.dbpassword)
        #print(self.dbpassword)
        #print(dbpassword)
        self.servicepasslist.switch_to_startmenu.connect(self.start_menu)
        self.servicepasslist.show()

    def database_passwindowsave(self):
        self.databasepasswindowsave = DatabasePassWindowSave()
        self.databasepasswindowsave.close_databasepasswindowload.connect(self.close_database_passwindowsave)
        self.databasepasswindowsave.show()

    def close_startmenu(self):
        self.startmenu.close()

    def close_servicelist(self):
        self.servicelist.close()

    def close_database_passwindowload(self):
        self.dbpassword = self.databasepasswindowload.dbpassword
        #print(self.dbpassword)
        #print("closing pass view")
        self.service_passlist()
        self.databasepasswindowload.close()

    def close_database_passwindowsave(self):
        #self.dbpassword = self.databasepasswindowload.dbpassword
        self.databasepasswindowsave.close()



class StartMenu(QtWidgets.QWidget):
    switch_to_servicewindow = QtCore.pyqtSignal()
    switch_to_loadpasswordswindow = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setWindowTitle("Robbie's Password Manager")
        layout = QtWidgets.QGridLayout()
        #define widgets items
        self.image = QtWidgets.QLabel(self)
        self.pixmap = QPixmap('source.gif')
        self.image.setPixmap(self.pixmap)
        self.label = QtWidgets.QLabel("\n\nWelcome to Robbie's easy Password Manager\n\n Click Next to get started! \n\n")
        self.button = QtWidgets.QPushButton("Next!")
        self.button.clicked.connect(self.service_list)
        #add widgets to layout
        layout.addWidget(self.image)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        #layout.addWidget(self.button2)
        #show layout
        self.setLayout(layout)

    def service_list(self):
        self.switch_to_servicewindow.emit()


class ServiceList(QtWidgets.QWidget):
    switch_to_startmenu = QtCore.pyqtSignal()
    switch_to_newpassword= QtCore.pyqtSignal()
    switch_to_newservice= QtCore.pyqtSignal()
    switch_to_service_passlist = QtCore.pyqtSignal()
    switch_to_databasepasswindowload = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.resize(600,300)
        self.setWindowTitle("Robbie's Password Manager")
        layout = QtWidgets.QGridLayout()
        #define widgets items
        self.listtable = QtWidgets.QListWidget()
        self.allservices = select_service_table(database)
        i=0
        for service in self.allservices:
            self.serv = '\t'.join(map(str, service))
            self.listtable.insertItem(i,self.serv)
            i += 1
        # self.listtable.insertItem(0,"Red")
        # self.listtable.insertItem(1, "Green")
        layout.addWidget(self.listtable)
        #buttons
        self.savepasswordbutton = QtWidgets.QPushButton("Save Password to Selected service")
        self.savepasswordbutton.clicked.connect(self.new_password)
        self.newservicebutton = QtWidgets.QPushButton("Create new Service")
        self.newservicebutton.clicked.connect(self.new_service)
        self.servicepasslistbutton = QtWidgets.QPushButton("Load Passwords for Selected service")
        self.servicepasslistbutton.clicked.connect(self.service_passlist)
        self.backbutton = QtWidgets.QPushButton("Back")
        self.backbutton.clicked.connect(self.start_menu)

        layout.addWidget(self.savepasswordbutton)
        layout.addWidget(self.newservicebutton)
        layout.addWidget(self.servicepasslistbutton)
        layout.addWidget(self.backbutton)
        #end buttons
        self.setLayout(layout)

    def start_menu(self):
        self.switch_to_startmenu.emit()
        #print(self.listtable.selectedItems()[0].text())
        #print(self.listtable.currentRow())
    def new_password(self):
        self.switch_to_newpassword.emit()
    def new_service(self):
        self.switch_to_newservice.emit()
    def service_passlist(self):
        global service_id
        if self.listtable.currentRow() != 0:
            self.switch_to_service_passlist.emit()
            service_id = self.listtable.currentRow()
            print(service_id)
            return service_id




class NewPassword(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)


class NewService(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

class DatabasePassWindowLoad(QtWidgets.QWidget):
    close_databasepasswindowload = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Please Enter Database Password")
        layout = QtWidgets.QGridLayout()
        self.label = QtWidgets.QLabel("\n\nEnter Database Password to get access:\n\n")
        layout.addWidget(self.label)
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(2)
        layout.addWidget(self.password)
        self.submitbutton = QtWidgets.QPushButton("Submit")
        self.submitbutton.clicked.connect(self.submit_button)
        self.cancelbutton = QtWidgets.QPushButton("Cancel")
        self.cancelbutton.clicked.connect(self.cancel_button)
        layout.addWidget(self.submitbutton)
        layout.addWidget(self.cancelbutton)
        self.setLayout(layout)

    def submit_button(self):
        self.dbpassword = self.password.text()
        self.close_databasepasswindowload.emit()

    def cancel_button(self):
        self.close_databasepasswindowload.emit()



class ServicePassList (QtWidgets.QWidget):
    switch_to_startmenu = QtCore.pyqtSignal()

    def __init__(self,dbpassword):
        QtWidgets.QWidget.__init__(self)
        self.dbpassword = dbpassword.encode('utf-8')
        print(self.dbpassword)
        self.resize(600,300)
        self.setWindowTitle("Service Password List")
        layout = QtWidgets.QGridLayout()
        #define widgets items
        self.listtable = QtWidgets.QListWidget()
        print(select_all_service_passwords(database,service_id))
        self.service_id, self.service_name, self.usernamehash, self.passwordhash, self.salt, self.expiry_date = select_all_service_passwords(
            database, service_id)

        print(dehash(self.dbpassword, self.passwordhash, self.salt))
        for i in range(length):
            passwords = 1

        i=0
        for password in self.allpasswords:
            self.serv = '\t'.join(map(str, password))
            self.listtable.insertItem(i,self.serv)
            i += 1
        # self.listtable.insertItem(0,"Red")
        # self.listtable.insertItem(1, "Green")
        layout.addWidget(self.listtable)
        self.setLayout(layout)

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.start_menu()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



