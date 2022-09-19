from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from settings_window import SettingsWindow
from register_wd import RegisterWindow
import sqlite3

# LoginWindow class that manages login and opening the setting window
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi('UI/login_window.ui', self)
        self.register_button.clicked.connect(self.go_to_register_page)
        self.login_button.clicked.connect(self.open_settings_window)

        self.show()
	
    # Open registration page
    def go_to_register_page(self):
        self.register_wd = RegisterWindow()
        self.register_wd.displayInfo()
        
	# Opens settings window, passes the received token and closes login window
    def open_settings_window(self):
        
        username = self.username_input.text().strip()
        password = self.password_input.text()

        conn = sqlite3.connect('wds_db')
        curs = conn.cursor()
        curs.execute('select * from uid where username=? and password=?',[username,password])
        if len(curs.fetchall()):
            self.settings_window = SettingsWindow()
            self.settings_window.displayInfo()
            self.close()
        else:
            print('User does not exist! Please register.')

        