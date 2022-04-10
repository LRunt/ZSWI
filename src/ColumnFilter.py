from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit


class ColumnFilter(QWidget):

    def __init__(self, tb):
        """
        Konstruktor připravý globální instanční proměnné pro okno s filtrem
        :param tb: tabulka ze které se vytváří filtr
        """
        super().__init__()

        self.table = tb
        self.listWithColumns = []

        self.label = None
        self.textBox = None
        self.listView = None
        self.model = None

        self.buildWindow()


    def buildWindow(self):

        layout = QVBoxLayout()
        layout.addWidget(self.makeSearchingLabel())
        layout.addWidget(self.makeSearchingTextBox())
        layout.addWidget(self.makeListView())

        self.setLayout(layout)



    def makeSearchingLabel(self):
        self.label = QLabel("Column filters")
        return self.label

    def makeSearchingTextBox(self):
        self.textBox = QLineEdit(self)
        self.textBox.textChanged.connect(self.computeText)
        return self.textBox


    def makeListView(self):
        """
        vytvoří listView a model
        cyklus prochází všechny sloupce tabulky
        pro každý sloupce je vytvořen listViewItem apřidá se do modelu
        listView si pak setne model
        propojí se mistView s funkcí listViewOnClickAction, která se volá při kliku do listView
        :return: listView
        """

        self.listView = QtWidgets.QListView()
        self.model = QStandardItemModel()

        tableColumnCount = self.table.columnCount()

        for i in range(tableColumnCount):

            item = QStandardItem(self.table.horizontalHeaderItem(i).text())
            self.listWithColumns.append(self.table.horizontalHeaderItem(i).text())

            if (self.table.isColumnHidden(i)):
                check = Qt.Unchecked
            else:
                check = Qt.Checked

            item.setEditable(False)
            item.setCheckable(True)
            item.setCheckState(check)

            self.model.appendRow(item)

        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.listViewOnClickAction)
        return self.listView


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
                if (self.table.isColumnHidden(index)):
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

        if (self.table.isColumnHidden(pureIndex) == False):
            self.table.hideColumn(pureIndex)
            it.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.table.showColumn(pureIndex)
            it.setCheckState(QtCore.Qt.Checked)