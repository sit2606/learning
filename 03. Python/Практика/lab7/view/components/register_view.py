from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QDialog, QMessageBox
from view.qtsrc.register_ui  import Ui_Dialog
class RegisterWindow(QDialog, Ui_Dialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller
        self.registerButton.clicked.connect(self.register)
        self.backButton.clicked.connect(self.reject)
        self.latitudeLineEdit.setValidator(QDoubleValidator(-90.0, 90.0, 6))
        self.longitudeLineEdit.setValidator(QDoubleValidator(-180.0, 180.0, 6))
    def register(self):
        username = self.usernameLineEdit.text()
        password = self.usernameLineEdit.text()
        first_name = self.firstnameLineEdit.text()
        last_name = self.lastnameLineEdit.text()
        longitude = float(self.longitudeLineEdit.text())
        latitude = float(self.latitudeLineEdit.text())
        if not (-180 <= longitude <= 180):
            QMessageBox.warning(self, "Error", "Latitude  should be a number between -90 and 90.")
            return self.reject
        if not (-90 <= latitude <= 90):
            QMessageBox.warning(self, "Error", "Latitude  should be a number between -90 and 90.")
            return self.reject
        user = self.controller.register(username, password, first_name, last_name, longitude, latitude)
        if user:
            QMessageBox.information(self, "Registration",
                                    "You're successfully registered. Please log in.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error",
                                "Please, provide other username.")