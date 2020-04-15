from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from passhandler import *
from databaseinterface import *
import sys
from datetime import datetime, timedelta

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
        global dbpassword
        pass
    def start_menu(self):
        self.startmenu = StartMenu()
        self.startmenu.switch_to_servicewindow.connect(self.service_list)
        self.startmenu.switch_to_servicewindow.connect(self.close_startmenu)
        self.startmenu.show()

    def service_list(self):
        self.servicelist = ServiceList()
        self.servicelist.switch_to_startmenu.connect(self.start_menu)
        self.servicelist.switch_to_startmenu.connect(self.close_servicelist)
        self.servicelist.switch_to_newpassword.connect(self.new_password)
        self.servicelist.switch_to_newpassword.connect(self.close_servicelist)
        self.servicelist.switch_to_newservice.connect(self.new_service)
        self.servicelist.switch_to_newservice.connect(self.close_servicelist)
        self.servicelist.switch_to_service_passlist.connect(self.database_passwindowload)
        self.servicelist.switch_to_service_passlist.connect(self.close_servicelist)
        self.servicelist.show()

    def new_service(self):
        self.newservice = NewService()
        self.newservice.switch_to_servicewindow.connect(self.service_list)
        self.newservice.switch_to_servicewindow.connect(self.close_newservice)
        self.newservice.switch_to_startmenu.connect(self.start_menu)
        self.newservice.switch_to_startmenu.connect(self.close_newservice)
        self.newservice.new_service_confirmation.connect(self.new_serviceconfirmation)
        self.newservice.show()

    def new_password(self):
        self.newpassword = NewPassword() # Make class
        self.newpassword.switch_to_servicewindow.connect(self.service_list)
        self.newpassword.switch_to_servicewindow.connect(self.close_newpassword)
        self.newpassword.switch_to_databasepasswindowsave.connect(self.database_passwindowsave)
        self.newpassword.switch_to_databasepasswindowsave.connect(self.close_newpassword)
        self.newpassword.show()

    def database_passwindowload(self):
        self.databasepasswindowload = DatabasePassWindowLoad()
        self.databasepasswindowload.close_databasepasswindowload.connect(self.close_database_passwindowload)
        self.databasepasswindowload.servicepasslist.connect(self.service_passlist)
        self.databasepasswindowload.show()

    def service_passlist(self):
        self.servicepasslist = ServicePassList()
        self.servicepasslist.switch_to_startmenu.connect(self.start_menu)
        self.servicepasslist.updatelist()
        self.servicepasslist.show()

    def database_passwindowsave(self):
        self.databasepasswindowsave = DatabasePassWindowSave()
        self.databasepasswindowsave.close_databasepasswindowsave.connect(self.close_database_passwindowsave)
        self.databasepasswindowsave.show()

    def close_startmenu(self):
        self.startmenu.close()

    def close_servicelist(self):
        self.servicelist.close()

    def close_newservice(self):
        self.newservice.close()

    def close_database_passwindowload(self):
        #self.dbpassword = self.databasepasswindowload.dbpassword
        self.service_passlist()
        self.databasepasswindowload.close()

    def close_database_passwindowsave(self):
        self.databasepasswindowsave.close()

    def new_serviceconfirmation(self):
        self.newserviceconfirmation = NewServiceConfirmation()
        self.newserviceconfirmation.show()

    def close_newpassword(self):
        self.newpassword.close()



class StartMenu(QtWidgets.QWidget):
    switch_to_servicewindow = QtCore.pyqtSignal()
    switch_to_loadpasswordswindow = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Robbie's Password Manager")
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        #self.layout.setAlignment(alignment = QtCore.Qt.AlignCenter)
        #define widgets items
        self.image = QtWidgets.QLabel(self)
        self.pixmap = QPixmap('source.gif')
        self.image.setPixmap(self.pixmap)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.label = QtWidgets.QLabel("<br><h1>Welcome to Robbie's easy Password Manager</h1><br>This tool securely salts and hashes usernames and passwords and saves them in an SQL database. <br><br>-------------------<br> <br><b>This has not been completely security checked so I would not recommend you use this for BAU.</b> <br><br>-------------------<br><br>  Click Next to get started! <br>")
        self.label.setTextFormat(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.button = QtWidgets.QPushButton("Next!")
        self.button.clicked.connect(self.service_list)
        #add widgets to layout
        layout.addWidget(self.image)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

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
        self.resize(800,600)
        self.setWindowTitle("Robbie's Password Manager")
        layout = QtWidgets.QGridLayout()
        self.allservices = select_service_table(database)
        ##if None in the database then show nothing. "Nothing in database"

        #print(self.allservices)
        #define widgets items
        self.headers = self.allservices[0]+("number of passwords saved",)
        #print(self.headers)
        rows= self.allservices[1:]
        for i in range(len(rows)):
            row = rows[i]
            service_id = row[0]
            passwordcount = count_passwords(database,service_id)
            row = row + tuple(str(passwordcount))
            rows[i]=row
        #print(rows)
        self.model = TableModel(rows, self.headers)
        self.table = QtWidgets.QTableView()
        self.table.clicked.connect(self.clickedserviceid)
        # self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        # self.table.resizeColumnToContents(1)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setModel(self.model)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        layout.addWidget(self.table)

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
    def new_password(self):
        global service_id
        if service_id != 0:
            self.switch_to_newpassword.emit()
            return service_id

    def new_service(self):
        self.switch_to_newservice.emit()
    def service_passlist(self):
        global service_id
        if service_id != 0:
            self.switch_to_service_passlist.emit()
            return service_id

    def clickedserviceid(self, signal):
        global service_id
        row = signal.row()
        service_id = str(signal.sibling(signal.row(),0).data())
        print(service_id)
        return service_id

class NewPassword(QtWidgets.QWidget):
    switch_to_servicewindow = QtCore.pyqtSignal()
    new_password_confirmation = QtCore.pyqtSignal()
    switch_to_databasepasswindowsave = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        global now
        global expiry_time
        self.setWindowTitle("Add a new password to the selected service")
        layout = QtWidgets.QGridLayout()

        # columns required: id, usernamehash, passwordhash, salt, service_id, creation_date, expiry_date

        self.label = QtWidgets.QLabel("\n\nEnter credentials of new password to be stored securely in the database for the service: "+service_id+" : ")
        self.userlabel = QtWidgets.QLabel("Username")
        self.username = QtWidgets.QLineEdit()
        self.passlabel = QtWidgets.QLabel("Password")
        self.password = QtWidgets.QLineEdit()
        now = str(datetime.now().isoformat())
        expiry_time = str((datetime.now() + timedelta(days=90)).isoformat())
        self.datelabel = QtWidgets.QLabel("Service will be created with the following date/time:\nCreation time: "+now+"\nExpiry date/time: "+expiry_time)


        self.createpasswordbutton = QtWidgets.QPushButton("Create Service in database")
        self.createpasswordbutton.clicked.connect(self.create_password)
        self.backbutton = QtWidgets.QPushButton("Back")
        self.backbutton.clicked.connect(self.back_button)

        layout.addWidget(self.label)
        layout.addWidget(self.userlabel)
        layout.addWidget(self.username)
        layout.addWidget(self.passlabel)
        layout.addWidget(self.password)
        layout.addWidget(self.datelabel)
        layout.addWidget(self.createpasswordbutton)
        layout.addWidget(self.backbutton)
        self.setLayout(layout)

    def create_password(self):
        ###database call here.
        global usernameinput
        usernameinput= self.username.text()
        global passwordinput
        passwordinput = self.password.text()
        self.switch_to_databasepasswindowsave.emit()
        #passcontroller =Controller()
        #passcontroller.database_passwindowsave()


    def back_button(self):
        self.switch_to_servicewindow.emit()



class NewService(QtWidgets.QWidget):
    switch_to_servicewindow = QtCore.pyqtSignal()
    switch_to_startmenu = QtCore.pyqtSignal()
    new_service_confirmation = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Add a new service to the database")
        layout = QtWidgets.QGridLayout()
        self.label = QtWidgets.QLabel("\n\nEnter name of new service to add to the database:")
        self.service_name = QtWidgets.QLineEdit()
        self.createservicebutton = QtWidgets.QPushButton("Create Service in database")
        self.createservicebutton.clicked.connect(self.create_service)
        self.now = str(datetime.now().isoformat())
        #no expiry included on service table
        #self.expiry_time = (datetime.now() + timedelta(days=90)).isoformat()
        self.datelabel = QtWidgets.QLabel("Service will be created with the following date/time:\nCreation time: "+self.now)
        self.backbutton = QtWidgets.QPushButton("Back")
        self.backbutton.clicked.connect(self.back_button)
        layout.addWidget(self.label)
        layout.addWidget(self.service_name)
        layout.addWidget(self.datelabel)
        layout.addWidget(self.createservicebutton)
        layout.addWidget(self.backbutton)
        self.setLayout(layout)

    def back_button(self):
        self.switch_to_servicewindow.emit()

    def create_service(self):
        global new_service_name
        new_service_name = self.service_name.text()
        service = [new_service_name,self.now]
        global service_id
        service_id = service_creation(database,service)
        print("Service created with service_id = "+str(service_id))
        self.new_service_confirmation.emit()
        self.switch_to_servicewindow.emit()

class DatabasePassWindowSave(QtWidgets.QWidget):
    close_databasepasswindowsave = QtCore.pyqtSignal()
    servicepasslist = QtCore.pyqtSignal() #connect this signal to the update of the database password list view.
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
        global dbpassword
        global now
        global expiry_time
        dbpassword = self.password.text().encode()
        #self.servicepasslist
        self.servicepasslist.emit()
        self.close_databasepasswindowsave.emit()
        salt = os.urandom(16)
        #dbpassword=b"1234"
        passhash = hash(dbpassword, passwordinput.encode(), salt)
        userhash = hash(dbpassword, usernameinput.encode(), salt)
        identity = userhash, passhash, salt, service_id, now, expiry_time
        new_password_id = password_creation(database,identity)
        #return dbpassword

    def cancel_button(self):
        self.close_databasepasswindowsave.emit()


class DatabasePassWindowLoad(QtWidgets.QWidget):
    close_databasepasswindowload = QtCore.pyqtSignal()
    servicepasslist = QtCore.pyqtSignal() #connect this signal to the update of the database password list view.
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
        global dbpassword
        dbpassword = self.password.text()
        #self.servicepasslist
        self.servicepasslist.emit()
        self.close_databasepasswindowload.emit()

    def cancel_button(self):
        self.close_databasepasswindowload.emit()

class NewServiceConfirmation(QtWidgets.QWidget):
    close_databasepasswindowload = QtCore.pyqtSignal()
    servicepasslist = QtCore.pyqtSignal() #connect this signal to the update of the database password list view.
    def __init__(self):
        global new_service_name
        global service_id
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("New Service Created Successfully")
        layout = QtWidgets.QGridLayout()
        self.label = QtWidgets.QLabel("\nNew Service created with name: "+str(new_service_name)+"\nService Id: "+str(service_id))
        layout.addWidget(self.label)
        self.setLayout(layout)

class ServicePassList (QtWidgets.QWidget):
    switch_to_startmenu = QtCore.pyqtSignal()

    def __init__(self,):
        global dbpassword
        QtWidgets.QWidget.__init__(self)
        if type(dbpassword) != bytes:
            dbpassword = dbpassword.encode('utf-8')
        #print(self.dbpassword)
        self.resize(600,300)
        self.setWindowTitle("Service Password List")
        #self.layout = QtWidgets.QGridLayout()
        #self.setLayout(self.layout)

    def updatelist(self):
        global dbpassword
        self.layout = QtWidgets.QGridLayout()
        if type(dbpassword) != bytes:
            dbpassword= dbpassword.encode('utf-8')
        #self.listtable = QtWidgets.QListWidget()
        rows= select_all_service_passwords(database,service_id)
        print(rows)
        print(type(rows))
        for i in range(len(rows)):
            row = rows[i]
            self.serv_id, self.serv_name, self.pass_id, self.usernamehash, self.passwordhash, self.salt, self.expiry_date = row
            self.password = dehash(dbpassword, self.passwordhash, self.salt)
            self.username = dehash(dbpassword, self.usernamehash, self.salt)
            unencrypted_row = self.serv_id, self.serv_name, self.pass_id, self.username, self.password, self.salt, self.expiry_date
            rows[i] = unencrypted_row
        self.headers = ["service id","service name","password id","username","password","salt","password expiry date"]
        self.model = TableModel(rows,self.headers)

        self.table = QtWidgets.QTableView()
        self.table.clicked.connect(self.viewClicked)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setModel(self.model)
        self.table.horizontalHeader()
        self.layout.addWidget(self.table)
        #self.layout.addWidget(self.listtable)
        self.setLayout(self.layout)


    def viewClicked(self, clickedIndex):
        row = clickedIndex.row()
        model = clickedIndex.model()

'''Below Table Model class taken from example here: https://www.learnpyqt.com/courses/model-views/qtableview-modelviews-numpy-pandas/

"headerData" and "sort" are from https://stackoverflow.com/questions/52332534/column-sorting-not-working-when-using-custom-headerview

Docs require the subclassing of the PyQT5 Abstract Table model class
'''
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data,headerdata):
        super(TableModel, self).__init__()
        self._data = data
        self.headerdata = headerdata

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, col, orientation, role):
        if orientation==QtCore.Qt.Horizontal and role==QtCore.Qt.DisplayRole:
            return self.headerdata[col]
        return None

    def sort(self,col,order):
        self.layoutAboutToBeChanged.emit()
        self.arraydata=sorted(self.arraydata,key=operator.itemgetter(col))
        if order==QtCore.Qt.DescendingOrder:
            self.arraydata.reverse()
        self.layoutChanged.emit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.start_menu()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



