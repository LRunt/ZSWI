"""
@Author Lukáš Runt
@Version 1.0
"""

#imports
import json
import sys
from PyQt5 import QtCore, QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    #nacitani dat z JSONU
    f = open('dummy.json', "r")
    d = f.read()
    f.close()
    data = json.loads(d)
    #ulozeni hlavicky tabulky
    labels =["report_ids"] + data["labels"] + ["gts"]
    gts = data["gts"]
    report_ids = data["report_ids"]
    prediction_probas = data["prediction_probas"]
    label = data["labels"]

    w = QtWidgets.QTableWidget(0, len(labels))
    w.setHorizontalHeaderLabels(labels)
    i = 0

    for x in gts:
        j = 0
        #vlozeni id
        w.insertRow(w.rowCount())
        it = QtWidgets.QTableWidgetItem()
        it.setData(QtCore.Qt.DisplayRole, report_ids[i])
        it.setFlags(QtCore.Qt.ItemIsEnabled)
        w.setItem(i, j, it)
        j += 1
        #vlozeni predikci
        for y in label:
            it = QtWidgets.QTableWidgetItem()
            predikce = prediction_probas[i][j - 1]
            it.setData(QtCore.Qt.DisplayRole, predikce)
            #zakazani editovani bunky
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            w.setItem(i, j, it)
            j += 1
        str = ""
        k = 0
        #clozeni spravnych vysledku
        for z in gts[i]:
            str += gts[i][k] + ", "
            k += 1
        #odstraneni posledni carky
        str = str[:-2]
        it = QtWidgets.QTableWidgetItem()
        it.setData(QtCore.Qt.DisplayRole, str)
        it.setFlags(QtCore.Qt.ItemIsEnabled)
        w.setItem(i, j, it)
        i += 1

    w.resize(640, 480)
    w.show()
    sys.exit( app.exec_())