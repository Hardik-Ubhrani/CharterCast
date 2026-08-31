from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import RiskRequest, RiskResponse
from backend.services.risk_service import RiskService

router = APIRouter(tags=["Risk Assessment"])
risk_service = RiskService()


@router.post("/risk", response_model=RiskResponse)
def assess_risk(request: RiskRequest):
    """
    Assess market freight risk score (0-100) and factors based on forecast uncertainty,
    volatility, port congestion, and vessel availability.
    """
    try:
        return risk_service.assess_risk(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk assessment error: {str(e)}"
        )
