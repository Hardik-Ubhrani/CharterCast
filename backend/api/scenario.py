from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import ScenarioRequest, ScenarioResponse
from backend.services.scenario_service import ScenarioService

router = APIRouter(tags=["Scenario Analysis"])
scenario_service = ScenarioService()


@router.post("/scenario", response_model=ScenarioResponse)
def evaluate_scenarios(request: ScenarioRequest):
    """
    Compare contract strategies (SPOT, SHORT_TERM, MEDIUM_TERM) and recommend optimal option.
    """
    try:
        return scenario_service.evaluate_scenarios(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scenario evaluation error: {str(e)}"
        )
