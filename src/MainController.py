import json
import re
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
from PyQt5 import QtCore, QtWidgets
import zipfile
from src.DetailWindow import DetailWindow
from src.evaluation import evaluate_multiclass_multilabel

"""
Class represents controller model of application,
this class contains all logic of application
"""
class MainController:

    def __init__(self, v):
        self.tableData = None
        self.descriptionData = None
        self.ids = None
        self.texts = None
        self.view = v
        self.help = 0

    def doubleSpinboxChanged(self, value):
        """
        Method reacts on change of spinBox
        :param value: new value of spinbox
        :return: changed value on slider
        """
        value2 = int(self.round(value / self.view.doubleSpinbox.singleStep()))
        self.view.slider.setValue(value2)


    def sliderChanged(self, value):
        """
        Method reacts on change of slider
        :param value: new value of slider
        :return: changed value on spinBox
        """
        value2 = self.round(float(value) * self.view.doubleSpinbox.singleStep())
        self.view.doubleSpinbox.setValue(value2)

    def round(self, value):
        """
        Method rounds numbers
        :param value:
        :return:
        """
        dicimals = str(self.view.doubleSpinbox.singleStep() / 10.0)
        value2 = float(Decimal(str(value)).quantize(Decimal(dicimals), rounding=ROUND_HALF_UP))
        return value2

    def loadTable(self):
        """
        Method loads table data
        :return: built small table (table without labels)
        """
        try:
            self.tableData = self.view.openFileDialog()
            self.view.buildSmallTable(self.tableData)
        except:
            self.view.showDialog("Non-valid data")

    def loadDescriptions(self):
        """
        Method loads description data
        :return:
        """
        try:
            self.descriptionData = self.view.openFileDialog()
            self.ids = self.descriptionData["report_ids"]
            self.texts = self.descriptionData["texts"]
            self.view.showDialog("Descriptions were loaded!")
        except:
            self.view.showDialog("Non-valid data")


    def loadData(self, path):
        """
        Method loads (.json) data from device
        :param path: path of file
        :return: loaded data in list
        """
        if path.endswith(".zip"):
            with zipfile.ZipFile(path) as zf:
                jsonstring = zf.read(zf.filelist[0]).decode('utf-8')
            loadedData = json.loads(jsonstring)
        else:
            with open(path, 'r') as json_file:
                loadedData = json.load(json_file)
        return loadedData

    def reactionOnPredictionButton(self):
        """
        Method reacts on prediction button, after the button was pushed it makes a new prediction
        :return: new prediction
        """
        if(self.tableData == None):
            self.view.showDialog("Table is empty! Please load table data!")
            return
        evaluated_predictions = self.computeTreshold(self.view.prediction_probas, self.view.label, self.view.slider.value())
        self.predictionColumn(evaluated_predictions)

        self.evaluateData()


    def computeTreshold(self, prediction_probas, prediction_label, threshold):
        """
        Method computes thresholds
        :param prediction_probas: list of prediction probas
        :param prediction_label: list of labels
        :param threshold: (double) vlalue of prediction
        :return: evaluated predictions
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



    def predictionColumn(self, evaluated_predictions):
        """
        Method create - rewrite the prediction column
        :param evaluated_predictions: list of evaluated predictions
        :return: prediction column
        """

        for i in range(self.view.table.columnCount()):

            if (self.view.table.horizontalHeaderItem(i).text() == "prediction"):
                predictionIndex = i

        for i in range(len(evaluated_predictions)):
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, evaluated_predictions[i])
            it.setFlags(QtCore.Qt.ItemIsEnabled)

            self.view.table.setItem(i, predictionIndex, it)

    def checkBoxChanged(self, int):
        """
        Method reacts on change of checkbox, after change refill the table
        :param int: button checked or unchecked
        :return: new table of datas
        """
        if int == 2:
            if(self.tableData != None):
                self.view.buildFullTable(self.tableData)
        else:
            if(self.tableData != None):
                self.view.buildSmallTable(self.tableData)


    def rowFilter(self, s):
        """
        Method filters lines in table
        :param s: string what must the line contains
        :return: table with hidden rows
        """
        for x in range(self.view.table.rowCount()):
            currRow = ""

            for y in range(self.view.table.columnCount()):
                currRow += self.view.table.item(x, y).text()

            if(s in str(currRow)):
                self.view.table.showRow(x)
            else:
                self.view.table.hideRow(x)


    def buttonDecsriptionPushed(self):
        if(self.view.textbox.text() == ""):
            return
        self.findDescription(self.view.textbox.text())

    def findDescription(self, idOfDescription):
        """
        Method search description in list, if the description is founded it shows window with description
        if in not found then it throws a window with text to user
        :return:
        """
        if(self.descriptionData == None):
            self.view.showDialog("Please, load description data!")
            return
        if(re.match(r'[0-9]+', idOfDescription)):
            for i in range(len(self.ids)):
                if(int(idOfDescription) == self.ids[i]):
                    self.openDetailView(i)
                    self.view.textbox.clear()
                    return
            #index nenalezen
        self.view.showDialog("The input \"" + idOfDescription + "\" was not found")
        self.view.textbox.clear()

    def openDetailView(self, index):
        """
        Method shows the window with description
        :param index: index of description in array
        :return: window with description
        """
        self.detailWindow = DetailWindow(self.ids[index], self.texts[index])
        self.detailWindow.show()

    #------------------------------------------------------------------------------------------------
    #------------------------------------EVALUACE DAT------------------------------------------------
    #------------------------------------------------------------------------------------------------


    """
    Již při vytváření tabulky je přidáno navíc několik sloupců
    Při vytvoření tabulky se zavolá metoda evaluateData aby se rovnou naplnily budky precision recall a f1
    
    Při stisku tlačítka MAKE PREDICTION se volá metoda reaction_on_prediction_button
    Tato metoda se stará o to, že změní stringy s predikovanými labely a dále volá metodu evaluate data
    tato metoda obsahuje list listů se všemi daty viz její výpisy
    
    Z tohoto listu listů si vytáhnu list obsahující precision, recall a f1 ke všem řádkům
    
    pošlu tyto listy metodě updateTableWithEvaluatedData, jako parametr předávám list s daty (např precision) a název sloupce tabulky kam patří ("precision")
    předpokládá se že ten slopec existuje, pokud by neexistoval bylo by to v čiči, ale je to ošetřeno,
    takže pokud se tu pokusim přidat data do sloupce který neexistuje, nespadne to
    
    Metoda list převezme a iteruje ho přičemž pokaždé setne budku tabulky
    
    """


    def evaluateData(self):

        labels = self.view.label.copy()
        prediction_probas = np.asarray(self.view.prediction_probas)
        gts = self.view.gts.copy()


        threshold = self.view.slider.value() / 100


        nplabels = np.asarray(labels)

        preds = self.convertProbasToLbls(nplabels, prediction_probas, threshold)  # dle prahu vrati list listu s predikovanymi tridami (labely)
        res = evaluate_multiclass_multilabel(gt=gts, pred=preds)


        macroPrecision = res["macro_precision"]
        macroRecall = res["macro_recall"]
        macroF1 = res["macro_f1"]

        self.view.lablePrecision.setText("Makro precision: " + '{:.2%}'.format(macroPrecision))
        self.view.lableRecall.setText("Makro recall: " + '{:.2%}'.format(macroRecall))
        self.view.lableF1.setText("Makro F1: " + '{:.2%}'.format(macroF1))

        tmp = res["samplewise_results"]
        """
        # výpisy ------------------------------------------
        print("výsledky pro jednotlivé zprávy")
        for k, v in tmp.items():
            print(f"{k} - {v}")

        index = 0
        print(
            f"výsledky pro zprávu na indexu {index}")  # index odpovídá pořadí, tak jak bylo zadáno gts a preds v evaluate_multiclass_multilabel
        print(f"gt: {gts[index]}, pred: {preds[index]}")
        for k, v in tmp.items():
            print(f"\t{k} - {v[index]}")
        # konec výpisů----------------------------------------------------------------
        """

        precisionList = tmp.get("micro_precision")
        recallList = tmp.get("micro_recall")
        f1List = tmp.get("micro_f1")

        self.updateTableWithEvaluatedData(precisionList, "precision")
        self.updateTableWithEvaluatedData(recallList,"recall")
        self.updateTableWithEvaluatedData(f1List, "f1")



    # melo by byt v poskytnutych skriptech v souboru utils.prediction_report
    def convertProbasToLbls(self, nplabels: np.ndarray, prediction_probas: np.ndarray, threshold: float):
        preds = []
        ppthresholded = (prediction_probas/100) >= threshold  # prahovani, dostanu true / false

        for ppt in ppthresholded:

            predlabels = nplabels[ppt].tolist()  # pro jeden report vybere z labelu dle true / false (nutne aby nplabels byly jako numpy ndarray)
            preds.append(predlabels)

        return preds


    #je zde důležitý předpoklad že název sloupce existuje
    def updateTableWithEvaluatedData(self, listWithData, columnName):
        # tento for tu je protože my vlastně nevíme na kterém indexu se nachází sloupček precision
        # je třeba ten index najít
        columnIndex = -1
        for i in range(self.view.table.columnCount()):
            if (self.view.table.horizontalHeaderItem(i).text() == columnName):
                columnIndex = i

        if(columnIndex != -1):
            counter = 0
            for v in listWithData:
                it = QtWidgets.QTableWidgetItem()
                it.setData(QtCore.Qt.DisplayRole, '{:.2%}'.format(v))
                self.view.table.setItem(counter, columnIndex, it)
                counter = counter + 1

