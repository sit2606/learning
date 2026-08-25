from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from view.helpers.column_helper import COLUMN_TO_SHOW
from view.qtsrc.filter_ui import Ui_filterDialog
class FilterWindow(QDialog, Ui_filterDialog):
    filter_options = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.FilterListcomboBox.addItems(COLUMN_TO_SHOW)
        self.AcceptpushButton.clicked.connect(self.get_filter)
    def get_filter(self):
        data = dict()

        data.update({'column': self.FilterListcomboBox.currentText()})
        #data.update({'order': })