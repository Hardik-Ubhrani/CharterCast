import os
import pickle
import logging
import pandas as pd
import numpy as np
import shap
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

MODEL_PATH = "backend/ml/portwise_vessel_model.pkl"

class VesselService:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.target_mapper = None
        self.inverse_mapper = None
        self.origin_categories = None
        self.destination_categories = None
        self.feature_columns = None
        self.explainer = None
        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            logger.error(f"Model file not found at {self.model_path}")
            raise RuntimeError(f"Vessel model pickle not found at {self.model_path}")
        try:
            with open(self.model_path, "rb") as f:
                bundle = pickle.load(f)
            self.model = bundle["model"]
            self.target_mapper = bundle["target_mapper"]
            self.inverse_mapper = bundle["inverse_mapper"]
            self.origin_categories = list(bundle["origin_categories"])
            self.destination_categories = list(bundle["destination_categories"])
            self.feature_columns = bundle["feature_columns"]
            
            # Known destination set for fast lookup
            self.known_destinations = set(self.destination_categories).union({"Maurer", "Iharana"})
            
            # Initialize SHAP explainer
            try:
                self.explainer = shap.TreeExplainer(self.model)
            except Exception as e:
                logger.warning(f"Failed to initialize SHAP explainer: {e}")
                self.explainer = None
        except Exception as e:
            logger.error(f"Error loading model bundle from {self.model_path}: {e}")
            raise RuntimeError(f"Model loading error: {str(e)}")

    def normalize_origin_port(self, port_name: str) -> str:
        if not port_name or not isinstance(port_name, str):
            return None
        p = port_name.strip()
        if p in self.origin_categories:
            return p
        for cat in self.origin_categories:
            if p.lower() in cat.lower() or cat.lower() in p.lower():
                return cat
        return None

    def normalize_dest_port(self, port_name: str) -> str:
        if not port_name or not isinstance(port_name, str):
            return None
        p = port_name.strip()
        if p in self.known_destinations:
            return p
        for cat in self.known_destinations:
            if p.lower() in cat.lower() or cat.lower() in p.lower():
                return cat
        return None

service = VesselService()
print("VesselService initialized successfully!")
print("Origin categories count:", len(service.origin_categories))
print("Destination categories count:", len(service.destination_categories))
