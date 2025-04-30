from .gui_controller import GUIController
from .keyboard_controller import KeyboardController
from .screen_controller import ScreenController
from .system_controller import SystemController

from .logger import *

class AutoGui(GUIController, KeyboardController, ScreenController, SystemController):
    def __init__(self, logger: logging.Logger = None):
        logger = setup_logger(logger)
        super().__init__(logger)

    