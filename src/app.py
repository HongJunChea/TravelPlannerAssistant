import random
from PySide6 import QtCore, QtWidgets


class TravelPlannerAssistanceApp(QtWidgets.QWidget):
    hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

    def __init__(self):
        super().__init__()
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))