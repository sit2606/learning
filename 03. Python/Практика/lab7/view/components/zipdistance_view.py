from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from view.helpers.column_helper import COLUMN_TO_SHOW
from view.qtsrc.filter_ui import Ui_filterDialog
class ZipDistanceWindow(QDialog, Ui_filterDialog):
    filter_options = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.FilterListcomboBox.addItem('Zip')
        self.FilterListcomboBox.setEnabled(False)
        self.AcceptpushButton.clicked.connect(self._get_filter)
        self.BackpushButton.clicked.connect(self.reject)
        self.AcceptpushButton.setEnabled(False)
        self.ZiplineEdit.textChanged.connect(self._validate)
        self.FilterCriterialabel.setText('Distance')
    def _get_filter(self):
        data = dict()
        data.update({'zip': self.ZiplineEdit.text()})
        data.update({'distance': self.FilterCriterialineEdit.text().split()})
        self.filter_options.emit(data)
        self.accept()
    def _validate(self):
        has_text = len(self.ZiplineEdit.text().strip()) > 0
        self.AcceptpushButton.setEnabled(has_text)