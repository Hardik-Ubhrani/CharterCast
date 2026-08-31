import logging
from typing import Dict, Any
from backend.models.schemas import (
    ForecastResponse,
    VesselRecommendResponse,
    RiskResponse,
    ScenarioResponse
)

logger = logging.getLogger(__name__)


class DecisionService:
    """
    Core Decision Engine for PORTWISE AI.
    Synthesizes ML freight forecasts, port feasibility, risk metrics, and contract scenarios
    to generate explainable chartering recommendations (CHART_NOW, WAIT, PARTIAL_CHART).
    """

    def synthesize_decision(
        self,
        forecast: ForecastResponse,
        vessel_analysis: VesselRecommendResponse,
        risk: RiskResponse,
        scenarios: ScenarioResponse,
        cargo_quantity_mt: float,
        number_of_voyages: int
    ) -> Dict[str, Any]:
        curr_rate = forecast.current_rate
        fore_rate = forecast.forecast_rate
        trend = forecast.trend
        risk_score = risk.risk_score

        rec_vessel = vessel_analysis.recommended_vessel
        contract_strategy = scenarios.recommended_strategy

        # Calculate estimated savings comparing SPOT vs Recommended strategy
        spot_item = next((s for s in scenarios.scenarios if s.strategy == "SPOT"), None)
        rec_item = next((s for s in scenarios.scenarios if s.strategy == contract_strategy), None)

        if spot_item and rec_item:
            estimated_saving = max(0.0, spot_item.estimated_cost - rec_item.estimated_cost)
        else:
            estimated_saving = 0.0

        # Decision rules
        if trend == "DOWN" and (curr_rate - fore_rate) / curr_rate >= 0.05:
            recommendation = "WAIT"
            explanation = (
                f"Freight rates are forecasted to decrease from ${curr_rate}/MT to ${fore_rate}/MT over the next "
                f"horizon ({trend} trend). Holding off on immediate charter contracts is recommended to secure lower "
                f"spot or short-term multi-voyage rates. Recommended strategy: {contract_strategy} contract with {rec_vessel} vessels."
            )
        elif trend == "UP" and (fore_rate - curr_rate) / curr_rate >= 0.05:
            recommendation = "CHART_NOW"
            explanation = (
                f"Freight rates are forecasted to rise from ${curr_rate}/MT to ${fore_rate}/MT ({trend} trend). "
                f"Locking in a {contract_strategy} contract immediately on {rec_vessel} vessels will protect against "
                f"impending rate increases and save an estimated ${estimated_saving:,.2f}."
            )
        elif risk_score > 60.0:
            recommendation = "PARTIAL_CHART"
            explanation = (
                f"High market risk score ({risk_score}/100) detected. Hedging risk by executing a PARTIAL_CHART strategy "
                f"(covering 50% cargo via short-term contract and keeping 50% in spot) optimizes voyage economics while mitigating volatility."
            )
        else:
            recommendation = "CHART_NOW"
            explanation = (
                f"Freight rates remain stable (${curr_rate} -> ${fore_rate}/MT) with LOW/MEDIUM risk ({risk_score}/100). "
                f"Executing a {contract_strategy} contract on {rec_vessel} vessels offers the best balance of operational feasibility and rate predictability."
            )

        return {
            "recommendation": recommendation,
            "recommended_vessel": rec_vessel,
            "contract_strategy": contract_strategy,
            "estimated_saving": round(estimated_saving, 2),
            "confidence": forecast.confidence,
            "explanation": explanation
        }
