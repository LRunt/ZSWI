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
from DoublespinboxAndSlider import DoublespinboxAndSlider
from Menu import Menu



class MyTable(QTableView):
    """
    Trida MyTable se stara o vykreslovani tabulky
    """


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
