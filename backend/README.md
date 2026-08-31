# PORTWISE AI — FastAPI Backend

**Intelligent Freight Forecasting Engine for Optimized Vessel Chartering and Bulk Cargo Procurement**  
*Smart India Hackathon (SIH) Solution for Overseas to East Coast India Trade Routes*

---

## 1. Project Overview

PORTWISE AI is an enterprise decision engine built for bulk freight procurement (Coal, Iron Ore, Bauxite). It helps organizations transition from reactive spot market contracts toward optimized short- and medium-term multi-voyage charter contracts.

### Key Capabilities
- **Freight Forecasting**: Predicts future freight rates across custom horizons.
- **Port Feasibility Engine**: Enforces strict physical infrastructure constraints (Max Draft, LOA, Beam, Cargo Capacity).
- **Vessel Recommendation**: Evaluates Handysize, Supramax, Panamax, and Capesize bulk carriers.
- **Risk Engine**: Calculates normalized risk scores (0–100) based on market volatility, forecast uncertainty, port congestion, and vessel availability.
- **Scenario Engine**: Compares SPOT, SHORT_TERM, and MEDIUM_TERM contract economics.
- **Unified Decision Engine**: Generates explainable, actionable chartering recommendations (`CHART_NOW`, `WAIT`, `PARTIAL_CHART`).

---

## 2. System Architecture

```text
                 FRONTEND (Portwise Dashboard)
                             │
                             ↓
                   FASTAPI API ROUTER
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
  POST /api/forecast  POST /api/vessel/recommend POST /api/risk
  POST /api/scenario  POST /api/analyze         GET /api/health
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ↓
                     SERVICES LAYER
     ├── ForecastService (MockForecaster / TFT / PatchTST)
     ├── PortService & VesselService (Port Feasibility Engine)
     ├── EconomicsService (Voyage Economics & Cost Calculations)
     ├── RiskService (Normalized Risk Scoring 0-100)
     ├── ScenarioService (Spot vs Short-Term vs Medium-Term)
     └── DecisionService (Final Recommendation Engine)
                             │
                             ↓
                     DATABASE & UTILS
     ├── SQLAlchemy Models (Port, Vessel, FreightRecord)
     ├── SQLite Database Initialization & Data Preloading
     └── Centralized Constants & Formula Utilities
```

---

## 3. Installation & Prerequisites

- Python 3.11+
- Virtualenv (recommended)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 4. Environment Variables (`.env`)

Create a `.env` file in `backend/`:

```env
APP_NAME=PORTWISE AI Backend
VERSION=0.1.0
DEBUG=true
PORT=8000
HOST=0.0.0.0
DEMO_MODE=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
DATABASE_URL=sqlite:///./portwise.db
```

---

## 5. Running Locally

Start the development server with Uvicorn:

```bash
python main.py
```
or
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Swagger Documentation
Access interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 6. API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status and version |
| `POST` | `/api/forecast` | Forecast freight rates for specified route & horizon |
| `POST` | `/api/vessel/recommend` | Evaluate vessel feasibility and recommendation |
| `POST` | `/api/risk` | Assess market freight risk score (0-100) |
| `POST` | `/api/scenario` | Compare SPOT vs SHORT_TERM vs MEDIUM_TERM contracts |
| `POST` | `/api/analyze` | Unified decision orchestration pipeline |

---

## 7. Example Requests & Responses

### 7.1 Unified Analysis (`POST /api/analyze`)

**Request**:
```json
{
  "commodity": "Coal",
  "cargo_quantity_mt": 70000,
  "origin": "Australia",
  "destination": "Paradip",
  "contract_duration_months": 6,
  "number_of_voyages": 3,
  "forecast_horizon_days": 30,
  "preferred_model": "auto"
}
```

**Response**:
```json
{
  "recommendation": "WAIT",
  "recommended_vessel": "Panamax",
  "contract_strategy": "SHORT_TERM",
  "forecast": {
    "model_used": "mock",
    "route": {
      "origin": "Australia",
      "destination": "Paradip",
      "vessel_class": "Panamax"
    },
    "current_rate": 31.4,
    "forecast_rate": 27.61,
    "lower_bound": 23.47,
    "upper_bound": 31.75,
    "confidence": 0.78,
    "trend": "DOWN",
    "forecast_points": [...]
  },
  "vessel_analysis": {
    "recommended_vessel": "Panamax",
    "options": [
      {
        "vessel_class": "Handysize",
        "feasible": true,
        "score": 72.0,
        "reason": "Feasible but requires multiple shipments (2 voyages) for total cargo."
      },
      {
        "vessel_class": "Supramax",
        "feasible": true,
        "score": 72.0,
        "reason": "Feasible but requires multiple shipments (1 voyages) for total cargo."
      },
      {
        "vessel_class": "Panamax",
        "feasible": true,
        "score": 95.0,
        "reason": "Optimal Panamax parcel size for East Coast India ports."
      },
      {
        "vessel_class": "Capesize",
        "feasible": false,
        "score": 0.0,
        "reason": "Port draft/LOA constraint. Vessel draft (18.2m) exceeds port maximum draft (14.5m)."
      }
    ]
  },
  "risk": {
    "risk_score": 29.0,
    "risk_level": "LOW",
    "factors": [
      {"factor": "Forecast uncertainty", "impact": "LOW"},
      {"factor": "Market volatility", "impact": "MEDIUM"}
    ],
    "warnings": []
  },
  "scenarios": {
    "recommended_strategy": "SHORT_TERM",
    "scenarios": [
      {"strategy": "SPOT", "estimated_cost": 6216000.0, "risk_score": 58.0},
      {"strategy": "SHORT_TERM", "estimated_cost": 5604900.0, "risk_score": 28.0},
      {"strategy": "MEDIUM_TERM", "estimated_cost": 5720400.0, "risk_score": 35.0}
    ]
  },
  "estimated_saving": 611100.0,
  "confidence": 0.78,
  "explanation": "Freight rates are forecasted to decrease from $31.4/MT to $27.61/MT over the next horizon (DOWN trend). Holding off on immediate charter contracts is recommended to secure lower spot or short-term multi-voyage rates. Recommended strategy: SHORT_TERM contract with Panamax vessels."
}
```

---

## 8. ML Model Integration (TFT & PatchTST)

The backend features an abstract `ForecastModel` base interface in `ml/model_interface.py`.

### How to Integrate Trained Models:
1. Place model checkpoint files in `backend/ml/weights/`:
   - `tft_model.pt`
   - `patchtst_model.pt`
2. Update `tft_forecaster.py` or `patchtst_forecaster.py` to load tensor weights and run PyTorch inference.
3. Call `/api/forecast` or `/api/analyze` passing `"preferred_model": "tft"` or `"patchtst"`.
4. If weight files are absent, the system automatically falls back to `MockForecaster` for 100% demo stability.

---

## 9. Demo-Safe Mode

Set `DEMO_MODE=true` in `.env`.
In Demo-Safe Mode:
- Zero external API dependencies required.
- Uses preloaded datasets in `backend/data/`.
- Pre-calculates physical port constraints for East Coast India (Paradip, Vizag, Dhamra, Haldia, Chennai).
- Guarantees fast, deterministic demonstration outputs during live hackathon presentations.

---

## 10. Automated Testing

Run the full pytest suite:

```bash
python -m pytest backend/tests/
```
