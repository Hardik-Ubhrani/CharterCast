import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "PORTWISE AI Backend"


def test_forecast_valid_request():
    payload = {
        "origin": "Australia",
        "destination": "Paradip",
        "vessel_class": "Panamax",
        "forecast_horizon_days": 30,
        "model": "auto"
    }
    response = client.post("/api/forecast", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "current_rate" in data
    assert "forecast_rate" in data
    assert "trend" in data
    assert len(data["forecast_points"]) == 30


def test_forecast_invalid_horizon():
    payload = {
        "origin": "Australia",
        "destination": "Paradip",
        "forecast_horizon_days": 500  # Exceeds max 180
    }
    response = client.post("/api/forecast", json=payload)
    assert response.status_code == 422  # Validation error


def test_vessel_recommend_case1_prototype():
    payload = {
        "origin_port": "Paradip Port",
        "destination_port": "Maurer",
        "consignment_size": 50000,
        "budget": 150000
    }
    response = client.post("/api/vessel/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommended_vessel"].upper() in ["HANDYMAX / SUPRAMAX", "SUPRAMAX"]
    assert data["route"]["origin_port"] == "Paradip Port"
    assert data["route"]["destination_port"] == "Maurer"
    assert data["consignment_size"] == 50000
    assert data["budget"] == 150000
    assert data["route_max_draft"] == 11.0
    assert "explanation" in data
    assert "consignment_size" in data["explanation"]


def test_vessel_recommend_case2_prototype():
    payload = {
        "origin_port": "Visakhapatnam (Vizag) Port",
        "destination_port": "Iharana",
        "consignment_size": 140000,
        "budget": 220000
    }
    response = client.post("/api/vessel/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommended_vessel"].upper() == "VALEMAX"
    assert data["route"]["origin_port"] == "Visakhapatnam (Vizag) Port"
    assert data["route"]["destination_port"] == "Iharana"
    assert data["route_max_draft"] == 14.0


def test_vessel_recommend_unknown_origin_port():
    payload = {
        "origin_port": "NonExistentPortXYZ999",
        "destination_port": "Maurer",
        "consignment_size": 50000,
        "budget": 150000
    }
    response = client.post("/api/vessel/recommend", json=payload)
    assert response.status_code == 400
    assert "Unknown origin port" in response.json()["detail"]


def test_vessel_recommend_unknown_dest_port():
    payload = {
        "origin_port": "Paradip Port",
        "destination_port": "NonExistentPortXYZ999",
        "consignment_size": 50000,
        "budget": 150000
    }
    response = client.post("/api/vessel/recommend", json=payload)
    assert response.status_code == 400
    assert "Unknown destination port" in response.json()["detail"]


def test_vessel_recommend_invalid_cargo():
    payload = {
        "origin_port": "Paradip Port",
        "destination_port": "Maurer",
        "consignment_size": -5000,
        "budget": 150000
    }
    response = client.post("/api/vessel/recommend", json=payload)
    assert response.status_code == 422


def test_vessel_model_loading_failure():
    from backend.services.vessel_service import VesselService
    from backend.models.schemas import VesselRecommendRequest
    from fastapi import HTTPException
    
    svc = VesselService(model_path="invalid/path/model.pkl")
    with pytest.raises(HTTPException) as exc_info:
        svc.recommend_vessels(VesselRecommendRequest(
            origin_port="Paradip Port",
            destination_port="Maurer",
            consignment_size=50000,
            budget=150000
        ))
    assert exc_info.value.status_code == 500
    assert "not found" in exc_info.value.detail.lower()



def test_risk_assessment_valid():
    payload = {
        "forecast_rate": 27.8,
        "current_rate": 31.4,
        "prediction_interval": 0.15,
        "market_volatility": 0.20,
        "port_congestion": 0.10,
        "vessel_availability": 0.80
    }
    response = client.post("/api/risk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert isinstance(data["factors"], list)


def test_scenario_evaluation_valid():
    payload = {
        "cargo_quantity_mt": 70000,
        "origin": "Australia",
        "destination": "Paradip",
        "vessel_class": "Panamax",
        "contract_duration_months": 6,
        "number_of_voyages": 3,
        "current_rate": 31.4,
        "forecast_rate": 27.8
    }
    response = client.post("/api/scenario", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_strategy" in data
    assert len(data["scenarios"]) == 3


def test_analyze_valid_full_flow():
    payload = {
        "commodity": "Coal",
        "cargo_quantity_mt": 70000,
        "origin": "Australia",
        "destination": "Paradip",
        "contract_duration_months": 6,
        "number_of_voyages": 3,
        "forecast_horizon_days": 30,
        "preferred_model": "auto"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommendation"] in ["CHART_NOW", "WAIT", "PARTIAL_CHART"]
    assert data["recommended_vessel"] in ["Panamax", "Supramax", "Handysize", "Capesize"]
    assert data["contract_strategy"] in ["SPOT", "SHORT_TERM", "MEDIUM_TERM"]
    assert "forecast" in data
    assert "vessel_analysis" in data
    assert "risk" in data
    assert "scenarios" in data
    assert "explanation" in data


def test_analyze_unknown_port():
    payload = {
        "commodity": "Coal",
        "cargo_quantity_mt": 70000,
        "origin": "Australia",
        "destination": "UnknownPort123",
        "contract_duration_months": 6,
        "number_of_voyages": 3,
        "forecast_horizon_days": 30,
        "preferred_model": "auto"
    }
    # Unknown port should return 400 Bad Request
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 400


def test_freight_predict_valid():
    payload = {
        "bdi": 1772,
        "daily_time_charter": 18957,
        "newcastle_coal_price": 158.44,
        "voyage_distance_nm": 5120
    }
    response = client.post("/api/freight/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_freight_usd_mt" in data
    assert abs(data["predicted_freight_usd_mt"] - 21.06) < 1.0


def test_trade_route_optimize_valid():
    payload = {
        "origin": "Australia",
        "destination": "Dhamra",
        "commodity": "Coking Coal",
        "vessel_class": "Capesize"
    }
    response = client.post("/api/trade-route/optimize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["route_feasible"] is True
    assert data["recommended_route"] == ["Australia", "Lombok/Sunda Strait", "Dhamra"]
    assert data["distance_nm"] == 5050.0
    assert data["engine_name"] == "Constraint-Aware A* Route Engine"


def test_trade_route_optimize_infeasible():
    payload = {
        "origin": "Indonesia",
        "destination": "Haldia",
        "commodity": "Thermal Coal",
        "vessel_class": "Capesize"
    }
    response = client.post("/api/trade-route/optimize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["route_feasible"] is False
    assert data["reason"] is not None
    assert "exceeds" in data["reason"].lower() or "no feasible" in data["reason"].lower()


