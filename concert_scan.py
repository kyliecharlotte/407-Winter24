import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 150)
        self.setWindowTitle("Concert Search")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.move(20,20)
        self.input.resize(180, 130)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.button = QPushButton("Submit Search", self)

        self.button.move(200,100)
        self.button.resize(150, 40)
        self.button.clicked.connect(self.clickbutton)

        self.setMenuWidget(container)

    def clickbutton(self):
        text = self.input.text()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
'''app.setStyle('Fusion')
app.setStyleSheet("QLabel { margin-top: 5ex; margin-bottom: 5ex; margin-left: 10ex; margin-right: 10ex; background-color: #65989f; color: black; font-family: 'Times New Roman', Times, Serif; font-size: 25px;}")
label = QLabel("Concert Scan")
label.show()
app.setStyleSheet("QPushButton { margin: 5ex;}")
enter_button = QPushButton('Submit')
enter_button.show()'''
app.exec()