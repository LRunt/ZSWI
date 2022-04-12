from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel, QGridLayout, \
    QMenuBar, QMainWindow, QTableView, QTableWidget, QStyledItemDelegate, QAction
from PyQt5 import QtCore, QtWidgets

from ColumnFilter import ColumnFilter


class Menu(QWidget):
    """
    Trida Menu se stara o vykreslovani menu
    """

    def __init__(self, tb):
        QWidget.__init__(self)

        self.table = QtWidgets.QTableWidget()
        self.table = tb

        self.colFilter = None

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
        settingsFile.addAction("Column settings").triggered.connect(self.processTrigger)

        menubar.addMenu("Help")

    def processTrigger(self):
        self.colFilter = ColumnFilter(self.table)
        self.colFilter.show()

    def turnOf(self):
        """
        Vypnuti aplikace
        """
        QCoreApplication.quit()
