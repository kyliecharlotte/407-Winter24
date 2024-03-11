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
        print(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()