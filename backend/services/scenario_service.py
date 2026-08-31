import logging
from typing import List
from backend.models.schemas import ScenarioRequest, ScenarioResponse, ScenarioItem
from backend.services.economics_service import EconomicsService

logger = logging.getLogger(__name__)


class ScenarioService:
    """
    Scenario Analysis Engine comparing SPOT (individual voyages), SHORT_TERM (multi-voyage contract),
    and MEDIUM_TERM (longer term contract) strategies.
    """

    def __init__(self, economics_service: EconomicsService = None):
        self.economics_service = economics_service or EconomicsService()

    def evaluate_scenarios(self, request: ScenarioRequest) -> ScenarioResponse:
        cargo_mt = request.cargo_quantity_mt
        num_voyages = request.number_of_voyages
        total_cargo_mt = cargo_mt * num_voyages
        current_rate = request.current_rate
        forecast_rate = request.forecast_rate

        # 1. SPOT Strategy: Exposed to full market fluctuations across voyages
        avg_expected_spot = (current_rate + forecast_rate) / 2.0
        spot_cost = round(total_cargo_mt * avg_expected_spot, 2)
        spot_risk = 58.0  # High exposure to spot rate swings

        # 2. SHORT_TERM Contract: Locks in discount on forecast rate (e.g. 3-5% discount for guaranteed volume)
        short_term_rate = round(min(current_rate, forecast_rate) * 0.96, 2)
        short_term_cost = round(total_cargo_mt * short_term_rate, 2)
        short_term_risk = 28.0  # Low risk, locks in lower rate

        # 3. MEDIUM_TERM Contract: Includes market premium for longer commitment
        medium_term_rate = round(min(current_rate, forecast_rate) * 0.98, 2)
        medium_term_cost = round(total_cargo_mt * medium_term_rate, 2)
        medium_term_risk = 35.0  # Medium risk, slightly longer lock-in

        scenarios = [
            ScenarioItem(
                strategy="SPOT",
                estimated_cost=spot_cost,
                risk_score=spot_risk
            ),
            ScenarioItem(
                strategy="SHORT_TERM",
                estimated_cost=short_term_cost,
                risk_score=short_term_risk
            ),
            ScenarioItem(
                strategy="MEDIUM_TERM",
                estimated_cost=medium_term_cost,
                risk_score=medium_term_risk
            )
        ]

        # Recommend strategy with lowest cost-to-risk metric
        best_strategy = min(scenarios, key=lambda s: s.estimated_cost * (1.0 + s.risk_score / 200.0)).strategy

        return ScenarioResponse(
            recommended_strategy=best_strategy,
            scenarios=scenarios
        )
