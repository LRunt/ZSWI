from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel, QGridLayout, \
    QMenuBar, QMainWindow, QTableView, QTableWidget, QStyledItemDelegate, QAction
from PyQt5 import QtCore, QtWidgets

class Menu(QWidget):
    """
    Trida Menu se stara o vykreslovani menu - cele zkopirovano z netu
    """

    colFilter = None

    def __init__(self, tb):
        QWidget.__init__(self)

        self.table = QtWidgets.QTableWidget()
        self.table = tb

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # create menu
        menubar = QMenuBar()
        layout.addWidget(menubar, 0, 0)
        actionFile = menubar.addMenu("File")
        actionFile.addAction("New")
        actionFile.addAction("Open")
        actionFile.addAction("Save")
        actionFile.addSeparator()
        actionFile.addAction("Quit").triggered.connect(self.turnOf)

        menubar.addMenu("Edit")
        menubar.addMenu("View")
        settingsFile = menubar.addMenu("Settings")
        settingsFile.addAction("Column settings")
        settingsFile.triggered[QAction].connect(self.processTrigger)
        menubar.addMenu("Help")

    def processTrigger(self):
        self.colFilter = ColumnFilter(self.table)
        self.colFilter.show()

    def turnOf(self):
        QCoreApplication.quit()
