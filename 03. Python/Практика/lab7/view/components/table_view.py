from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from controller.AppController import AppController
from view.components import login_view
from view.components.login_view import LoginWindow
# Сгенерированный файл
from view.qtsrc.table_ui import Ui_MainWindow

from view.helpers.column_helper import COLUMN_TO_SHOW

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, controller: AppController):
        super().__init__()
        self.setupUi(self)  # строим интерфейс из Designer
        self.controller = controller
        # --- Данные для таблицы ---
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(COLUMN_TO_SHOW)
        self.tableView.setModel(self.model)
        # --- Загрузка данных при старте ---
        self.show_markets()
        self.currentUser.setText(controller.user)
        self.loginButton.clicked.connect(self.open_login)
    def update_current_user(self):
        self.currentUser.setText(str(self.controller.user))
    def show_markets(self):
        markets = self.controller.get_all_markets()
        if markets is None:
            return
        for num, market_dict in markets.items():
            row = []
            for col in COLUMN_TO_SHOW:
                row.append(str(market_dict.get(col, '')))
            self.model.appendRow([QStandardItem(v) for v in row])
    def open_login(self):
        dialog = LoginWindow(self.controller)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.update_current_user()
