"""
Centralized constants, defaults, and domain configuration for PORTWISE AI.
"""

# Vessel Classes and Technical Specifications (Defaults)
VESSEL_CLASSES = {
    "Handysize": {
        "min_dwt": 10000,
        "max_dwt": 40000,
        "typical_dwt": 35000,
        "max_draft_m": 10.0,
        "max_loa_m": 180.0,
        "max_beam_m": 28.0,
        "base_daily_charter_usd": 12000,
        "avg_speed_knots": 13.0,
        "fuel_consumption_tpd": 22.0
    },
    "Supramax": {
        "min_dwt": 40001,
        "max_dwt": 65000,
        "typical_dwt": 58000,
        "max_draft_m": 12.8,
        "max_loa_m": 200.0,
        "max_beam_m": 32.3,
        "base_daily_charter_usd": 15500,
        "avg_speed_knots": 13.5,
        "fuel_consumption_tpd": 28.0
    },
    "Panamax": {
        "min_dwt": 65001,
        "max_dwt": 85000,
        "typical_dwt": 75000,
        "max_draft_m": 14.5,
        "max_loa_m": 229.0,
        "max_beam_m": 32.3,
        "base_daily_charter_usd": 18500,
        "avg_speed_knots": 14.0,
        "fuel_consumption_tpd": 32.0
    },
    "Capesize": {
        "min_dwt": 120000,
        "max_dwt": 210000,
        "typical_dwt": 180000,
        "max_draft_m": 18.2,
        "max_loa_m": 300.0,
        "max_beam_m": 45.0,
        "base_daily_charter_usd": 24000,
        "avg_speed_knots": 14.5,
        "fuel_consumption_tpd": 45.0
    }
}

# Major Bulk Freight Ports (Default Infrastructure Constraints for East Coast India)
PORT_CONSTRAINTS = {
    "Paradip": {
        "name": "Paradip Port",
        "max_draft_m": 14.5,
        "max_loa_m": 230.0,
        "max_beam_m": 33.0,
        "handling_rate_tpd": 25000,
        "lat": 20.2644,
        "lon": 86.6713
    },
    "Visakhapatnam": {
        "name": "Visakhapatnam (Vizag) Port",
        "max_draft_m": 14.0,
        "max_loa_m": 230.0,
        "max_beam_m": 32.5,
        "handling_rate_tpd": 22000,
        "lat": 17.6868,
        "lon": 83.2185
    },
    "Dhamra": {
        "name": "Dhamra Port",
        "max_draft_m": 17.5,
        "max_loa_m": 295.0,
        "max_beam_m": 45.0,
        "handling_rate_tpd": 35000,
        "lat": 20.8030,
        "lon": 86.9730
    },
    "Haldia": {
        "name": "Haldia Dock Complex",
        "max_draft_m": 8.5,
        "max_loa_m": 190.0,
        "max_beam_m": 27.0,
        "handling_rate_tpd": 12000,
        "lat": 22.0257,
        "lon": 88.0583
    },
    "Chennai": {
        "name": "Chennai Port",
        "max_draft_m": 14.0,
        "max_loa_m": 230.0,
        "max_beam_m": 33.0,
        "handling_rate_tpd": 20000,
        "lat": 13.0827,
        "lon": 80.2707
    }
}

# Standard Voyage Route Distances in Nautical Miles (Approximate)
ROUTE_DISTANCES_NM = {
    ("Australia", "Paradip"): 4500,
    ("Australia", "Visakhapatnam"): 4600,
    ("Australia", "Dhamra"): 4450,
    ("Australia", "Haldia"): 4700,
    ("Australia", "Chennai"): 4300,
    ("Indonesia", "Paradip"): 2100,
    ("Indonesia", "Visakhapatnam"): 2000,
    ("Indonesia", "Dhamra"): 2150,
    ("Indonesia", "Haldia"): 2250,
    ("Indonesia", "Chennai"): 1800,
    ("South Africa", "Paradip"): 4600,
    ("South Africa", "Visakhapatnam"): 4500,
    ("South Africa", "Dhamra"): 4650,
    ("South Africa", "Haldia"): 4800,
    ("South Africa", "Chennai"): 4200,
    ("Russia", "Paradip"): 5000,
    ("Russia", "Visakhapatnam"): 5100,
    ("Russia", "Dhamra"): 4950,
    ("Russia", "Haldia"): 5200,
    ("Russia", "Chennai"): 5300
}

DEFAULT_DISTANCE_NM = 3500

# Voyage Economics Assumptions
BUNKER_PRICE_USD_PER_TON = 620.0  # VLSFO benchmark
PORT_COST_FLAT_USD = 35000.0

# Risk Thresholds
RISK_LEVELS = {
    "LOW": (0, 30),
    "MEDIUM": (31, 60),
    "HIGH": (61, 100)
}

# Contract Strategies
STRATEGIES = ["SPOT", "SHORT_TERM", "MEDIUM_TERM"]

# Decision Recommendations
RECOMMENDATIONS = ["CHART_NOW", "WAIT", "PARTIAL_CHART"]
