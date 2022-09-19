from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import sqlite3

class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        loadUi('UI/registeration_window.ui', self)
        self.register_buttonf.clicked.connect(self.go_to_login)
    
    def displayInfo(self):
        self.show()

    def go_to_login(self):
        
        username = self.uname_input.text().strip()
        email = self.email_input.text().strip()
        password = self.pswd_input.text()

        if username and email and password:
            conn = sqlite3.connect('wds_db')
            curs = conn.cursor()
            curs.execute('select * from uid where username=? and email=? and password=?',[username,email,password])
            if len(curs.fetchall()):
                print("User already exists! Please login.")
                conn.close()
                self.close()
            else:
                curs.execute('insert into uid values(?, ?, ?)',(username,email,password))
                conn.commit()
                conn.close()
                self.close()
        else:
            print("All the fields are mandatory")