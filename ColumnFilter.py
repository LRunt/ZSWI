from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel, QGridLayout, \
    QMenuBar, QMainWindow, QAction, QTreeWidget, QTreeWidgetItem, QTableWidget, QLineEdit, QTextEdit


class ColumnFilter(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    table = QtWidgets.QTableWidget

    def __init__(self, tb):
        super().__init__()

        self.listWithColumns = []

        self.table = QtWidgets.QTableWidget()
        self.table = tb

        tableColumnCount = self.table.columnCount()


        layout = QVBoxLayout()
        self.label = QLabel("Column filters")
        layout.addWidget(self.label)

        self.textbox = QLineEdit(self)

        layout.addWidget(self.textbox)

        self.textbox.textChanged.connect(self.computeText)

        self.listView = QtWidgets.QListView()

        self.model = QStandardItemModel()

        counter = 0

        for i in range(tableColumnCount):

            item = QStandardItem(self.table.horizontalHeaderItem(counter).text())
            self.listWithColumns.append(self.table.horizontalHeaderItem(counter).text())

            if (self.table.isColumnHidden(i)):
                check = Qt.Unchecked
            else:
                check = Qt.Checked

            item.setEditable(False)

            item.setCheckState(check)
            item.setCheckable(True)
            self.model.appendRow(item)

            counter = counter + 1


        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.onClicke)

        layout.addWidget(self.listView)

        self.setLayout(layout)


    def computeText(self, s):

        self.model.removeRows(0, self.model.rowCount())

        for index in range(len(self.listWithColumns)):


            if (s in str(self.listWithColumns[index])):
                item = QStandardItem(self.listWithColumns[index])
                if (self.table.isColumnHidden(index)):
                    check = Qt.Unchecked
                else:
                    check = Qt.Checked
                item.setEditable(False)
                item.setCheckState(check)
                item.setCheckable(True)
                self.model.appendRow(item)


    # @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onClicke(self, index):
        number = index.row()
        model = self.listView.model()
        it = model.item(number)
        pureIndex = -1
        listCount = len(self.listWithColumns)


        for x in range(listCount):
            if (self.listWithColumns[x] == str(it.text())):
                pureIndex = x


        if (self.table.isColumnHidden(pureIndex) == False):
            self.table.hideColumn(pureIndex)
            it.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.table.showColumn(pureIndex)
            it.setCheckState(QtCore.Qt.Checked)