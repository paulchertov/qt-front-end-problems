from PySide6.QtCore import QObject

from controllers import PSWithViewMixin


class PSPlayerController(QObject, PSWithViewMixin):
    gui_name = "player"

    def __init__(self, ):
        super().__init__()
        self.install_gui()
        self.set_styles()

    def present(self):
        pass

