from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import FreightPredictRequest, FreightPredictResponse
from backend.services.freight_service import FreightService

router = APIRouter(tags=["Freight Prediction"])
freight_service = FreightService()


@router.post("/freight/predict", response_model=FreightPredictResponse)
def predict_freight(request: FreightPredictRequest):
    """
    Predict spot freight rate (Spot_Freight_USD_MT) using trained XGBoost model.
    """
    try:
        return freight_service.predict_freight(request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Freight prediction endpoint error: {str(e)}"
        )
