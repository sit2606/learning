from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog


from view.qtsrc.add_review_ui import Ui_addReviewDialog
class AddReviewView(QDialog, Ui_addReviewDialog):
    review_created = pyqtSignal( float, str)
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.scoredial.valueChanged.connect(self._update_score)
        self.scorelcdNumber.display(0)
        self.AddReviewpushButton.clicked.connect(self._add_review)
        self.backReviewpushButton.clicked.connect(self.reject)
    def _update_score(self):
        self.scorelcdNumber.display(float(self.scoredial.value()/10))
    def _add_review(self):
        self.review_created.emit(float(self.scoredial.value())/10, self.reviewtextEdit.toPlainText())
        self.accept()
