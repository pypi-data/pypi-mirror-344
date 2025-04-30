import inspect
from pathlib import Path
import os
import pyautogui
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

    def take_screenshot(self, file_name: str, region=None) -> str | Model_Error:
        """Takes a screenshot and saves it in the caller's directory under 'screenshots' folder."""
        try:
            self.logger.info("Taking screenshot")
            
            # Get caller's directory
            caller_dir = self._get_caller_directory()
            screenshots_dir = caller_dir
            
            # Create screenshots directory if it doesn't exist
            screenshots_dir.mkdir(exist_ok=True)
            
            # Generate full path
            full_path = screenshots_dir / file_name
            
            # Take and save screenshot
            pyautogui.screenshot(region=region).save(str(full_path))
            self.logger.info(f"Screenshot saved to: {full_path}")
            return str(full_path)
            
        except Exception as e:
            self.logger.error(f"Screenshot error: {e}")
            return Model_Error(f"Screenshot error: {e}", 500)

    def _get_caller_directory(self) -> Path:
        """Finds the directory of the immediate caller script."""
        stack = inspect.stack()
        for frame in stack[2:]:  # Skip current and take_screenshot frames
            try:
                path = Path(frame.filename).resolve()
                if not any(p in str(path) for p in ("site-packages", "python", "lib")):
                    return path.parent
            except (AttributeError, IndexError):
                continue
        return Path.cwd()  # Fallback to current directory