from PySide6.QtWidgets import QMainWindow

from controllers import PSWithViewMixin


class PSPlayerController(PSWithViewMixin):
    gui_name = "player"

    def __init__(self, ):
        super().__init__()
        self.install_gui()
        self.set_styles()

    def present(self):
        pass

