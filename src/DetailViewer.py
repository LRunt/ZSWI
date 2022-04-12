import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

from DetailWindow import DetailWindow


class DetailViewer(QWidget):

    def __init__(self, textData):
        super().__init__()
        self.textData = textData
        self.ids = textData["report_ids"]
        self.texts = textData["texts"]

        #Nastaveni layoutu
        layout = QVBoxLayout()

        #TextField
        self.textbox = QLineEdit(self)
        self.textbox.move(0, 0)
        self.textbox.resize(100, 20)
        layout.addWidget(self.textbox)

        #Button
        self.button = QPushButton('Description', self)
        self.button.move(0, 0)
        self.button.clicked.connect(self.showIt)
        layout.addWidget(self.button)

        self.setLayout(layout)

    """
    Metoda zajisti data, vezme index a zjisti jestli se vysytuje v jsonu
    """
    def showIt(self):
        input = self.textbox.text()
        if(re.match(r'[0-9]+', input)):
            for i in range(len(self.ids)):
                print(self.ids[i])
                if(int(input) == self.ids[i]):
                    print(self.ids[i])
                    print(input)
                    print("Nasel jsem")
                    self.showDetail(i)
                    return
            #print("Nenasel jsem")
            #index nenalezen
            QMessageBox.information(self, 'Info', "The index " + input + " was not found", QMessageBox.Ok)
        else:
            #vstup neni cislo
            #print("spatne")
            QMessageBox.warning(self, 'Error', "The input \"" + input + "\" is not a number: ", QMessageBox.Ok)

    """
    Metoda zobrazi okno s detailem
    """
    def showDetail(self, index):
        self.detailWindow = DetailWindow(self.ids[index], self.texts[index])
        self.detailWindow.show()

