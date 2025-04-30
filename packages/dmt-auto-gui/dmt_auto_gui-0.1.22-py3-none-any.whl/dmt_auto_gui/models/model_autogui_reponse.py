from .model_response import Model_Response

class Model_AutoGuiResponse(Model_Response):
    def __init__(self, x: int, y: int, confidence: float, time_took: float):
        super().__init__(True)
        self.posistion_found = x, y
        self.confidence = confidence
        self.time_took = time_took