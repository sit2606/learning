from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from view.qtsrc.pagination_widget import Ui_paginationwidget


class PaginationWidget(QWidget, Ui_paginationwidget):
    page_size_changed = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setMinimumSize(180, 30)
        self.radioButton_page5.toggled.connect(lambda checked: self._on_change(5, checked))
        self.radioButton_page10.toggled.connect(lambda checked: self._on_change(10, checked))
        self.radioButton_page20.toggled.connect(lambda checked: self._on_change(20, checked))
        self.radioButton_page30.toggled.connect(lambda checked: self._on_change(30, checked))
        self.radioButton_page50.toggled.connect(lambda checked: self._on_change(50, checked))

    def _on_change(self, new_value, checked):
        if checked:
            self.page_size_changed.emit(new_value)
            print(new_value)