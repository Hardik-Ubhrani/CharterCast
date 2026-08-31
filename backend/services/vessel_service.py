import logging
import os
import pickle
import pandas as pd
import shap
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status

from backend.utils.constants import VESSEL_CLASSES
from backend.services.port_service import PortService
from backend.models.schemas import VesselRecommendRequest, VesselRecommendResponse, VesselOption, RouteInfo

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "ml", "portwise_vessel_model.pkl")


class VesselService:
    """
    Trained Prototype Vessel Recommendation Service.
    Loads trained XGBoost model bundle, validates port constraints, calculates route bottleneck draft,
    reproduces categorical preprocessing, predicts optimal vessel class, and generates SHAP feature explanations.
    """

    def __init__(self, port_service: Optional[PortService] = None, model_path: str = DEFAULT_MODEL_PATH):
        self.port_service = port_service or PortService()
        self.vessel_specs = VESSEL_CLASSES
        self.model_path = model_path
        self.model = None
        self.target_mapper = None
        self.inverse_mapper = None
        self.origin_categories = None
        self.destination_categories = None
        self.feature_columns = None
        self.explainer = None
        self.known_destinations = set()
        self.load_error = None

        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            self.load_error = f"Model bundle pickle file not found at {self.model_path}"
            logger.error(self.load_error)
            return

        try:
            with open(self.model_path, "rb") as f:
                bundle = pickle.load(f)
            self.model = bundle["model"]
            self.target_mapper = bundle["target_mapper"]
            self.inverse_mapper = bundle["inverse_mapper"]
            self.origin_categories = list(bundle["origin_categories"])
            self.destination_categories = list(bundle["destination_categories"])
            self.feature_columns = bundle["feature_columns"]
            
            # Combine trained destination categories and prototype ports
            self.known_destinations = set(self.destination_categories).union({"Maurer", "Iharana"})

            try:
                self.explainer = shap.TreeExplainer(self.model)
            except Exception as e:
                logger.warning(f"Failed to initialize SHAP explainer: {e}")
                self.explainer = None

            logger.info(f"Loaded vessel recommendation model from {self.model_path}")
        except Exception as e:
            self.load_error = f"Model loading error: {str(e)}"
            logger.error(self.load_error)

    def normalize_origin_port(self, port_name: str) -> Optional[str]:
        if not port_name or not isinstance(port_name, str):
            return None
        p = port_name.strip()
        if not self.origin_categories:
            return p
        if p in self.origin_categories:
            return p
        for cat in self.origin_categories:
            if p.lower() in cat.lower() or cat.lower() in p.lower():
                return cat
        if p in self.port_service.ports or any(p.lower() in k.lower() for k in self.port_service.ports.keys()):
            # Find matching category in origin_categories if possible
            for cat in self.origin_categories:
                if any(k.lower() in cat.lower() for k in self.port_service.ports.keys() if p.lower() in k.lower()):
                    return cat
            return "Paradip Port"
        # Support origin region/country defaults (e.g. Australia, Indonesia, South Africa, Russia)
        if p.lower() in ["australia", "indonesia", "south africa", "russia", "india"]:
            return "Paradip Port"
        return None

    def normalize_dest_port(self, port_name: str) -> Optional[str]:
        if not port_name or not isinstance(port_name, str):
            return None
        p = port_name.strip()
        if not self.known_destinations:
            return p
        if p in self.known_destinations:
            return p
        for cat in self.known_destinations:
            if p.lower() in cat.lower() or cat.lower() in p.lower():
                return cat
        if p in self.port_service.ports or any(p.lower() in k.lower() for k in self.port_service.ports.keys()):
            return p
        return None

    def recommend_vessels(self, request: VesselRecommendRequest) -> VesselRecommendResponse:
        if self.load_error or self.model is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=self.load_error or "Vessel model is not loaded."
            )

        origin_input = request.origin_port
        dest_input = request.destination_port

        # 1. Validate Ports
        canonical_origin = self.normalize_origin_port(origin_input)
        if not canonical_origin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown origin port: {origin_input}"
            )

        canonical_dest = self.normalize_dest_port(dest_input)
        if not canonical_dest:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown destination port: {dest_input}"
            )

        # Validate numeric inputs
        if request.consignment_size <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid consignment size: must be > 0"
            )
        if request.budget <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid budget: must be > 0"
            )

        # 2. Calculate Bottleneck Draft
        origin_info = self.port_service.get_port_info(origin_input)
        dest_info = self.port_service.get_port_info(dest_input)

        origin_draft = float(origin_info.get("max_draft_m", 14.5))
        dest_draft = float(dest_info.get("max_draft_m", 14.5))
        route_max_draft = min(origin_draft, dest_draft)

        if route_max_draft <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid route/draft information: calculated draft is <= 0"
            )

        # 3. Preprocessing (Exact Feature Order & Categorical Types)
        df = pd.DataFrame([{
            "origin_port": canonical_origin,
            "destination_port": canonical_dest,
            "consignment_size": float(request.consignment_size),
            "budget": float(request.budget),
            "route_max_draft": float(route_max_draft)
        }])

        df["origin_port"] = pd.Categorical(df["origin_port"], categories=self.origin_categories)
        df["destination_port"] = pd.Categorical(df["destination_port"], categories=self.destination_categories)
        df = df[self.feature_columns]

        # 4. Predict
        pred = self.model.predict(df)[0]
        if hasattr(pred, "item"):
            pred = pred.item()
        pred_int = int(pred)
        recommended_vessel = self.inverse_mapper.get(pred_int, "Panamax")

        # 5. SHAP Feature Explanation
        explanation = None
        if self.explainer:
            try:
                shap_res = self.explainer(df)
                class_shap_values = shap_res.values[0, :, pred_int]
                explanation = {
                    col: float(class_shap_values[i])
                    for i, col in enumerate(self.feature_columns)
                }
            except Exception as e:
                logger.warning(f"Error computing SHAP values: {e}")
                explanation = None

        # 6. Options Analysis for Compatibility
        options: List[VesselOption] = []
        for cls_name, specs in self.vessel_specs.items():
            feasible, failure_reasons = self.port_service.check_port_compatibility(
                vessel_specs=specs,
                port_name=dest_input,
                cargo_mt=request.consignment_size
            )
            dwt = specs["typical_dwt"]
            score = 0.0
            if not feasible:
                reason = "Port draft/LOA constraint. " + " ".join(failure_reasons)
            else:
                cap_ratio = request.consignment_size / dwt
                if 0.85 <= cap_ratio <= 1.10:
                    score = 94.0
                    reason = "Best balance of cargo capacity and voyage economics."
                elif 0.50 <= cap_ratio < 0.85:
                    score = 84.0
                    reason = "Operationally feasible."
                else:
                    score = 65.0
                    reason = "Suboptimal capacity utilization."

            options.append(VesselOption(
                vessel_class=cls_name,
                feasible=feasible,
                score=round(score, 1),
                reason=reason
            ))

        return VesselRecommendResponse(
            recommended_vessel=recommended_vessel,
            route=RouteInfo(
                origin_port=origin_input,
                destination_port=dest_input
            ),
            consignment_size=request.consignment_size,
            budget=request.budget,
            route_max_draft=route_max_draft,
            explanation=explanation,
            options=options
        )

