from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from controller.AppController import AppController
from view.components.detail_view import DetailWindow
from view.components.filter_view import FilterWindow
from view.components.paginationWidget import  PaginationWidget
from view.components.login_view import LoginWindow
from view.components.user_detail import UserDetail
from view.components.zipdistance_view import ZipDistanceWindow

from view.qtsrc.table_ui import Ui_MainWindow

from view.helpers.column_helper import COLUMN_TO_SHOW, COLUMNS, COLUMNS_INFO_REVERSED, COLUMNS_INFO


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, controller: AppController):
        super().__init__()
        self.setupUi(self)
        self.controller = controller
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(COLUMN_TO_SHOW)
        self.tableView.setModel(self.model)
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
        self.filterButton.clicked.connect(self.on_filter_clicked)
        self.ResetFilterpushButton.setVisible(False)
        self.ResetFilterpushButton.clicked.connect(self._reset_filter)
        self.zipdistancepushButton.clicked.connect(self._open_zip_distance)
    def update_current_user(self):
        self.currentUser.setText(str(self.controller.user))
    def show_markets(self):
        self.markets = self.controller.get_all_markets()
        self.model.removeRows(0, self.model.rowCount())
        if self.markets is None:
            return
        for num, market_dict in self.markets.items():
            row = []
            for col in COLUMN_TO_SHOW:
                row.append(str(market_dict.get(col, '')))
            self.model.appendRow([QStandardItem(v) for v in row])
    def open_login(self):
        if self.controller.user:
            dialog = UserDetail(self.controller)
            dialog.on_update_view.connect(self.update_current_user)
            result = dialog.exec_()
        else:
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
        dialog = DetailWindow(market_info=self.controller.get_market_by_id(market_id), reviews_info=self.controller.get_market_reviews(market_id)
                              , user_name=self.controller.user)
        dialog.review_created.connect(self.on_review_created)
        result = dialog.exec_()
    def on_review_created(self, market_id, score, text):
        res = self.controller.add_review(market_id, score, text)
        if not res:
            QMessageBox.warning(self, "Review error",
                                    "You should be logged in to post a review")
    def on_filter_clicked(self):
        dialog = FilterWindow()
        dialog.filter_options.connect(self.filter)
        result = dialog.exec_()
    def filter(self, options):
        column = COLUMNS_INFO_REVERSED[options['column']]
        if COLUMNS_INFO[column]['type'] == 'text':
            filter_value = options['filter_value'][0]
        else:
            filter_value = tuple(options['filter_value'])
        self.markets = self.controller.get_filtered_markets(column= COLUMNS_INFO_REVERSED[options['column']], filter_value=filter_value)[0]
        self.show_paged_markets(self.page_size, self.current_page)
        self.ResetFilterpushButton.setVisible(True)
    def _reset_filter(self):
        self.show_markets()
        self.ResetFilterpushButton.setVisible(False)
    def _update_view(self):
        self.currentUser.setText(None)
    def _open_zip_distance(self):
        dialog = ZipDistanceWindow()
        dialog.filter_options.connect(self.zip_distance)
        result = dialog.exec_()
    def zip_distance(self,options):
        print('s')
        distance = float(options['distance'][0])
        self.markets = self.controller.search_by_zip(postalcode=options['zip'], radius= distance)[0]
        self.show_paged_markets(self.page_size, self.current_page)
        self.ResetFilterpushButton.setVisible(True)
