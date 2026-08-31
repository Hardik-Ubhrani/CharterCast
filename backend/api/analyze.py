from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ForecastRequest,
    VesselRecommendRequest,
    RiskRequest,
    ScenarioRequest
)
from backend.services.forecast_service import ForecastService
from backend.services.vessel_service import VesselService
from backend.services.risk_service import RiskService
from backend.services.scenario_service import ScenarioService
from backend.services.decision_service import DecisionService

router = APIRouter(tags=["Main Decision Engine"])

forecast_service = ForecastService()
vessel_service = VesselService()
risk_service = RiskService()
scenario_service = ScenarioService()
decision_service = DecisionService()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_freight_and_charter(request: AnalyzeRequest):
    """
    Main orchestration endpoint for PORTWISE AI.
    Executes input validation, freight forecast, vessel feasibility, risk scoring, scenario comparison,
    and decision synthesis into a single unified recommendation response.
    """
    try:
        # 1. Freight Forecast
        forecast_req = ForecastRequest(
            origin=request.origin,
            destination=request.destination,
            vessel_class="Panamax",  # Initial default for route lookup
            forecast_horizon_days=request.forecast_horizon_days,
            model=request.preferred_model
        )
        forecast_res = forecast_service.get_forecast(forecast_req)

        # 2. Vessel Recommendation & Feasibility Engine
        vessel_req = VesselRecommendRequest(
            cargo_quantity_mt=request.cargo_quantity_mt,
            origin=request.origin,
            destination=request.destination
        )
        vessel_res = vessel_service.recommend_vessels(vessel_req)

        # Update forecast if recommended vessel differs
        if vessel_res.recommended_vessel != "Panamax":
            forecast_req.vessel_class = vessel_res.recommended_vessel
            forecast_res = forecast_service.get_forecast(forecast_req)

        # 3. Risk Assessment Engine
        risk_req = RiskRequest(
            forecast_rate=forecast_res.forecast_rate,
            current_rate=forecast_res.current_rate,
            prediction_interval=0.15,
            market_volatility=0.20,
            port_congestion=0.10,
            vessel_availability=0.80
        )
        risk_res = risk_service.assess_risk(risk_req)

        # 4. Scenario Analysis Engine
        scenario_req = ScenarioRequest(
            cargo_quantity_mt=request.cargo_quantity_mt,
            origin=request.origin,
            destination=request.destination,
            vessel_class=vessel_res.recommended_vessel,
            contract_duration_months=request.contract_duration_months,
            number_of_voyages=request.number_of_voyages,
            current_rate=forecast_res.current_rate,
            forecast_rate=forecast_res.forecast_rate
        )
        scenario_res = scenario_service.evaluate_scenarios(scenario_req)

        # 5. Decision Engine Synthesis
        decision = decision_service.synthesize_decision(
            forecast=forecast_res,
            vessel_analysis=vessel_res,
            risk=risk_res,
            scenarios=scenario_res,
            cargo_quantity_mt=request.cargo_quantity_mt,
            number_of_voyages=request.number_of_voyages
        )

        return AnalyzeResponse(
            recommendation=decision["recommendation"],
            recommended_vessel=decision["recommended_vessel"],
            contract_strategy=decision["contract_strategy"],
            forecast=forecast_res,
            vessel_analysis=vessel_res,
            risk=risk_res,
            scenarios=scenario_res,
            estimated_saving=decision["estimated_saving"],
            confidence=decision["confidence"],
            explanation=decision["explanation"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis orchestration error: {str(e)}"
        )

