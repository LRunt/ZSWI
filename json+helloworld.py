"""
@Author Lukáš Runt
@Version 1.0
"""

#imports
import json
import turtle
from turtle import *
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize
#import pandasgui

"""
print("hello world")
#hello world
a = "Lukas"
b = "Runt"
c = a + " " + b
print(c)
print(a[0])
print(10 > 9)
print(a == b)

f = open("Output.txt", "wt")
f.write("Soubor uspesne vytvoren")
f.close()

f = open("Testovaci soubor.txt", "rt")
print(f.read())



#cyklus for
for x in range(2, 20):
    if(x > 10):
        exit()
    elif(x >= 5):
        print(x)
    else:
        print("Min nez 5")
"""

#cteni JSONU
f = open('dummy.json', "r")
d = f.read()
f.close()
print(d)
f = open('dummy.json', "r")
data = json.loads(f.read())
print(data["description"])
print(data["labels"])
f.close()
print("------------------------------")
#f = open('dummy.json.zip', "r")
#data = f.read()

turtle.shape("turtle")
color('brown', 'green')
begin_fill()
while True:
    forward(200)
    left(170)
    if abs(pos()) < 1:
        break
end_fill()
done()

class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Hello world - pythonprogramminglanguage.com")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        title = QLabel("Hello World from PyQt", self)
        title.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title, 0, 0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit( app.exec_() )