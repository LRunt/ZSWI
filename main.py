"""
@Author Lukáš Runt
@Version 1.0
"""

#imports
import json
import sys
import zipfile
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel, QGridLayout, \
    QMenuBar, QMainWindow

"""
Trida Slider se stara o vykreslovani slideru
"""
class Slider(QWidget):
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)

        #nastaveni layoutu a defaultni hodnoty po nacteni
        layout = QVBoxLayout()
        self.l1 = QLabel("50")
        self.l1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.l1)

        #nastaveni slideru
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(50)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(1)

        #propojeni labelu a slideru
        layout.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)
        self.setLayout(layout)

    #promitnuti zmeny hodnoty
    def valuechange(self):
        size = self.sl.value()
        #print(size)
        self.l1.setText(str(size))

"""
Trida Menu se stara o vykreslovani menu - cele zkopirovano z netu
"""
class Menu(QWidget):
    def __init__(self):
        QWidget.__init__(self)
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
        actionFile.addAction("Quit")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

"""
Trida MyTable se stara o vykreslovani tabulky
"""
class MyTable(QWidget):
    #konstruktor
    def __init__(self):
        QWidget.__init__(self)
        #nastaveni layoutu, ktery se bude predavat oknu
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # nacitani dat z JSONU
        data = load_data('report_cnn_512_lite_scenario3.json.zip')
        # ulozeni hlavicky tabulky
        labels = ["report_ids"] + data["labels"]+ ["gts"] + ["prediction"]
        gts = data["gts"]
        report_ids = data["report_ids"]
        prediction_probas = data["prediction_probas"]
        label = data["labels"]

        #nastaveni poctu sloupu a vlozeni textu do sloupcu
        table = QtWidgets.QTableWidget(0, len(labels))
        table.setHorizontalHeaderLabels(labels)
        i = 0

        prediction = self.compute_treshold(prediction_probas, data["labels"], 50)


        #vkladani dat do tabulky
        for j in gts:
            j = 0
            # vlozeni id
            table.insertRow(table.rowCount())
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, report_ids[i])
            #zamezeni zmeny dat v bunce
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            #nastaveni na prislusne misto
            table.setItem(i, j, it)
            j += 1
            # vlozeni sloupecku predikci - zatim zakomentovano, kvuli rychlostnim pozadavkum
            for y in label:
                it = QtWidgets.QTableWidgetItem()
                predikce = prediction_probas[i][j - 1]
                it.setData(QtCore.Qt.DisplayRole, predikce)
                # zakazani editovani bunky
                it.setFlags(QtCore.Qt.ItemIsEnabled)
                table.setItem(i, j, it)
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
            table.setItem(i, j, it)

            #diagnozy vyhodnocene podle prahu
            j += 1
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, prediction[i])
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            table.setItem(i, j, it)
            i += 1
            layout.addWidget(table, 0, 0)

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
    myMenu = Menu()
    myTable = MyTable()
    mySlider = Slider()
    #pridani komponent do gridu
    grid.addWidget(myMenu, 0, 0)
    grid.addWidget(myTable, 1, 0)
    grid.addWidget(mySlider, 2, 0)

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
