import logging
import os
import pickle
import pandas as pd
import numpy as np
from typing import Optional
from fastapi import HTTPException, status

from backend.models.schemas import FreightPredictRequest, FreightPredictResponse

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FREIGHT_MODEL_PATH = os.path.join(BASE_DIR, "ml", "weights", "xgboost_freight_model.pkl")

# Exact feature order required by the trained XGBoost model
FEATURE_COLUMNS = [
    "Baltic_Dry_Index_BDI",
    "Daily_Time_Charter_USD_Day",
    "Newcastle_Coal_USD_MT",
    "Voyage_Distance_NM"
]


class FreightService:
    """
    Trained XGBoost Freight Rate Inference Service.
    Loads trained XGBoost model from backend/ml/weights/xgboost_freight_model.pkl
    and provides spot freight rate predictions (Spot_Freight_USD_MT).
    """

    def __init__(self, model_path: str = DEFAULT_FREIGHT_MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.load_error = None

        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            self.load_error = f"Freight model pickle file not found at {self.model_path}"
            logger.error(self.load_error)
            return

        try:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
            logger.info(f"Freight model loaded successfully from {self.model_path}")
        except Exception as e:
            self.load_error = f"Failed to load freight model: {str(e)}"
            logger.error(self.load_error)

    def predict_freight(self, request: FreightPredictRequest) -> FreightPredictResponse:
        if self.model is None:
            error_msg = self.load_error or "Freight model is not loaded"
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )

        try:
            # Construct DataFrame with exact feature order required by model
            input_data = pd.DataFrame(
                [[
                    request.bdi,
                    request.daily_time_charter,
                    request.newcastle_coal_price,
                    request.voyage_distance_nm
                ]],
                columns=FEATURE_COLUMNS
            )

            prediction = self.model.predict(input_data)
            
            if isinstance(prediction, (list, np.ndarray)):
                predicted_val = float(prediction[0])
            else:
                predicted_val = float(prediction)

            return FreightPredictResponse(
                predicted_freight_usd_mt=predicted_val
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Freight rate prediction error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Freight prediction error: {str(e)}"
            )
