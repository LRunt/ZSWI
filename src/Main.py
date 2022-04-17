"""
@Author Lukáš Runt
@Version 1.0
"""

#imports
import json
import sys
import zipfile
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel, QGridLayout, \
    QMenuBar, QMainWindow, QTableView, QTableWidget, QStyledItemDelegate, QAction

from DetailViewer import DetailViewer
from DoublespinboxAndSlider import DoublespinboxAndSlider
from src.ImportData import ImportData
from src.MainController import MainController
from src.MyMenu import Menu
from src.MyTable import MyTable
from src.MainView import MainView

"""
Trida predstavujici okno
"""
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

"""
Metoda se stara o okno (velikost, text v titulku...) a sestavuje komponenty
"""
def window():
    app = QApplication(sys.argv)

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

    mySlider = DoublespinboxAndSlider(myTable)
    descriptionData = ImportData.load_data('C:/Users/polac/Documents/Vysoká škola/KIV-ZSWI/pokus/ZSWI/Data/dummy.json.zip')
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
    #window()
    m = MainView()

    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    """
