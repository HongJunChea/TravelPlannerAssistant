import sys
from PySide6 import QtWidgets

from src.app import TravelPlannerAssistanceApp

app = QtWidgets.QApplication([])

widget = TravelPlannerAssistanceApp()
widget.resize(800, 600)
widget.show()

sys.exit(app.exec())
