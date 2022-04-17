
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QMenuBar, QWidget, QLineEdit, QPushButton, QFileDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableView, QGridLayout

from src.MainController import MainController








class MainView():

    def __init__(self):
        app = QApplication(sys.argv)


        self.controller = MainController(self)


        self.menubar = QMenuBar()
        self.textbox = QLineEdit()
        self.button = QPushButton('Description')
        self.table = QtWidgets.QTableWidget()
        self.doubleSpinbox = QtWidgets.QDoubleSpinBox()
        self.slider = QtWidgets.QSlider()
        self.sliderButton = QtWidgets.QPushButton()


        self.buildMenu()
        self.buildDoubleSpinBox()
        self.buildSlider()
        self.buildSliderButton()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.addWidget(self.menubar, 0, 0)
        grid.addWidget(self.textbox, 1, 0)
        grid.addWidget(self.button, 2, 0)
        grid.addWidget(self.table, 3, 0)
        grid.addWidget(self.doubleSpinbox, 4, 0)
        grid.addWidget(self.slider, 5, 0)
        grid.addWidget(self.sliderButton, 6, 0)


        window = QWidget()
        window.setLayout(grid)
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
        #settingsFile.addAction("Column settings").triggered.connect(self.processTrigger)
        self.menubar.addMenu("Help")


    def buildDoubleSpinBox(self):
        minimum = 0
        maximum = 100
        step = 1

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.doubleSpinbox.setSizePolicy(size_policy)
        self.doubleSpinbox.valueChanged.connect(self.controller.double_spinbox_changed)
        self.doubleSpinbox.setMaximum(maximum)
        self.doubleSpinbox.setMinimum(minimum)
        self.doubleSpinbox.setSingleStep(step)
        self.doubleSpinbox.setValue(50)
        self.doubleSpinbox.setDecimals(len(str(step).split('.')[-1]))


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

    def buildSliderButton(self):
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.button.setSizePolicy(size_policy)
        self.sliderButton.setText("MAKE PREDICTION")



    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fn, _ = QFileDialog.getOpenFileName(self.menubar, "QFileDialog.getOpenFileName()", "",
                                            "All Files (*);;Python Files (*.py)", options=options)
        self.controller.loadData(fn)













    def buildSmallTable(self, data):
        self.table.clear()
        while (self.table.rowCount() > 0):
            self.table.removeRow(0);


        # ulozeni hlavicky tabulky
        labels = ["report_ids"] + ["gts"] + ["prediction"] #+ self.data["labels"]
        gts = data["gts"]
        report_ids = data["report_ids"]
        prediction_probas = data["prediction_probas"]
        label = data["labels"]

        # nastaveni poctu sloupu a vlozeni textu do sloupcu
        #self.table = QtWidgets.QTableWidget(0, len(labels))
        self.table.setColumnCount(len(labels))
        self.table.setHorizontalHeaderLabels(labels)
        i = 0

        prediction = self.compute_treshold(prediction_probas, data["labels"], 50)

        self.table.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        # vkladani dat do tabulky
        for j in gts:
            j = 0
            # vlozeni id
            self.table.insertRow(self.table.rowCount())
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, report_ids[i])
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
            for z in gts[i]:
                str += gts[i][k] + ", "
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


    def compute_treshold(self, prediction_probas, prediction_label, threshold):
        evaluated_predictions = []
        str_of_one_prediction = ""

        for i in range(len(prediction_probas)):
            for j in range(len(prediction_probas[i])):
                # porovnavani zda hodnota presahne prah
                if (prediction_probas[i][j] > threshold):
                    # pridani diagnozi do stringu diagnoz
                    str_of_one_prediction += prediction_label[j] + ", ";
            # odstraneni posledni carky
            str_of_one_prediction = str_of_one_prediction[:-2]
            evaluated_predictions.append(str_of_one_prediction)
            str_of_one_prediction = ""
        return evaluated_predictions


    def on_selectionChanged(selfself, selected):
        print("hehe")