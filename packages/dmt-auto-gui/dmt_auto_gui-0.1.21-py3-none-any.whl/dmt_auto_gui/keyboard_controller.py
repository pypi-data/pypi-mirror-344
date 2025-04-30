import pyautogui
import pyperclip
import time 
from .models import Model_Error
import logging
class KeyboardController:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger

    def press_keys(self, *keys, tempo=0) -> bool | Model_Error:
        """
        Pressiona teclas\n
        args:
            keys: str -> Teclas a serem pressionadas
            tempo: float -> Tempo de espera
        return:
            bool | Model_Error
        """
        try:
            if not keys:
                self.logger.error("At least one key must be specified")
                raise ValueError("At least one key must be specified")
            pyautogui.hotkey(*keys)
            self.logger.info(f"Teclas pressionadas: {', '.join(keys)}")
            if tempo > 0:
                self.logger.info(f"Esperando {tempo} segundos")
                time.sleep(tempo)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao pressionar teclas: {e}")
            return Model_Error(f"Erro ao pressionar teclas: {e}", 500)
    
    def write_text(self, text:str, tempo=0) -> bool | Model_Error:
        """
        Escreve um texto\n
        args:
            text: str -> Texto a ser escrito
            tempo: float -> Tempo de espera
        return:
            bool | Model_Error
        """
        try:
            self.logger.info(f"Escrevendo texto: {text}")
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            self.logger.info(f"Texto escrito")
            if tempo > 0:
                self.logger.info(f"Esperando {tempo} segundos")
                time.sleep(tempo)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao escrever texto: {e}")
            return Model_Error(f"Erro ao escrever texto: {e}", 500)