from PySide6.QtWidgets import QMainWindow

from controllers import PSWithViewMixin
from controllers.player import PSPlayerController


class PSFrontEndProblems(QMainWindow, PSWithViewMixin):
    gui_name = "main"

    def __init__(self):
        super().__init__()
        self.install_gui()
        self.set_styles()
        self.player = PSPlayerController()

        self.view.app_layout.addWidget(self.player.view)
        self.player.view.show()
        self.setCentralWidget(self.view)
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("m ^_^ m")
        self.show()