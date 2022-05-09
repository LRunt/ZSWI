from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit

class ColumnFilterView(QWidget):

    def __init__(self, mv):
        super().__init__()

        self.listWithColumns = []

        self.mainView = mv

        self.layout = QVBoxLayout()

        self.searchingLabel = QLabel("Column filters")
        self.searchingTextBox = QLineEdit(self)
        self.searchingTextBox.textChanged.connect(self.computeText)

        self.listView = QtWidgets.QListView()

        self.makeListView()

        self.layout.addWidget(self.searchingLabel)
        self.layout.addWidget(self.searchingTextBox)
        self.layout.addWidget(self.listView)

        self.setLayout(self.layout)

    def makeListView(self):
        """
        vytvoří listView a model
        cyklus prochází všechny sloupce tabulky
        pro každý sloupce je vytvořen listViewItem apřidá se do modelu
        listView si pak setne model
        propojí se mistView s funkcí listViewOnClickAction, která se volá při kliku do listView
        :return: listView
        """


        self.model = QStandardItemModel()

        tableColumnCount = self.mainView.table.columnCount()

        for i in range(tableColumnCount):

            item = QStandardItem(self.mainView.table.horizontalHeaderItem(i).text())
            self.listWithColumns.append(self.mainView.table.horizontalHeaderItem(i).text())

            if (self.mainView.table.isColumnHidden(i)):
                check = Qt.Unchecked
            else:
                check = Qt.Checked

            item.setEditable(False)
            item.setCheckable(True)
            item.setCheckState(check)

            self.model.appendRow(item)

        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.listViewOnClickAction)


    def computeText(self, s):

        """
        Metoda se volá pokaždé když se změní obsah textboxu
        :param s: string který je aktuálně v textBoxu
        odstraní se celý model listView - lsiView je prázné
        prochází se list se sloupci
        pokud s (obsah textBoxu) je obsažen v názvu sloupce, vytvoříse item a přidá se do modelu
        všechny tyto sloupce jsou sloupce, které jsou vyfiltrovány a nově zobrazeny v listboxu
        """

        self.model.removeRows(0, self.model.rowCount())

        for index in range(len(self.listWithColumns)):

            if (s in str(self.listWithColumns[index])):
                item = QStandardItem(self.listWithColumns[index])
                if (self.mainView.table.isColumnHidden(index)):
                    check = Qt.Unchecked
                else:
                    check = Qt.Checked

                item.setEditable(False)
                item.setCheckable(True)
                item.setCheckState(check)
                self.model.appendRow(item)


    def listViewOnClickAction(self, index):
        """
        Funkce reaguje na klik do listboxu
        :param index: index prvku na který se kliklo
        it je prvek na který jsem kliknul
        zjistím jaký je jeho skutečný index - to je důležité, pokud použiji filtr a vyfiltruji si poslední sloupec
        v listBoxu by měl index 0, ikdyž jeho skutečný index je např. 5
        Když mám skutečný index skrývám a odkrývám podle potřeby
        """
        number = index.row()
        model = self.listView.model()
        it = model.item(number)
        pureIndex = -1
        listCount = len(self.listWithColumns)


        for x in range(listCount):
            if (self.listWithColumns[x] == str(it.text())):
                pureIndex = x

        if (self.mainView.table.isColumnHidden(pureIndex) == False):
            self.mainView.table.hideColumn(pureIndex)
            it.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.mainView.table.showColumn(pureIndex)
            it.setCheckState(QtCore.Qt.Checked)