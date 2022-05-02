
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QMenuBar, QWidget, QLineEdit, QPushButton, QFileDialog, QCheckBox
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableView, QGridLayout

from src.ColumnFilterView import ColumnFilterView
from src.DetailWindow import DetailWindow
from src.MainController import MainController



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



        actionFile = self.menubar.addMenu("File")
        actionFile.addAction("New")
        actionFile.addAction("Open").triggered.connect(self.openFileDialog)
        actionFile.addAction("Save")
        actionFile.addSeparator()
        #actionFile.addAction("Quit").triggered.connect(self.turnOf)
        self.menubar.addMenu("Edit")
        self.menubar.addMenu("View")
        settingsFile = self.menubar.addMenu("Settings")
        settingsFile.addAction("Column settings").triggered.connect(self.openColumnView)
        self.menubar.addMenu("Help")

        return self.menubar

    def buildTextBox(self):
        return self.textbox

    def buildDescriptionButton(self):
        #self.descriptionButton.clicked.connect(self.controller.findDescription)
        return self.descriptionButton

    def buildTableCheckBox(self):
        self.tableCheckBox.stateChanged.connect(self.controller.checkBoxChanged)
        return self.tableCheckBox

    def buildSearchTextBox(self):
        self.searchTextBox.textChanged.connect(self.controller.rowFilter)
        return self.searchTextBox

    def buildDoubleSpinBox(self):



        minimum = 0
        maximum = 100
        step = 1
        self.doubleSpinbox.valueChanged.connect(self.controller.double_spinbox_changed)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.doubleSpinbox.setSizePolicy(size_policy)

        self.doubleSpinbox.setMaximum(maximum)
        self.doubleSpinbox.setMinimum(minimum)
        self.doubleSpinbox.setSingleStep(step)
        self.doubleSpinbox.setValue(50)

        self.doubleSpinbox.setDecimals(len(str(step).split('.')[-1]))
        return self.doubleSpinbox


    def buildSlider(self):

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setSizePolicy(size_policy)
        self.slider.valueChanged.connect(self.controller.slider_changed)
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

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.sliderButton.setSizePolicy(size_policy)
        self.sliderButton.setText("MAKE PREDICTION")
        self.sliderButton.clicked.connect(self.controller.reaction_on_prediction_button)
        #self.sliderButton.clicked.connect(self.controller.pokus)
        return self.sliderButton


    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fn, _ = QFileDialog.getOpenFileName(self.menubar, "QFileDialog.getOpenFileName()", "",
                                            "All Files (*);;Python Files (*.py)", options=options)

        if(fn):
            self.controller.loadData(fn)



    def buildFullTable(self, data):



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

        prediction = self.controller.compute_treshold(self.prediction_probas, data["labels"], 50)

        self.table.selectionModel().selectionChanged.connect(self.controller.on_selectionChanged)



        # vkladani dat do tabulky
        for j in self.gts:
            j = 0
            # vlozeni id
            self.table.insertRow(self.table.rowCount())

            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, self.report_ids[i])
            # zamezeni zmeny dat v bunce
            # it.setFlags(QtCore.Qt.ItemIsEnabled)
            # it.setFlags(QtCore.Qt.ItemIsSelectable)
            # it.setFlags(QtCore.Qt.ItemSelectionMode)
            it.setSelected(True)
            # nastaveni na prislusne misto
            self.table.setItem(i, j, it)
            j += 1
            # vlozeni sloupecku predikci - zatim zakomentovano, kvuli rychlostnim pozadavkum

            for y in self.label:
                it = QtWidgets.QTableWidgetItem()
                predikce = self.prediction_probas[i][j - 1]
                it.setData(QtCore.Qt.DisplayRole, predikce)
                # zakazani editovani bunky
                it.setFlags(QtCore.Qt.ItemIsEnabled)
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
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(i, j, it)

            # diagnozy vyhodnocene podle prahu
            j += 1
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, prediction[i])
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(i, j, it)
            i += 1


        return self.table



    def buildSmallTable(self, data):
        """
        self.table.clear()
        while (self.table.rowCount() > 0):
            self.table.removeRow(0)
        """
        self.table = QtWidgets.QTableWidget()

        if(data == None):
            return self.table


        # ulozeni hlavicky tabulky



        self.labels = ["report_ids"] + ["gts"] + ["prediction"] #+ self.data["labels"]
        self.labels.append("precision")

        self.gts = data["gts"]
        self.report_ids = data["report_ids"]
        self.prediction_probas = data["prediction_probas"]
        self.label = data["labels"]

        # nastaveni poctu sloupu a vlozeni textu do sloupcu

        self.grid.addWidget(self.table, self.tableX, self.tableY)



        self.table.setColumnCount(len(self.labels))
        self.table.setHorizontalHeaderLabels(self.labels)
        i = 0

        prediction = self.controller.compute_treshold(self.prediction_probas, data["labels"], 50)

        self.table.selectionModel().selectionChanged.connect(self.controller.on_selectionChanged)

        # vkladani dat do tabulky
        for j in self.gts:
            j = 0
            # vlozeni id
            self.table.insertRow(self.table.rowCount())
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, self.report_ids[i])
            # zamezeni zmeny dat v bunce
            # it.setFlags(QtCore.Qt.ItemIsEnabled)
            # it.setFlags(QtCore.Qt.ItemIsSelectable)
            # it.setFlags(QtCore.Qt.ItemSelectionMode)
            it.setSelected(True)
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
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(i, j, it)

            # diagnozy vyhodnocene podle prahu
            j += 1
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, prediction[i])
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(i, j, it)
            i += 1


        return self.table

    def openColumnView(self):
        self.cf = ColumnFilterView(self)
        self.cf.show()

    """
    def openDetailView(self, index):
        self.detailWindow = DetailWindow(self.ids[index], self.texts[index])
        self.detailWindow.show()
    """
