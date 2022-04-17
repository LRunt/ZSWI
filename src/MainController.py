import json
from decimal import Decimal, ROUND_HALF_UP
from PyQt5 import QtCore, QtGui, QtWidgets
import zipfile
class MainController:

    def __init__(self, v):

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
            data = json.loads(jsonstring)
        else:
            with open(path, 'r') as json_file:
                data = json.load(json_file)

        self.view.buildSmallTable(data)


