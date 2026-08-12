import sys

from PyQt5.QtWidgets import QApplication

from view.components.table_view import MainWindow

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
