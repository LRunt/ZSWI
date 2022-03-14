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


class slider(QWidget):
    def __init__(self, parent=None):
        super(slider, self).__init__(parent)

        layout = QVBoxLayout()
        self.l1 = QLabel("50")
        self.l1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.l1)

        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(50)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(1)

        layout.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)
        self.setLayout(layout)

    def valuechange(self):
        size = self.sl.value()
        #print(size)
        self.l1.setText(str(size))

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

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        myMenu = Menu()

        self.setMenuWidget(myMenu)

"""
Metoda necita data z JSONU, at kompresovana nebo normalni 
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

def window():
    # nacitani dat z JSONU
    data = load_data('dummy.json.zip')
    # ulozeni hlavicky tabulky
    labels = ["report_ids"] + data["labels"] + ["gts"]
    gts = data["gts"]
    report_ids = data["report_ids"]
    prediction_probas = data["prediction_probas"]
    label = data["labels"]

    app = QApplication(sys.argv)

    window = QWidget()

    table = QtWidgets.QTableWidget(0, len(labels))
    table.setHorizontalHeaderLabels(labels)
    i = 0

    for x in gts:
        j = 0
        # vlozeni id
        table.insertRow(table.rowCount())
        it = QtWidgets.QTableWidgetItem()
        it.setData(QtCore.Qt.DisplayRole, report_ids[i])
        it.setFlags(QtCore.Qt.ItemIsEnabled)
        table.setItem(i, j, it)
        j += 1
        # vlozeni predikci
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
        # clozeni spravnych vysledku
        for z in gts[i]:
            str += gts[i][k] + ", "
            k += 1
        # odstraneni posledni carky
        str = str[:-2]
        it = QtWidgets.QTableWidgetItem()
        it.setData(QtCore.Qt.DisplayRole, str)
        it.setFlags(QtCore.Qt.ItemIsEnabled)
        table.setItem(i, j, it)
        i += 1

    vbox = QVBoxLayout()
    grid = QGridLayout()
    grid.setSpacing(0)
    #grid.setAlignment(0)
    grid.setContentsMargins(0, 0, 0, 0)

    myMenu = Menu()

    grid.addWidget(myMenu, 0, 0)
    #vbox.addWidget(myMenu)
    #vbox.addWidget(table)

    grid.addWidget(table, 1, 0)

    mySlider = slider();

    grid.addWidget(mySlider, 2, 0)
    #vbox.addWidget(mySlider)

    window.setLayout(grid)
    window.setWindowTitle("Predikce")
    window.resize(1080, 780)

    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    window()

    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    """
