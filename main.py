import sys

from PySide6.QtWidgets import QApplication
from controllers.main import PSFrontEndProblems

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PSFrontEndProblems()
    sys.exit(app.exec())
