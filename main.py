"""
@Author Lukáš Runt
@Version 1.0
"""

#imports
import json
import sys
import zipfile
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel, QGridLayout, \
    QMenuBar, QMainWindow, QTableView, QTableWidget, QStyledItemDelegate, QAction

from ColumnFilter import ColumnFilter
from DetailViewer import DetailViewer

"""
Trida Slider se stara o vykreslovani slideru
"""
import sys
from decimal import Decimal, ROUND_HALF_UP
from PyQt5 import QtCore, QtGui, QtWidgets


class DoublespinboxAndSlider(QtWidgets.QWidget):
    def __init__(self, parent = None, minimum=0, maximum=100, step=1):
        super(DoublespinboxAndSlider, self).__init__(parent)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)

        self.label = QtWidgets.QLabel('Label', self)
        self.label.setSizePolicy(size_policy)

        self.double_spinbox = QtWidgets.QDoubleSpinBox(self)
        self.double_spinbox.setSizePolicy(size_policy)

        self.slider = QtWidgets.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setSizePolicy(size_policy)

        self.double_spinbox.valueChanged.connect(self.double_spinbox_changed)
        self.slider.valueChanged.connect(self.slider_changed)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.addWidget(self.label)
        self.vertical_layout.addWidget(self.double_spinbox)
        self.vertical_layout.addWidget(self.slider)

        self.set_single_step(step)
        self.slider.setMinimum(0)
        self.set_minimum(minimum)
        self.set_maximum(maximum)

    def set_maximum(self, value):
        self.double_spinbox.setMaximum(value)
        self.set_slider_maximum()

    def set_minimum(self, value):
        self.double_spinbox.setMinimum(value)
        self.set_slider_maximum()

    def set_single_step(self, value):
        self.double_spinbox.setSingleStep(value)
        self.double_spinbox.setDecimals(len(str(value).split('.')[-1]))
        self.set_slider_maximum()

    def set_slider_maximum(self):
        double_spinbox_range = self.double_spinbox.maximum() - self.double_spinbox.minimum()
        slider_max = double_spinbox_range / self.double_spinbox.singleStep()
        self.slider.setMaximum(int(slider_max))

    def slider_changed(self, value):
        value2 = self.round2(float(value) * self.double_spinbox.singleStep())
        self.double_spinbox.setValue(value2)

    def double_spinbox_changed(self, value):
        value2 = int(self.round2(value / self.double_spinbox.singleStep()))
        self.slider.setValue(value2)

    def round2(self, value):
        dicimals = str(self.double_spinbox.singleStep() / 10.0)
        value2 = float(Decimal(str(value)).quantize(Decimal(dicimals), rounding=ROUND_HALF_UP))
        return value2

    def set_maximum(self, value):
        self.double_spinbox.setMaximum(value)
        self.set_slider_maximum()

    def set_minimum(self, value):
        self.double_spinbox.setMinimum(value)
        self.set_slider_maximum()

    def set_single_step(self, value):
        self.double_spinbox.setSingleStep(value)
        self.double_spinbox.setDecimals(len(str(value).split('.')[-1]))
        self.set_slider_maximum()

    def set_slider_maximum(self):
        double_spinbox_range = self.double_spinbox.maximum() - self.double_spinbox.minimum()
        slider_max = double_spinbox_range / self.double_spinbox.singleStep()
        self.slider.setMaximum(int(slider_max))

    def slider_changed(self, value):
        value2 = self.round2(float(value) * self.double_spinbox.singleStep())
        self.double_spinbox.setValue(value2)

    def double_spinbox_changed(self, value):
        value2 = int(self.round2(value / self.double_spinbox.singleStep()))
        self.slider.setValue(value2)

    def round2(self, value):
        dicimals = str(self.double_spinbox.singleStep() / 10.0)
        value2 = float(Decimal(str(value)).quantize(Decimal(dicimals), rounding=ROUND_HALF_UP))
        return value2



"""
Trida Menu se stara o vykreslovani menu - cele zkopirovano z netu
"""
class Menu(QWidget):

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

"""
Trida MyTable se stara o vykreslovani tabulky
"""
class MyTable(QTableView):

    table = None

    #konstruktor
    def __init__(self):
        QTableView.__init__(self)
        #nastaveni layoutu, ktery se bude predavat oknu
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # nacitani dat z JSONU
        data = load_data('Data/dummy.json.zip')
        # ulozeni hlavicky tabulky
        labels = ["report_ids"] + data["labels"] + ["gts"] + ["prediction"]
        gts = data["gts"]
        report_ids = data["report_ids"]
        prediction_probas = data["prediction_probas"]
        label = data["labels"]

        #nastaveni poctu sloupu a vlozeni textu do sloupcu
        self.table = QtWidgets.QTableWidget(0, len(labels))


        self.table.setHorizontalHeaderLabels(labels)
        i = 0

        prediction = self.compute_treshold(prediction_probas, data["labels"], 50)

        self.table.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        #vkladani dat do tabulky
        for j in gts:
            j = 0
            # vlozeni id
            self.table.insertRow(self.table.rowCount())
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, report_ids[i])
            #zamezeni zmeny dat v bunce
            #it.setFlags(QtCore.Qt.ItemIsEnabled)
            #it.setFlags(QtCore.Qt.ItemIsSelectable)
            #it.setFlags(QtCore.Qt.ItemSelectionMode)
            it.setSelected(True)
            #nastaveni na prislusne misto
            self.table.setItem(i, j, it)
            j += 1
            # vlozeni sloupecku predikci - zatim zakomentovano, kvuli rychlostnim pozadavkum

            for y in label:
                it = QtWidgets.QTableWidgetItem()
                predikce = prediction_probas[i][j - 1]
                it.setData(QtCore.Qt.DisplayRole, predikce)
                # zakazani editovani bunky
                it.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, j, it)
                j += 1

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

            #diagnozy vyhodnocene podle prahu
            j += 1
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, prediction[i])
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(i, j, it)
            i += 1

            layout.addWidget(self.table, 0, 0)

    def getTable(self):
        return self.table

    """
    Metoda vyhodnocuje podle tresholdu ktere predikce budou vyhodnoceny jako pozitivny
    @param prediction_probas data pradikcí
    @param prediction_label jmena predikci
    @param treshold prah podle ktereho se vyhodnocuje zda bude predikce pozitivni nebo ne
    @return pole (list) stringu, ktere znazornuji pozitivni diagnozy
    """
    def compute_treshold(self, prediction_probas, prediction_label, threshold):
        evaluated_predictions = []
        str_of_one_prediction = ""

        for i in range(len(prediction_probas)):
            for j in range(len(prediction_probas[i])):
                #porovnavani zda hodnota presahne prah
                if(prediction_probas[i][j] > threshold):
                    #pridani diagnozi do stringu diagnoz
                    str_of_one_prediction += prediction_label[j] + ", ";
            # odstraneni posledni carky
            str_of_one_prediction = str_of_one_prediction[:-2]
            evaluated_predictions.append(str_of_one_prediction)
            str_of_one_prediction = ""
        return evaluated_predictions

    def on_selectionChanged(selfself, selected):
        print("hehe")

"""
Trida predstavujici okno
"""
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

"""
Metoda necita data z JSONU, at kompresovana nebo normalni 
@return data from JSON
"""
def load_data(path):
    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as zf:
            jsonstring = zf.read(zf.filelist[0]).decode('utf-8')
        data = json.loads(jsonstring)
    else:
        with open(path, 'r') as json_file:
            data = json.load(json_file)
    return data

"""
Metoda se stara o okno (velikost, text v titulku...) a sestavuje komponenty
"""
def window():
    app = QApplication(sys.argv)

    """
    vbox = QVBoxLayout()
    vbox.addWidget(myMenu)
    vbox.addWidget(table)
    #vbox.addWidget(mySlider)
    """

    #vytvoreni gridu
    grid = QGridLayout()
    #nastaveni mezer (jak daleko od okraje se budou vyreslovat komponenty)
    grid.setSpacing(0)
    grid.setContentsMargins(0, 0, 0, 0)

    #vytvoreni komponent

    myTable = MyTable()

    #####

    tb = myTable.getTable()
    myMenu = Menu(tb)

    #####

    mySlider = DoublespinboxAndSlider()
    descriptionData = load_data('Data/dummy_texts.json.zip')
    detailViewer = DetailViewer(descriptionData)
    #pridani komponent do gridu
    grid.addWidget(myMenu, 0, 0)
    grid.addWidget(detailViewer, 1, 0)
    grid.addWidget(myTable, 2, 0)
    grid.addWidget(mySlider, 3, 0)

    #pridani gridu do okna
    window = QWidget()
    window.setLayout(grid)
    window.setWindowTitle("Predikce")
    window.resize(1080, 780)

    window.show()

    sys.exit(app.exec_())

#vstupni bod programu
if __name__ == "__main__":
    window()

    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    """
