from gui import MazeWindow
from PySide6.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MazeWindow()
    sys.exit(app.exec())

