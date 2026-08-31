import logging
import os
from backend.ml.model_interface import ForecastModel
from backend.ml.mock_forecaster import MockForecaster
from backend.models.schemas import ForecastRequest, ForecastResponse

logger = logging.getLogger(__name__)


class TFTForecaster(ForecastModel):
    """
    Temporal Fusion Transformer (TFT) forecasting model wrapper.
    Checks for trained PyTorch / PyTorch Forecasting model weights.
    If model weights are not loaded, falls back to MockForecaster for demo safety.
    """

    def __init__(self, model_path: str = "backend/ml/weights/tft_model.pt"):
        self.model_path = model_path
        self.model_loaded = os.path.exists(model_path)
        if self.model_loaded:
            logger.info(f"Loaded TFT model weights from {model_path}")
            # Placeholder for loading actual PyTorch TFT model
        else:
            logger.info(f"TFT weights not found at {model_path}. Operating in placeholder mode.")

    def predict(self, request: ForecastRequest) -> ForecastResponse:
        if not self.model_loaded:
            response = MockForecaster().predict(request)
            response.model_used = "tft (placeholder -> fallback to mock)"
            return response

        # When trained TFT model is plugged in:
        # 1. Preprocess request into time-series features
        # 2. Run torch model inference
        # 3. Format predictions into ForecastResponse
        raise NotImplementedError("TFT model loading and inference logic will be wired once ML weights are placed in backend/ml/weights/")
