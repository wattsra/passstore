from PyQt5 import QtCore, QtWidgets
import sys

class Controller:
    def __init__(self):
        pass
    def start_menu(self):
        self.startmenu = StartMenu()
        #self.startmenu.switch_window.connect(self.show_username)
        self.startmenu.switch_window.connect(self.close_startmenu)
        self.startmenu.show()
    def close_startmenu(self):
        self.startmenu.close()

    def next_menu(self):
        self.nextmenu = NextMenu()
        #self.nextmenu.switch_window.connect(self.show_username)
        #self.nextmenu.switch_window.connect(self.close_startmenu)
        self.nextmenu.show()


class StartMenu(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Robbie's Password Manager")
        layout = QtWidgets.QGridLayout()
        self.label = QtWidgets.QLabel("\nWelcome to Robbie's easy Password Manager\nWhat would you like to do?:\n")
        self.button = QtWidgets.QPushButton("Save New Password")
        self.button.clicked.connect(self.nextmenu)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def nextmenu(self):
        self.switch_window.emit()

    def load_passwords(self):
        ## Load all passwords here




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


    def


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



