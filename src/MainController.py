import json
from decimal import Decimal, ROUND_HALF_UP
import re

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import zipfile

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QMessageBox

from src.evaluation import evaluate_multiclass_multilabel


class MainController:

    def __init__(self, v):
        self.data = None
        self.view = v

        self.help = 0


    def double_spinbox_changed(self, value):
        value2 = int(self.round2(value / self.view.doubleSpinbox.singleStep()))
        self.view.slider.setValue(value2)


    def slider_changed(self, value):
        value2 = self.round2(float(value) * self.view.doubleSpinbox.singleStep())
        self.view.doubleSpinbox.setValue(value2)
        print(value)

    def round2(self, value):
        dicimals = str(self.view.doubleSpinbox.singleStep() / 10.0)
        value2 = float(Decimal(str(value)).quantize(Decimal(dicimals), rounding=ROUND_HALF_UP))
        return value2




    def loadData(self, path):

        if path.endswith(".zip"):
            with zipfile.ZipFile(path) as zf:
                jsonstring = zf.read(zf.filelist[0]).decode('utf-8')
            dataa = json.loads(jsonstring)
        else:
            with open(path, 'r') as json_file:
                dataa = json.load(json_file)
        self.data = dataa
        self.view.buildSmallTable(self.data)




    def reaction_on_prediction_button(self):

        evaluated_predictions = self.compute_treshold(self.view.prediction_probas, self.view.label,self.view.slider.value())
        self.prediction_column(evaluated_predictions)

        self.evaluateData()


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



    def prediction_column(self, evaluated_predictions):

        for i in range(self.view.table.columnCount()):

            if (self.view.table.horizontalHeaderItem(i).text() == "prediction"):
                predictionIndex = i

        for i in range(len(evaluated_predictions)):
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, evaluated_predictions[i])
            it.setFlags(QtCore.Qt.ItemIsEnabled)



            self.view.table.setItem(i, predictionIndex, it)


    def on_selectionChanged(self, selected):
        print("hehe")


    def checkBoxChanged(self, int):


        if int == 2:
            if(self.data != None):
                self.view.buildFullTable(self.data)
        else:
            if(self.data != None):
                self.view.buildSmallTable(self.data)

    def rowFilter(self, s):

        for x in range(self.view.table.rowCount()):

            currRow = ""

            for y in range(self.view.table.columnCount()):
                currRow += self.view.table.item(x, y).text()

            if(s in str(currRow)):
                self.view.table.showRow(x)
            else:
                self.view.table.hideRow(x)












    """
    def findDescription(self):
        input = self.textbox.text()
        if(re.match(r'[0-9]+', input)):
            for i in range(len(self.ids)):
                print(self.ids[i])
                if(int(input) == self.ids[i]):
                    print(self.ids[i])
                    print(input)
                    print("Nasel jsem")
                    self.view.openDetailView(i)
                    return
            #print("Nenasel jsem")
            #index nenalezen
            QMessageBox.information(self, 'Info', "The index " + input + " was not found", QMessageBox.Ok)
        else:
            #vstup neni cislo
            #print("spatne")
            QMessageBox.warning(self, 'Error', "The input \"" + input + "\" is not a number: ", QMessageBox.Ok)
    """


    #------------------------------------------------------------------------------------------------
    #------------------------------------EVALUACE DAT------------------------------------------------
    #------------------------------------------------------------------------------------------------


    """
    Již při vytváření tabulky je přidán navíc právě jeden sloupec s názvem precision
    V buňkách u tohoto sloupce nejsou na začátku žádná data, ale umožní to později (při stisku tlačítka např.) do buněk data vkládat
    
    Při stisku tlačítka MAKE PREDICTION se volá metoda reaction_on_prediction_button
    Tato metoda se stará o to, že změní stringy s predikovanými labely a dále volá metodu evaluate data
    tato metoda obsahuje list listů se všemi daty viz její výpisy
    
    Z tohoto listu listů si vytáhnu list obsahující precision ke všem řádkům
    
    A tento list pošlu jako parametr metodě updateTableWithPrecision
    
    Tato metoda list převezme a iteruje ho přičemž pokaždé setne budku tabulky
    
    """


    def evaluateData(self):



        labels = self.view.label.copy()
        prediction_probas = np.asarray(self.view.prediction_probas)
        gts = self.view.gts.copy()


        threshold = self.view.slider.value() / 100


        nplabels = np.asarray(labels)

        preds = self._convert_probas_to_lbls(nplabels, prediction_probas, threshold)  # dle prahu vrati list listu s predikovanymi tridami (labely)
        res = evaluate_multiclass_multilabel(gt=gts, pred=preds)

        # výpisy ------------------------------------------
        print("výsledky pro jednotlivé zprávy")
        tmp = res["samplewise_results"]
        for k, v in tmp.items():



            print(f"{k} - {v}")

        index = 0
        print(
            f"výsledky pro zprávu na indexu {index}")  # index odpovídá pořadí, tak jak bylo zadáno gts a preds v evaluate_multiclass_multilabel
        print(f"gt: {gts[index]}, pred: {preds[index]}")
        for k, v in tmp.items():
            print(f"\t{k} - {v[index]}")
        # konec výpisů----------------------------------------------------------------


        precisionList = tmp.get("micro_precision")

        self.updateTableWithPrecision(precisionList)




    # melo by byt v poskytnutych skriptech v souboru utils.prediction_report
    def _convert_probas_to_lbls(self, nplabels: np.ndarray, prediction_probas: np.ndarray, threshold: float):
        preds = []
        ppthresholded = (prediction_probas/100) >= threshold  # prahovani, dostanu true / false

        for ppt in ppthresholded:

            predlabels = nplabels[ppt].tolist()  # pro jeden report vybere z labelu dle true / false (nutne aby nplabels byly jako numpy ndarray)
            print("ttt")
            preds.append(predlabels)

        return preds


    def updateTableWithPrecision(self, precisionList):

        # tento for tu je protože my vlastně nevíme na kterém indexu se nachází sloupček precision
        # je třeba ten index najít
        for i in range(self.view.table.columnCount()):
            if(self.view.table.horizontalHeaderItem(i).text() == "precision"):
                precisionIndex = i


        counter = 0
        for v in precisionList:
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, str(v))
            self.view.table.setItem(counter, precisionIndex, it)
            counter = counter + 1