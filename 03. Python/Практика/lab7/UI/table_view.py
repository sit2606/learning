import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem

# Сгенерированный файл
from .table_ui import Ui_MainWindow

from .column_helper import COLUMN_TO_SHOW

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # строим интерфейс из Designer
        from BusinessLogic import commandHandler
        is_run, market_list = commandHandler.command_list_all()
        if market_list is None:
            print('Ошибка. Попробуйте ещё раз')
        else:
            for k, i in market_list.items():
                market_list[k] = i.get_as_dict()



        # --- Данные для таблицы ---
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(COLUMN_TO_SHOW)
        for num, market_dict in market_list.items():
            row = []  # первый столбец — порядковый номер
            for col in COLUMN_TO_SHOW:
                row.append(str(market_dict.get(col, '')))
            self.model.appendRow([QStandardItem(v) for v in row])

        # --- Подключаем к tableView ---
        self.tableView.setModel(self.model)