from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from view.qtsrc.user_ui  import Ui_UserDetailsDialog
class UserDetail(QDialog, Ui_UserDetailsDialog):
    on_update_view = pyqtSignal()
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller
        self.usernamelineEdit.setText(controller.user.username)
        self.firstnamelineEdit.setText(controller.user.firstname)
        self.lastnamelineEdit.setText(controller.user.lastname)
        self.latitudelineEdit.setText(str(controller.user.latitude))
        self.longitudelineEdit.setText(str(controller.user.longitude))
        self.logoutpushButton.clicked.connect(self._logout)
        self.backpushButton.clicked.connect(self._back)
    def _logout(self):
        self.controller.logout()
        self.on_update_view.emit()
        self.close()
    def _back(self):
        self.close()