from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from view.components.register_view import RegisterWindow
from view.qtsrc.login_ui import Ui_Dialog
class LoginWindow(QDialog, Ui_Dialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller
        self.loginButton.clicked.connect(self.do_login)
        self.backButton.clicked.connect(self.reject)
        self.registerButton.clicked.connect(self.open_register)
    def do_login(self):
        user = self.controller.login(
            self.username.text(),
            self.password.text()
        )
        if user:
            self.controller.user = user
            self.accept()
            # закрыть с результатом "успех"
        else:
            self.statusText.setText("Incorrect credentials")
            self.username.setStyleSheet("border: 1px solid red;")
            self.password.setStyleSheet("border: 1px solid red;")
    def open_register(self):
        dialog = RegisterWindow(self.controller)
        result = dialog.exec_()