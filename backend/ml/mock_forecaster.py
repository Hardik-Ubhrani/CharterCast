from datetime import datetime, timedelta
import numpy as np
from backend.ml.model_interface import ForecastModel
from backend.models.schemas import ForecastRequest, ForecastResponse, ForecastPoint


class MockForecaster(ForecastModel):
    """
    Mock forecasting model for initial development, testing, and frontend integration.
    Generates realistic trajectory curve, confidence intervals, and trend indicators.
    """

    def predict(self, request: ForecastRequest) -> ForecastResponse:
        origin = request.origin
        destination = request.destination
        vessel_class = request.vessel_class
        horizon = request.forecast_horizon_days

        # Base current rate depends slightly on vessel class
        base_rates = {
            "Handysize": 22.5,
            "Supramax": 26.0,
            "Panamax": 31.4,
            "Capesize": 38.0
        }
        current_rate = base_rates.get(vessel_class, 31.4)

        # Generate a mild downward or upward curve depending on origin
        # (For demonstration: Australia -> India often experiences seasonal dips in winter/spring)
        is_dip_route = "australia" in origin.lower() or "indonesia" in origin.lower()
        target_rate = round(current_rate * (0.885 if is_dip_route else 1.05), 1)

        forecast_points = []
        today = datetime.now()

        for i in range(1, horizon + 1):
            date_str = (today + timedelta(days=i)).strftime("%Y-%m-%d")
            # Smooth trajectory from current_rate to target_rate with slight sine wave fluctuation
            progress = i / horizon
            interp_rate = current_rate + (target_rate - current_rate) * (progress ** 0.8)
            fluctuation = np.sin(i * 0.4) * 0.35
            rate = round(float(interp_rate + fluctuation), 2)

            margin = round(0.05 + 0.10 * progress, 2)
            lower = round(rate * (1.0 - margin), 2)
            upper = round(rate * (1.0 + margin), 2)

            forecast_points.append(
                ForecastPoint(
                    day=i,
                    date=date_str,
                    rate=rate,
                    lower_bound=lower,
                    upper_bound=upper
                )
            )

        final_point = forecast_points[-1]
        forecast_rate = final_point.rate

        # Calculate bounds and trend
        overall_lower = round(min(p.lower_bound for p in forecast_points[-5:]), 1)
        overall_upper = round(max(p.upper_bound for p in forecast_points[-5:]), 1)

        if forecast_rate < current_rate * 0.96:
            trend = "DOWN"
        elif forecast_rate > current_rate * 1.04:
            trend = "UP"
        else:
            trend = "STABLE"

        return ForecastResponse(
            model_used="mock",
            route={
                "origin": origin,
                "destination": destination,
                "vessel_class": vessel_class
            },
            current_rate=current_rate,
            forecast_rate=forecast_rate,
            lower_bound=overall_lower,
            upper_bound=overall_upper,
            confidence=0.78,
            trend=trend,
            forecast_points=forecast_points
        )
