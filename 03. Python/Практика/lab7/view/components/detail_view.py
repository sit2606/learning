from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from models.entities.market import Location
from view.components.add_review_view import AddReviewView
from view.qtsrc.detail_ui import Ui_marketDetailDialog
class DetailWindow(QDialog, Ui_marketDetailDialog):
    review_created = pyqtSignal(int, float, str)
    def __init__(self, market_info, reviews_info, user_name):
        super().__init__()
        self.setupUi(self)
        self.market_info = market_info
        self.marketidlineEdit.setText(str(self.market_info.id))
        self.marketNamelineEdit.setText(self.market_info.market_info.marketname)
        self.locationZiplineEdit.setText(self.market_info.location.zip)
        self.locationCountylineEdit.setText(self.market_info.location.county)
        self.locationStreetlineEdit.setText(self.market_info.location.street)
        self.locationCitylineEdit.setText(self.market_info.location.city)
        self.locationStatelineEdit.setText(self.market_info.location.state)
        self.addReviewpushButton.clicked.connect(self.add_review)
        self.backToTablepushButton.clicked.connect(self.reject)
        self.reviews_info = reviews_info
        self._update_review_text()
        self.user_name = user_name
        txt = ''
        for media, link in self.market_info.media_info.media.items():
            txt  += media + ' ' + link + '\n'
        self.medionfotextEdit.setText(txt)
        txt = ''
        for payment_method, payment_status in self.market_info.banking_info.banking.items():
            txt  += payment_method + ' ' + payment_status + '\n'
        self.bankinginfotextEdit.setText(txt)
        txt = ''
        for grocery_type, grocery_status in self.market_info.grocery_info.grocery.items():
            txt += grocery_type + ' ' + grocery_status + '\n'
        self.groceryInfotextEdit.setText(txt)
        txt = ''
        for season, time in self.market_info.timesheet.__dict__.items():
            txt += season + ' ' + time + '\n'
        self.timesheettextEdit.setText(txt)
    def add_review(self):
        dialog = AddReviewView(self.user_name)
        dialog.review_created.connect(self.on_review_created)
        self._update_review_text()
        result = dialog.exec_()
    def _update_review_text(self):
        if self.reviews_info:
            txt = ''
            for review in self.reviews_info[0]:
                txt += review['review_date'] + ' | ' + review['user_name'] + ' | ' + str(review['score']) + ' | ' + \
                       review['review_text'] + '\n'
            self.reviewstextEdit.setText(txt)
            self.scorelcdNumber.display(self.reviews_info[1])
    def on_review_created(self, score, text):
        self.review_created.emit(self.market_info.id ,score, text)