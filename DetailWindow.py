from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout


class DetailWindow(QWidget):

    def __init__(self, id, text):
        super().__init__()

        # vytvoreni gridu
        grid = QGridLayout()
        #nastaveni gridu
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        self.labelId = QLabel("ID:")
        self.id = QLabel(str(id))
        self.labelText = QLabel("Text:")
        self.text = QLabel(text)

        grid.addWidget(self.labelId, 0, 0)
        grid.addWidget(self.id, 0, 1)
        grid.addWidget(self.labelText, 1, 0)
        grid.addWidget(self.text, 1, 1)

        self.setLayout(grid)