from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton


class LeaderboardWindow(QDialog):
    """Окно таблицы результатов.

    Показывает историю игр: победитель, проигравший, дата.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Leaderboards")
        self.setMinimumSize(450, 300)
        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Победитель", "Проигравший", "Дата"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def load_results(self, results: list):
        """Заполняет таблицу результатами.

        Args:
            results: список словарей {winner, loser, date}
        """
        self.table.setRowCount(len(results))
        for row, r in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(r["winner"]))
            self.table.setItem(row, 1, QTableWidgetItem(r["loser"]))
            self.table.setItem(row, 2, QTableWidgetItem(r["date"]))
