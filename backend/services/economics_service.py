import math
from typing import Dict, Any
from backend.utils.constants import (
    VESSEL_CLASSES,
    ROUTE_DISTANCES_NM,
    DEFAULT_DISTANCE_NM,
    BUNKER_PRICE_USD_PER_TON,
    PORT_COST_FLAT_USD,
    PORT_CONSTRAINTS
)


class EconomicsService:
    """
    Voyage Economics Service for estimating voyage duration, fuel costs, time-charter rates,
    total voyage expenditure, and unit cost per metric tonne ($/MT).
    """

    def calculate_voyage_economics(
        self,
        vessel_class: str,
        cargo_quantity_mt: float,
        origin: str = "Australia",
        destination: str = "Paradip",
        spot_rate_per_mt: float = 31.4
    ) -> Dict[str, Any]:
        vessel_specs = VESSEL_CLASSES.get(vessel_class, VESSEL_CLASSES["Panamax"])
        distance_nm = ROUTE_DISTANCES_NM.get((origin, destination), DEFAULT_DISTANCE_NM)

        speed_knots = vessel_specs["avg_speed_knots"]
        sea_days = (distance_nm / (speed_knots * 24.0)) * 2.0  # Round trip ballast + laden

        # Port handling time
        port_info = PORT_CONSTRAINTS.get(destination, {})
        handling_rate = port_info.get("handling_rate_tpd", 25000)
        port_days = (cargo_quantity_mt / handling_rate) + 2.0  # Loading + discharge + waiting

        total_days = math.ceil(sea_days + port_days)

        daily_rate = vessel_specs["base_daily_charter_usd"]
        fuel_tpd = vessel_specs["fuel_consumption_tpd"]

        tc_cost = total_days * daily_rate
        bunker_cost = sea_days * fuel_tpd * BUNKER_PRICE_USD_PER_TON
        port_cost = PORT_COST_FLAT_USD * 2.0

        estimated_total_voyage_cost = tc_cost + bunker_cost + port_cost
        spot_implied_cost = cargo_quantity_mt * spot_rate_per_mt

        cost_per_mt = round(estimated_total_voyage_cost / max(cargo_quantity_mt, 1.0), 2)

        return {
            "vessel_class": vessel_class,
            "cargo_quantity_mt": cargo_quantity_mt,
            "distance_nm": distance_nm,
            "total_days": total_days,
            "sea_days": round(sea_days, 1),
            "port_days": round(port_days, 1),
            "daily_charter_rate_usd": daily_rate,
            "time_charter_cost_usd": round(tc_cost, 2),
            "bunker_cost_usd": round(bunker_cost, 2),
            "port_costs_usd": round(port_cost, 2),
            "total_voyage_cost_usd": round(estimated_total_voyage_cost, 2),
            "cost_per_mt": cost_per_mt,
            "spot_implied_cost_usd": round(spot_implied_cost, 2)
        }
