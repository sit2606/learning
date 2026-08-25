from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from controller.AppController import AppController
from view.components.detail_view import DetailView
from view.components.paginationWidget import  PaginationWidget
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
        self.markets = self.controller.get_all_markets()
        self.show_markets()
        self.currentUser.setText(controller.user)
        self.loginButton.clicked.connect(self.open_login)
        self.pagination = PaginationWidget()
        self.horizontalLayout_2.addWidget(self.pagination)
        self.viewButton.clicked.connect(self.open_view)
        self.pagination.setVisible(False)
        self.viewButton.setText('All')
        self.pageControlWidget.setVisible(False)
        self.pagination.radioButton_page5.setChecked(True)
        self.pagination.page_size_changed.connect(self.show_paged_markets)
        self.forwardPage.clicked.connect(self.next_page)
        self.backPage.clicked.connect(self.prev_page)
        self.page_size = 5
        self.current_page = 0
        self.pageCount.setText(str(self.current_page))
        self.tableView.clicked.connect(self.on_row_clicked)

    def update_current_user(self):
        self.currentUser.setText(str(self.controller.user))
    def show_markets(self):
        if self.markets is None:
            return
        for num, market_dict in self.markets.items():
            row = []
            for col in COLUMN_TO_SHOW:
                row.append(str(market_dict.get(col, '')))
            self.model.appendRow([QStandardItem(v) for v in row])
    def open_login(self):
        dialog = LoginWindow(self.controller)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.update_current_user()
    def open_view(self):
        a = self.viewButton.text()
        if a == 'All':
            self.viewButton.setText('By page')
            self.pagination.setVisible(True)
            self.pageControlWidget.setVisible(True)
            self.show_paged_markets()
        if a == 'By page':
            self.viewButton.setText('All')
            self.pagination.setVisible(False)
            self.pageControlWidget.setVisible(False)
            self.show_markets()
    def show_paged_markets(self, page_size = 5, current_page = 0):
        self.model.removeRows(0, self.model.rowCount())
        self.page_size = page_size
        self.current_page = current_page
        self.pageCount.setText(str(self.current_page))
        start = current_page * page_size
        end = start + page_size
        page_data = list(self.markets.items())[start:end]
        for num, market_dict in page_data:
            row = []
            for col in COLUMN_TO_SHOW:
                row.append(str(market_dict.get(col, '')))
            self.model.appendRow([QStandardItem(v) for v in row])
    def next_page(self):
        self.current_page += 1
        self.show_paged_markets(self.page_size, self.current_page)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_paged_markets(self.page_size, self.current_page)
    def on_row_clicked(self, index):
        row = index.row()  # номер строки
        market_id = int(self.model.item(row, 0).text()) # первая колонка
        dialog = DetailView(market_info=self.controller.get_market_by_id(market_id),reviews_info=self.controller.get_market_reviews(market_id)
                            ,user_name=self.controller.user)
        dialog.review_created.connect(self.on_review_created)
        result = dialog.exec_()
    def on_review_created(self, market_id, score, text):
        res = self.controller.add_review(market_id, score, text)
        if not res:
            QMessageBox.warning(self, "Review error",
                                    "You should be logged in to post a review")
        