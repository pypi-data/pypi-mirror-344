from .model_response import Model_Response

class Model_Error(Model_Response): # Model_Error also inherits
    def __init__(self, message: str, code: int):
        super().__init__(False)
        self.message = message
        self.code = code