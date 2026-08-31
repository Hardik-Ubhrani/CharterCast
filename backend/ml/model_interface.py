from abc import ABC, abstractmethod
from typing import Dict, Any
from backend.models.schemas import ForecastRequest, ForecastResponse


class ForecastModel(ABC):
    """
    Abstract base interface for all freight rate forecasting models in PORTWISE AI.
    Models implementing this interface must provide a standard predict() method.
    """

    @abstractmethod
    def predict(self, request: ForecastRequest) -> ForecastResponse:
        """
        Generate freight forecast predictions for the given route, vessel class, and horizon.
        """
        pass
