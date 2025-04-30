import pyautogui
import time 
import os 
from .models import Model_AutoGuiResponse, Model_Error
import logging
from pathlib import Path
from PIL import Image
import sys
import inspect

class GUIController:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger  # Define a base_path ao criar a instância

    def _get_caller_directory(self):
        """Encontra o diretório do script chamador imediatamente anterior na pilha de execução."""
        stack = inspect.stack()
        for frame in stack:
            path = Path(frame.filename).resolve()
            if "site-packages" not in str(path) and "python" not in str(path).lower():
                return path.parent  # Retorna o diretório do script chamador
        raise RuntimeError("Não foi possível determinar o diretório chamador corretamente.")
        
    def find_image_on_screen(self, file_name:str, sleep_after=0, confidence=.9, timeout=30, pos=None) -> Model_AutoGuiResponse | Model_Error:
        """
        Procura uma imagem na tela\n
        args:
            file_name: str -> Nome do arquivo
            sleep: int -> Tempo de espera
            confidence: float -> Confiança
            timeout: int -> Tempo limite
            pos: tuple -> Posição
        return:
            Model_AutoGuiResponse | Model_Error
        """
        self.logger.info(f"Iniciando busca de imagem: {file_name}")
        

        # Carregar a imagem usando PIL
        img = self._get_image_from_path(file_name)

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                x, y = pyautogui.locateCenterOnScreen(img, confidence=confidence, region=pos)
                time_took = time.time() - start_time
                time.sleep(sleep_after)
                self.logger.info(f"Imagem encontrada em {x}, {y} com confiança {confidence} em {time_took} segundos")
                return Model_AutoGuiResponse(x, y, confidence, time_took)
            except TypeError as e:
                self.logger.info(f"Erro ao procurar imagem: {file_name} Erro: {e}")
            except Exception as e:
                pass
            except BaseException as e:
                return Model_Error(f"Erro inesperado: {e}", 500)
        self.logger.info(f"Tempo excedido para encontrar imagem: {file_name} em {timeout} segundos")
        return Model_Error("Tempo excedido", 408)
    
    def _get_image_from_path(self, file_name: str) -> Image.Image:
        """
        Pega a imagem do caminho\n
        args:
            file_name: str -> Nome do arquivo
        return:
            Image.Image
        """
        full_path = Path(file_name)
        if not full_path.is_absolute():
            full_path = (self._get_caller_directory() / file_name).resolve()

        if not full_path.exists():
            self.logger.info(f"Arquivo {full_path} não encontrado!")
            raise FileNotFoundError(f"Arquivo {full_path} não encontrado!")
        try:
            img = Image.open(full_path)
            return img
        except Exception as e:
            raise FileNotFoundError(f"Não foi possível carregar a imagem em: {full_path}!")
        
    def click_on_image(self, file_name: str, sleep: float = 0, clicks: int = 1, confidence = .9, timeout = 30, pos = None, mouse_btn: str = "primary") -> Model_AutoGuiResponse | Model_Error:
        """
        Clica em uma imagem\n
        args:
            file_name: str -> Nome do arquivo
            sleep: float -> Tempo de espera
            clicks: int -> Número de cliques
            confidence: float -> Confiança
            timeout: int -> Tempo limite
            pos: tuple -> Posição
            mouse_btn: str -> Botão do mouse a ser clicado (default: "primary") ["primary", "secondary", "middle", "left", "right"]
        return:
            Model_AutoGuiResponse | Model_Error
        """
        response = self.find_image_on_screen(file_name, 0, confidence, timeout, pos)
        if isinstance(response, Model_AutoGuiResponse):
            x, y = response.posistion_found
            self.click_on_position(x, y, clicks, mouse_btn)
            if sleep > 0:
                self.logger.info(f"Esperando {sleep} segundos")
                time.sleep(sleep)
        return response
    
    def click_on_position(self, x: int, y: int, clicks: int = 1, btn: str = "primary") -> None | Model_Error:
        """
        Clica em uma posição\n
        args:
            x: int -> Posição x
            y: int -> Posição y
            clicks: int -> Número de cliques
            btn: str -> Botão do mouse a ser clicado (default: "primary") ["primary", "secondary", "middle", "left", "right"]
        return:
            None | Model_Error
        """
        try:
            self.logger.info(f"Clicando na posição: {x}, {y} com {clicks} cliques")
            pyautogui.click(x, y, clicks=clicks, button=btn)
            return None
        except Exception as e:
            return Model_Error(f"Erro ao clicar na posição {x}, {y}: {e}", 500)
    
    def get_mouse_position(self) -> tuple | Model_Error:
        """
        Pega a posição do mouse\n
        return:
            tuple | Model_Error
        """
        try:
            pos = pyautogui.position()
            self.logger.info(f"Mouse encontrado na posição {pos.x}, {pos.y}")
            return pos
        except Exception as e:
            self.logger.error(f"Erro ao pegar posição do mouse: {e}")
            return Model_Error(f"Erro ao pegar posição do mouse: {e}", 500)