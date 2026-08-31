import logging
from typing import List
from backend.models.schemas import RiskRequest, RiskResponse, RiskFactor

logger = logging.getLogger(__name__)


class RiskService:
    """
    Risk Assessment Engine evaluating market rate uncertainty, spot rate volatility,
    port congestion, and vessel availability.
    """

    def assess_risk(self, request: RiskRequest) -> RiskResponse:
        forecast_rate = request.forecast_rate
        current_rate = request.current_rate
        pred_interval = request.prediction_interval
        volatility = request.market_volatility
        congestion = request.port_congestion
        availability = request.vessel_availability
        constraints = request.operational_constraints

        factors: List[RiskFactor] = []
        warnings: List[str] = []

        # 1. Forecast Trend & Spread Risk (0-30 pts)
        rate_diff_pct = (forecast_rate - current_rate) / max(current_rate, 1.0)
        if rate_diff_pct > 0.10:
            trend_score = 25.0
            factors.append(RiskFactor(factor="Forecast uncertainty (Upward price pressure)", impact="HIGH"))
            warnings.append("Forecasted freight rates show significant upward momentum.")
        elif rate_diff_pct > 0.02:
            trend_score = 15.0
            factors.append(RiskFactor(factor="Forecast uncertainty", impact="MEDIUM"))
        else:
            trend_score = 5.0
            factors.append(RiskFactor(factor="Forecast uncertainty", impact="LOW"))

        # 2. Market Volatility (0-25 pts)
        vol_score = min(volatility * 80.0, 25.0)
        vol_impact = "HIGH" if vol_score > 18 else ("MEDIUM" if vol_score > 10 else "LOW")
        factors.append(RiskFactor(factor="Market volatility", impact=vol_impact))
        if vol_impact == "HIGH":
            warnings.append("High spot market freight volatility detected.")

        # 3. Port Congestion Risk (0-25 pts)
        congestion_score = min(congestion * 30.0, 25.0)
        cong_impact = "HIGH" if congestion_score > 18 else ("MEDIUM" if congestion_score > 10 else "LOW")
        factors.append(RiskFactor(factor="Port congestion", impact=cong_impact))
        if cong_impact == "HIGH":
            warnings.append("Elevated vessel waiting times at destination port.")

        # 4. Vessel Availability Risk (0-20 pts)
        unavail = max(0.0, 1.0 - availability)
        avail_score = min(unavail * 25.0, 20.0)
        avail_impact = "HIGH" if avail_score > 15 else ("MEDIUM" if avail_score > 8 else "LOW")
        factors.append(RiskFactor(factor="Vessel availability", impact=avail_impact))
        if avail_impact == "HIGH":
            warnings.append("Tight vessel supply in origin loading region.")

        # Total combined risk score (0 - 100)
        total_risk_score = round(min(100.0, trend_score + vol_score + congestion_score + avail_score), 1)

        # Operational constraints penalty
        if constraints:
            total_risk_score = min(100.0, total_risk_score + len(constraints) * 5.0)

        if total_risk_score <= 30.0:
            risk_level = "LOW"
        elif total_risk_score <= 60.0:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        return RiskResponse(
            risk_score=total_risk_score,
            risk_level=risk_level,
            factors=factors,
            warnings=warnings
        )
