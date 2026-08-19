from PyQt5.QtWidgets import QDialog
from view.qtsrc.register_ui  import Ui_Dialog
class RegisterWindow(QDialog, Ui_Dialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller
        self.register_button.clicked.connect(self.register)
        self.b_register.clicked.connect(self.reject)
    def register(self):
        username = self.usernameLineEdit.text()
        password = self.usernameLineEdit.text()
        first_name = self.firstnameLineEdit.text()
        last_name = self.lastnameLineEdit.text()
        longitude = self.longitudeLineEdit.text()
        latitude = self.latitudeLineEdit.text()

