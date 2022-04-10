from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QTextEdit


class DetailWindow(QWidget):

    def __init__(self, id, text):
        super().__init__()

        # vytvoreni gridu
        grid = QGridLayout()
        #nastaveni gridu
        grid.setSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)

        self.labelId = QLabel("ID: " + str(id))
        #self.id = QLabel(str(id))
        #self.labelText = QLabel("Text:")
        self.text = QTextEdit(text)

        self.labelId.setFont(QFont('Arial', 10))
        self.text.setFont(QFont('Arial', 10))

        grid.addWidget(self.labelId, 0, 0)
        #grid.addWidget(self.id, 0, 1)
        #rid.addWidget(self.labelText, 2, 0)
        grid.addWidget(self.text, 1, 0)

        self.setLayout(grid)