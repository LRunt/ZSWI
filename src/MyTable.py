from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableView, QGridLayout

from src.ImportData import ImportData


class MyTable(QTableView):
    """
    Trida MyTable se stara o vykreslovani tabulky
    """

    #konstruktor
    def __init__(self):
        QTableView.__init__(self)
        #nastaveni layoutu, ktery se bude predavat oknu
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


        # nacitani dat z JSONU
        data = ImportData.load_data('C:/Users/polac/Documents/Vysoká škola/KIV-ZSWI/pokus/ZSWI/Data/dummy.json.zip')
        # ulozeni hlavicky tabulky
        self.labels = ["report_ids"] + data["labels"] + ["gts"] + ["prediction"]
        gts = data["gts"]
        report_ids = data["report_ids"]
        self.prediction_probas = data["prediction_probas"]
        self.label = data["labels"]

        #nastaveni poctu sloupu a vlozeni textu do sloupcu
        self.table = QtWidgets.QTableWidget(0, len(self.labels))


        self.table.setHorizontalHeaderLabels(self.labels)
        i = 0

        prediction = self.compute_treshold(self.prediction_probas, data["labels"], 50)

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

    def prediction_column(self, evaluated_predictions):
        for i in range(len(evaluated_predictions)):
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, evaluated_predictions[i])
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(i, len(self.labels) - 1, it)

    def metoda(self):
        it = QtWidgets.QTableWidgetItem()
        it.setData(QtCore.Qt.DisplayRole, "vklad")
        it.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table.setItem(0, 0, it)
        #self.table

    def compute_treshold(self, prediction_probas, prediction_label, threshold):
        """
        Metoda vyhodnocuje podle tresholdu ktere predikce budou vyhodnoceny jako pozitivny
        @param prediction_probas data pradikcí
        @param prediction_label jmena predikci
        @param treshold prah podle ktereho se vyhodnocuje zda bude predikce pozitivni nebo ne
        @return pole (list) stringu, ktere znazornuji pozitivni diagnozy
        """
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

    def on_selectionChanged(self, selected):
        print("hehe")