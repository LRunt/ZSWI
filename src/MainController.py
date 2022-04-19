import json
from decimal import Decimal, ROUND_HALF_UP
from PyQt5 import QtCore, QtGui, QtWidgets
import zipfile
class MainController:

    def __init__(self, v):
        self.data = None
        self.view = v


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
        print("sdsd")
        if path.endswith(".zip"):
            with zipfile.ZipFile(path) as zf:
                jsonstring = zf.read(zf.filelist[0]).decode('utf-8')
            dataa = json.loads(jsonstring)
        else:
            with open(path, 'r') as json_file:
                dataa = json.load(json_file)
        self.data = dataa
        self.view.buildSmallTable(self.data)




    def update_table(self):
        print("wewewew")
        evaluated_predictions = self.compute_treshold(self.view.prediction_probas, self.view.label,self.view.slider.value())


        self.prediction_column(evaluated_predictions)


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
        for i in range(len(evaluated_predictions)):
            it = QtWidgets.QTableWidgetItem()
            it.setData(QtCore.Qt.DisplayRole, evaluated_predictions[i])
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.view.table.setItem(i, len(self.view.labels) - 1, it)


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




