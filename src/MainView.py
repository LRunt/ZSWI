
import sys
from PyQt5.QtWidgets import QApplication, QMenuBar, QWidget, QLineEdit, QPushButton, QFileDialog, QCheckBox, \
    QMessageBox, QTableWidget
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGridLayout

from src.ColumnFilterView import ColumnFilterView
from src.MainController import MainController

"""
Class {@code MainView} represents the main window
"""
class MainView():

    def __init__(self):

        app = QApplication(sys.argv)

        self.controller = MainController(self)

        self.menubar = QMenuBar()
        self.textbox = QLineEdit()
        self.descriptionButton = QPushButton('Description')
        self.table = QtWidgets.QTableWidget()
        self.tableCheckBox = QCheckBox("Full table")
        self.searchTextBox = QLineEdit()
        self.doubleSpinbox = QtWidgets.QDoubleSpinBox()
        self.slider = QtWidgets.QSlider()
        self.sliderButton = QtWidgets.QPushButton()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setContentsMargins(10, 10, 10, 10)

        self.grid.addWidget(self.buildMenu(), 0, 0)
        self.grid.addWidget(self.buildTextBox(), 1, 0)
        self.grid.addWidget(self.buildDescriptionButton(), 2, 0)
        self.grid.addWidget(self.buildTableCheckBox(), 3, 0)
        self.grid.addWidget(self.buildSearchTextBox(), 4, 0)

        self.tableX = 5
        self.tableY = 0
        self.grid.addWidget(self.table, self.tableX, self.tableY)

        self.grid.addWidget(self.buildDoubleSpinBox(), 6, 0)
        self.grid.addWidget(self.buildSlider(), 7, 0)
        self.grid.addWidget(self.buildSliderButton(), 8, 0)

        window = QWidget()
        window.setLayout(self.grid)
        window.setWindowTitle("Predikce")
        window.resize(1080, 780)
        window.show()

        sys.exit(app.exec_())


    def buildMenu(self):
        """
        Method create menu in top of the window
        :return: menu
        """
        actionFile = self.menubar.addMenu("File")
        actionFile.addAction("Load data").triggered.connect(self.controller.loadTable)
        actionFile.addAction("Load descriptions").triggered.connect(self.controller.loadDescriptions)
        actionFile.addSeparator()
        #actionFile.addAction("Quit").triggered.connect(self.turnOf)
        self.menubar.addMenu("Edit")
        self.menubar.addMenu("View")
        settingsFile = self.menubar.addMenu("Settings")
        settingsFile.addAction("Column settings").triggered.connect(self.openColumnView)
        self.menubar.addMenu("Help")

        return self.menubar

    def buildTextBox(self):
        """
        Method creates textBox
        :return:  textBox
        """
        return self.textbox

    def buildDescriptionButton(self):
        """
        Method creates description button
        Description button opens description of record
        :return: description button
        """
        self.descriptionButton.clicked.connect(self.controller.buttonDecsriptionPushed)
        return self.descriptionButton

    def buildTableCheckBox(self):
        """
        Method creates empty table
        :return: empty table
        """
        self.tableCheckBox.stateChanged.connect(self.controller.checkBoxChanged)
        return self.tableCheckBox

    def buildSearchTextBox(self):
        """
        Method creates textBox for searching records in the table
        :return: search textBox
        """
        self.searchTextBox.textChanged.connect(self.controller.rowFilter)
        return self.searchTextBox

    def buildDoubleSpinBox(self):
        """
        Method creates double spinbox, where user can type only numbers
        :return: double spinBox
        """
        minimum = 0
        maximum = 100
        step = 1
        self.doubleSpinbox.valueChanged.connect(self.controller.doubleSpinboxChanged)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.doubleSpinbox.setSizePolicy(size_policy)

        self.doubleSpinbox.setMaximum(maximum)
        self.doubleSpinbox.setMinimum(minimum)
        self.doubleSpinbox.setSingleStep(step)
        self.doubleSpinbox.setValue(50)

        self.doubleSpinbox.setDecimals(len(str(step).split('.')[-1]))
        return self.doubleSpinbox


    def buildSlider(self):
        """
        Method creates slider connected with double spin box, after pushing slider button (button with text "make prediction")
        it takes the number for slider and make prediction
        :return: slider
        """
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setSizePolicy(size_policy)
        self.slider.valueChanged.connect(self.controller.sliderChanged)
        #double_spinbox_range = self.double_spinbox.maximum() - self.double_spinbox.minimum()
        #slider_max = double_spinbox_range / self.double_spinbox.singleStep()
        self.slider.setMaximum(int(100))

        #self.buttonS.clicked.connect(self.update_table)
        minimum = 0
        maximum = 100
        step = 1
        #self.set_single_step(step)
        #self.slider.setMinimum(0)
        #self.set_minimum(minimum)
        #self.set_maximum(maximum)

        return self.slider

    def buildSliderButton(self):
        """
        Method creates slider button
        :return: slider button
        """
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.sliderButton.setSizePolicy(size_policy)
        self.sliderButton.setText("MAKE PREDICTION")
        self.sliderButton.clicked.connect(self.controller.reactionOnPredictionButton)
        #self.sliderButton.clicked.connect(self.controller.pokus)
        return self.sliderButton

    def openFileDialog(self):
        """
        Method opens a file dialog where chose the file to open
        :return: file dialog
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fn, _ = QFileDialog.getOpenFileName(self.menubar, "QFileDialog.getOpenFileName()", "",
                                            "JSON Files (*.json *.json.zip)", options=options)
        if(fn):
           return self.controller.loadData(fn)


    def buildFullTable(self, data):
        """
        Method fill table with all columns - "Full table"
        :param data: data which will showed
        :return: table with all columns
        """

        """
        self.table.clear()
        while (self.table.rowCount() > 0):
            self.table.removeRow(0)
        """

        if (data == None):
            return self.table


        # ulozeni hlavicky tabulky
        self.labels = ["report_ids"] + data["labels"] + ["gts"] + ["prediction"]
        self.labels.append("precision")
        self.labels.append("recall")
        self.labels.append("f1")

        self.gts = data["gts"]

        self.report_ids = data["report_ids"]

        self.prediction_probas = data["prediction_probas"]

        self.label = data["labels"]

        # nastaveni poctu sloupu a vlozeni textu do sloupcu
        self.table = QtWidgets.QTableWidget()
        
        
        self.grid.addWidget(self.table, self.tableX, self.tableY)

        self.table.setColumnCount(len(self.labels))
        self.table.setHorizontalHeaderLabels(self.labels)

        # nastaveni layoutu, ktery se bude predavat oknu

        i = 0

        prediction = self.controller.computeTreshold(self.prediction_probas, data["labels"], 50)

        #self.table.selectionModel().selectionChanged.connect(self.controller.on_selectionChanged)

        # vkladani dat do tabulky
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        for j in self.gts:
            j = 0
            # vlozeni id
            self.table.insertRow(self.table.rowCount())

            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, self.report_ids[i])
            # nastaveni na prislusne misto
            self.table.setItem(i, j, it)
            j += 1
            # vlozeni sloupecku predikci - zatim zakomentovano, kvuli rychlostnim pozadavkum

            for y in self.label:
                it = QtWidgets.QTableWidgetItem()
                predikce = self.prediction_probas[i][j - 1]
                it.setData(QtCore.Qt.DisplayRole, predikce)
                # zakazani editovani bunky
                self.table.setItem(i, j, it)
                j += 1

            str = ""
            k = 0
            # vlozeni spravnych vysledku predikci
            for z in self.gts[i]:
                str += self.gts[i][k] + ", "
                k += 1
            # odstraneni posledni carky
            str = str[:-2]
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, str)
            self.table.setItem(i, j, it)

            # diagnozy vyhodnocene podle prahu
            j += 1
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, prediction[i])
            self.table.setItem(i, j, it)
            i += 1

        self.table.doubleClicked.connect(self.openDetail)
        self.controller.evaluateData()
        return self.table



    def buildSmallTable(self, data):
        """
        Method fill table without label columns
        :param data: data what will be filled into the table
        :return: full table
        """

        self.table = QtWidgets.QTableWidget()

        if(data == None):
            return self.table

        # ulozeni hlavicky tabulky
        self.labels = ["report_ids"] + ["gts"] + ["prediction"] #+ self.data["labels"]
        self.labels.append("precision")
        self.labels.append("recall")
        self.labels.append("f1")

        self.gts = data["gts"]
        self.report_ids = data["report_ids"]
        self.prediction_probas = data["prediction_probas"]
        self.label = data["labels"]

        # nastaveni poctu sloupu a vlozeni textu do sloupcu

        self.grid.addWidget(self.table, self.tableX, self.tableY)

        self.table.setColumnCount(len(self.labels))
        self.table.setHorizontalHeaderLabels(self.labels)
        i = 0

        prediction = self.controller.computeTreshold(self.prediction_probas, data["labels"], 50)

        #self.table.selectionModel().selectionChanged.connect(self.controller.on_selectionChanged)

        # vkladani dat do tabulky
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        for j in self.gts:
            j = 0
            # vlozeni id
            self.table.insertRow(self.table.rowCount())
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, self.report_ids[i])
            #self.table.doubleClicked.connect(self.openDetail)
            # zamezeni zmeny dat v bunce
            #it.setFlags(QtCore.Qt.ItemIsEnabled)
            # nastaveni na prislusne misto
            self.table.setItem(i, j, it)
            j += 1
            # vlozeni sloupecku predikci - zatim zakomentovano, kvuli rychlostnim pozadavkum

            str = ""
            k = 0
            # vlozeni spravnych vysledku predikci
            for z in self.gts[i]:
                str += self.gts[i][k] + ", "
                k += 1
            # odstraneni posledni carky
            str = str[:-2]
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, str)
            #it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(i, j, it)

            # diagnozy vyhodnocene podle prahu
            j += 1
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, prediction[i])
            #it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(i, j, it)
            i += 1

        self.table.doubleClicked.connect(self.openDetail)
        self.controller.evaluateData()
        return self.table

    def openColumnView(self):
        """
        Method opens choseBox with column choice
        :return: choseBox
        """
        self.cf = ColumnFilterView(self)
        self.cf.show()

    def openDetail(self, item):
        cellContent = item.data()
        itemColumn = item.column()
        if(itemColumn == 0):
            self.controller.findDescription(str(cellContent))

    def showDialog(self, text):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("QMessageBox Example")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()

# vstupni bod programu
if __name__ == "__main__":
    # window()
    m = MainView()


