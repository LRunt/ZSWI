
"""
Trida Slider se stara o vykreslovani slideru
"""
import sys
from decimal import Decimal, ROUND_HALF_UP
from PyQt5 import QtCore, QtGui, QtWidgets


class DoublespinboxAndSlider(QtWidgets.QWidget):
    def __init__(self, tb, parent = None, minimum=0, maximum=100, step=1):
        super(DoublespinboxAndSlider, self).__init__(parent)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)

        self.table = tb

        #self.label = QtWidgets.QLabel('Label', self)
        #self.label.setSizePolicy(size_policy)

        self.double_spinbox = QtWidgets.QDoubleSpinBox(self)
        self.double_spinbox.setSizePolicy(size_policy)

        self.slider = QtWidgets.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setSizePolicy(size_policy)

        self.double_spinbox.valueChanged.connect(self.double_spinbox_changed)
        self.double_spinbox.setValue(50)
        self.slider.valueChanged.connect(self.slider_changed)

        self.button = QtWidgets.QPushButton(self)
        self.button.setSizePolicy(size_policy)
        self.button.setText("MAKE PREDICTION")
        self.button.clicked.connect(self.update_table)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        #self.vertical_layout.addWidget(self.label)
        self.vertical_layout.addWidget(self.double_spinbox)
        self.vertical_layout.addWidget(self.slider)
        self.vertical_layout.addWidget(self.button)

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














    def update_table(self):
        evaluated_predictions = self.table.compute_treshold(self.table.prediction_probas, self.table.label, self.slider.value())
        self.table.prediction_column(evaluated_predictions)
        #self.table.metoda()


