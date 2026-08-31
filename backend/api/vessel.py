from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import VesselRecommendRequest, VesselRecommendResponse
from backend.services.vessel_service import VesselService

router = APIRouter(tags=["Vessel Feasibility"])
vessel_service = VesselService()


@router.post("/vessel/recommend", response_model=VesselRecommendResponse)
def recommend_vessel(request: VesselRecommendRequest):
    """
    Recommend optimal vessel class based on trained XGBoost model, route bottleneck draft, and SHAP explainability.
    """
    try:
        return vessel_service.recommend_vessels(request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vessel recommendation error: {str(e)}"
        )

