import pyautogui
import os 
from .models import Model_Error
import logging

class ScreenController:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger

    def get_screen_size(self) -> tuple | Model_Error:
        """
        Pega o tamanho da tela\n
        return:
            tuple | Model_Error
        """
        try:
            return pyautogui.size()
        except Exception as e:
            return Model_Error(f"Erro ao pegar tamanho da tela: {e}", 500)

    def take_screenshot(self, file_name: str, region=None) -> str | Model_Error: # Return path or error
        """Takes a screenshot and saves it to the specified file."""
        try:
            self.logger.info(f"Tirando screenshot da tela")
            screenshot = pyautogui.screenshot(region=region) # Use region parameter
            full_path = file_name
            if not os.path.exists(full_path): # Check if it's a full path
                # Try relative path in the same directory as the script
                script_dir = os.path.dirname(os.path.abspath(__file__))
                full_path = os.path.join(script_dir, file_name)
            screenshot.save(full_path)
            self.logger.info(f"Screenshot salvo em: {full_path}")
            return full_path # Return the file path
        except Exception as e:
            self.logger.error(f"Erro ao tirar screenshot: {e}")
            return Model_Error(f"Erro ao tirar screenshot: {e}", 500)