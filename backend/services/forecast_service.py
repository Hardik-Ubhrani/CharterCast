import logging
from backend.models.schemas import ForecastRequest, ForecastResponse
from backend.ml.mock_forecaster import MockForecaster
from backend.ml.tft_forecaster import TFTForecaster
from backend.ml.patchtst_forecaster import PatchTSTForecaster

logger = logging.getLogger(__name__)


class ForecastService:
    """
    Central service for delegating forecasting requests to registered ML models.
    Supports 'mock', 'tft', 'patchtst', and 'auto' model selection.
    """

    def __init__(self):
        self.mock_model = MockForecaster()
        self.tft_model = TFTForecaster()
        self.patchtst_model = PatchTSTForecaster()

    def get_forecast(self, request: ForecastRequest) -> ForecastResponse:
        model_choice = (request.model or "auto").lower()

        if model_choice == "tft":
            return self.tft_model.predict(request)
        elif model_choice == "patchtst":
            return self.patchtst_model.predict(request)
        elif model_choice in ("mock", "auto"):
            return self.mock_model.predict(request)
        else:
            logger.warning(f"Unknown model requested '{request.model}', falling back to mock.")
            return self.mock_model.predict(request)
