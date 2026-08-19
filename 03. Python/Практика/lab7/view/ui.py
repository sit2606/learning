import sys

from PyQt5.QtWidgets import QApplication

from controller.AppController import AppController
from view.components.table_view import MainWindow


def run_gui(controller: AppController):
    app = QApplication(sys.argv)
    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec_())
