from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator


# --- FORECAST SCHEMAS ---
class ForecastRequest(BaseModel):
    origin: str = Field(default="Australia", description="Country or port of origin")
    destination: str = Field(default="Paradip", description="Destination port in East Coast India")
    vessel_class: str = Field(default="Panamax", description="Target vessel class (Handysize, Supramax, Panamax, Capesize)")
    forecast_horizon_days: int = Field(default=30, ge=1, le=180, description="Forecast horizon in days")
    model: str = Field(default="auto", description="Model selection: mock, tft, patchtst, auto")


class ForecastPoint(BaseModel):
    day: int
    date: str
    rate: float
    lower_bound: float
    upper_bound: float


class ForecastResponse(BaseModel):
    model_used: str
    route: Dict[str, str]
    current_rate: float
    forecast_rate: float
    lower_bound: float
    upper_bound: float
    confidence: float
    trend: str  # UP, DOWN, STABLE
    forecast_points: List[ForecastPoint]


# --- VESSEL SCHEMAS ---
class VesselOption(BaseModel):
    vessel_class: str
    feasible: bool
    score: float
    reason: str


class RouteInfo(BaseModel):
    origin_port: str
    destination_port: str


class VesselRecommendRequest(BaseModel):
    origin_port: Optional[str] = Field(default=None, description="Origin port or region")
    origin: Optional[str] = Field(default=None, description="Origin port alias for backwards compatibility")
    destination_port: Optional[str] = Field(default=None, description="Destination port")
    destination: Optional[str] = Field(default=None, description="Destination port alias for backwards compatibility")
    consignment_size: Optional[float] = Field(default=None, gt=0, description="Consignment size in metric tonnes")
    cargo_quantity_mt: Optional[float] = Field(default=None, gt=0, description="Cargo quantity alias for backwards compatibility")
    budget: float = Field(default=150000.0, gt=0, description="Chartering budget in USD")

    @model_validator(mode="after")
    def validate_and_populate_fields(self):
        if not self.origin_port and self.origin:
            self.origin_port = self.origin
        if not self.origin_port:
            raise ValueError("origin_port or origin must be provided")

        if not self.destination_port and self.destination:
            self.destination_port = self.destination
        if not self.destination_port:
            raise ValueError("destination_port or destination must be provided")

        if self.consignment_size is None and self.cargo_quantity_mt is not None:
            self.consignment_size = self.cargo_quantity_mt
        if self.consignment_size is None:
            raise ValueError("consignment_size or cargo_quantity_mt must be provided and > 0")

        return self


class VesselRecommendResponse(BaseModel):
    recommended_vessel: str
    route: RouteInfo
    consignment_size: float
    budget: float
    route_max_draft: float
    explanation: Optional[Dict[str, float]] = None
    options: Optional[List[VesselOption]] = Field(default_factory=list)


# --- RISK SCHEMAS ---
class RiskFactor(BaseModel):
    factor: str
    impact: str  # LOW, MEDIUM, HIGH


class RiskRequest(BaseModel):
    forecast_rate: float = Field(..., gt=0, description="Forecasted freight rate ($/MT)")
    current_rate: float = Field(..., gt=0, description="Current freight rate ($/MT)")
    prediction_interval: float = Field(default=0.15, ge=0, description="Relative forecast uncertainty width")
    market_volatility: float = Field(default=0.20, ge=0, description="Historical market volatility ratio")
    port_congestion: float = Field(default=0.10, ge=0, le=1.0, description="Port congestion factor (0-1)")
    vessel_availability: float = Field(default=0.80, ge=0, le=1.0, description="Vessel availability factor (0-1)")
    operational_constraints: List[str] = Field(default_factory=list, description="List of active operational constraints")


class RiskResponse(BaseModel):
    risk_score: float
    risk_level: str  # LOW, MEDIUM, HIGH
    factors: List[RiskFactor]
    warnings: List[str]


# --- SCENARIO SCHEMAS ---
class ScenarioItem(BaseModel):
    strategy: str  # SPOT, SHORT_TERM, MEDIUM_TERM
    estimated_cost: float
    risk_score: float


class ScenarioRequest(BaseModel):
    cargo_quantity_mt: float = Field(default=70000, gt=0)
    origin: str = Field(default="Australia")
    destination: str = Field(default="Paradip")
    vessel_class: str = Field(default="Panamax")
    contract_duration_months: int = Field(default=6, ge=1)
    number_of_voyages: int = Field(default=3, ge=1)
    current_rate: float = Field(default=31.4, gt=0)
    forecast_rate: float = Field(default=27.8, gt=0)


class ScenarioResponse(BaseModel):
    recommended_strategy: str
    scenarios: List[ScenarioItem]


# --- MAIN ANALYZE SCHEMAS ---
class AnalyzeRequest(BaseModel):
    commodity: str = Field(default="Coal", description="Commodity type (e.g. Coal, Iron Ore, Bauxite)")
    cargo_quantity_mt: float = Field(default=70000, gt=0, description="Total cargo quantity in metric tonnes")
    origin: str = Field(default="Australia", description="Origin location")
    destination: str = Field(default="Paradip", description="Destination port")
    contract_duration_months: int = Field(default=6, ge=1, description="Target contract duration in months")
    number_of_voyages: int = Field(default=3, ge=1, description="Planned number of voyages")
    forecast_horizon_days: int = Field(default=30, ge=1, le=180, description="Forecast horizon in days")
    preferred_model: str = Field(default="auto", description="Preferred ML forecasting model")


class AnalyzeResponse(BaseModel):
    recommendation: str  # CHART_NOW, WAIT, PARTIAL_CHART
    recommended_vessel: str
    contract_strategy: str  # SPOT, SHORT_TERM, MEDIUM_TERM
    forecast: ForecastResponse
    vessel_analysis: VesselRecommendResponse
    risk: RiskResponse
    scenarios: ScenarioResponse
    estimated_saving: float
    confidence: float
    explanation: str


# --- FREIGHT PREDICT SCHEMAS ---
class FreightPredictRequest(BaseModel):
    bdi: float = Field(default=1850.0, description="Baltic Dry Index")
    daily_time_charter: float = Field(default=16500.0, description="Daily Time Charter rate ($/day)")
    newcastle_coal_price: float = Field(default=135.0, description="Newcastle Coal price ($/MT)")
    voyage_distance_nm: float = Field(default=4500.0, description="Voyage distance in nautical miles")


class FreightPredictResponse(BaseModel):
    predicted_freight_usd_mt: float
    model_name: str = Field(default="XGBoost Spot Freight Model")



# --- FREIGHT PREDICT SCHEMAS ---
class FreightPredictRequest(BaseModel):
    bdi: float = Field(default=1772, description="Baltic Dry Index")
    daily_time_charter: float = Field(default=18957, description="Daily Time Charter rate in USD/day")
    newcastle_coal_price: float = Field(default=158.44, description="Newcastle Coal price in USD/MT")
    voyage_distance_nm: float = Field(default=5120, description="Voyage distance in nautical miles")


class FreightPredictResponse(BaseModel):
    predicted_freight_usd_mt: float
    model_name: str = Field(default="XGBoost Freight Model")


# --- TRADE ROUTE SCHEMAS ---
class TradeRouteOptimizeRequest(BaseModel):
    origin: str = Field(default="Australia", description="Origin port or region")
    destination: str = Field(default="Dhamra", description="Destination port")
    commodity: str = Field(default="Coking Coal", description="Commodity type")
    vessel_class: str = Field(default="Capesize", description="Target vessel class")
    cargo_quantity: Optional[float] = Field(default=None, description="Cargo quantity in metric tonnes")


class TradeRouteOptimizeResponse(BaseModel):
    origin: str
    destination: str
    vessel_class: str
    recommended_route: List[str] = Field(default_factory=list)
    distance_nm: Optional[float] = None
    route_feasible: bool
    reason: Optional[str] = None
    engine_name: str = Field(default="Constraint-Aware A* Route Engine")


