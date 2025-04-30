import subprocess 
from .models import Model_Error
import logging

class SystemController:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger

    def open_program(self, path: str) -> subprocess.Popen | Model_Error: # More specific return type
        """Opens a program."""
        try:
            self.logger.info(f"Abrindo programa: {path}")
            resp = subprocess.Popen(path, shell=True) # Return the Popen object
            self.logger.info(f"Programa aberto: {path}")
            return resp
        except FileNotFoundError: # Catch specific exception
            self.logger.error(f"Programa não encontrado em: {path}")
            return Model_Error(f"Programa não encontrado em: {path}", 404)
        except Exception as e:
            self.logger.error(f"Erro ao abrir programa: {e}")
            return Model_Error(f"Erro ao abrir programa: {e}", 500)
        
    def close_program(self, name: str) -> int | Model_Error:
        """Closes a program by name."""
        try:
            self.logger.info(f"Fechando programa: {name}")
            resp = subprocess.call(f"taskkill /f /im {name}.exe", shell=True)
            self.logger.info(f"Programa fechado: {name}")
            return resp
        except Exception as e:
            return Model_Error(f"Erro ao fechar programa: {e}", 500)