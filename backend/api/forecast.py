from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import ForecastRequest, ForecastResponse
from backend.services.forecast_service import ForecastService

router = APIRouter(tags=["Freight Forecast"])
forecast_service = ForecastService()


@router.post("/forecast", response_model=ForecastResponse)
def get_freight_forecast(request: ForecastRequest):
    """
    Predict future freight rates for specified route, vessel class, and horizon.
    """
    try:
        return forecast_service.get_forecast(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Forecast calculation error: {str(e)}"
        )
