import logging
import os
import pandas as pd
from typing import Dict, Any, Tuple
from backend.utils.constants import PORT_CONSTRAINTS

logger = logging.getLogger(__name__)


def check_draft(vessel_draft: float, port_max_draft: float) -> Tuple[bool, str]:
    """Check draft constraint: Vessel draft cannot exceed port maximum draft."""
    if vessel_draft > port_max_draft:
        return False, f"Vessel draft ({vessel_draft}m) exceeds port maximum draft ({port_max_draft}m)."
    return True, "Draft within safe operating limit."


def check_loa(vessel_loa: float, port_max_loa: float) -> Tuple[bool, str]:
    """Check Length Overall (LOA) constraint."""
    if vessel_loa > port_max_loa:
        return False, f"Vessel LOA ({vessel_loa}m) exceeds port maximum length ({port_max_loa}m)."
    return True, "LOA compatible with port berth length."


def check_beam(vessel_beam: float, port_max_beam: float) -> Tuple[bool, str]:
    """Check vessel beam constraint."""
    if vessel_beam > port_max_beam:
        return False, f"Vessel beam ({vessel_beam}m) exceeds port maximum channel/berth width ({port_max_beam}m)."
    return True, "Beam compatible with port infrastructure."


def check_cargo_capacity(cargo_mt: float, vessel_dwt: float) -> Tuple[bool, str]:
    """Check whether vessel deadweight tonnage is compatible with cargo size."""
    if vessel_dwt < cargo_mt * 0.8:
        return False, f"Vessel capacity (DWT {vessel_dwt}t) insufficient for total cargo ({cargo_mt} MT)."
    return True, "Cargo quantity fits vessel deadweight capacity."


class PortService:
    """
    Port Feasibility Engine for evaluating physical port infrastructure limits.
    Loads port data from updatedpub150.csv if present, or falls back to PORT_CONSTRAINTS.
    """

    def __init__(self, data_path: str = "backend/data/updatedpub150.csv"):
        self.ports = PORT_CONSTRAINTS.copy()
        self._load_dataset(data_path)

    def _load_dataset(self, data_path: str):
        # 1. Load East Coast master CSV if available
        master_path = "backend/data/indian_east_coast_ports_master.csv"
        if os.path.exists(master_path):
            try:
                df_m = pd.read_csv(master_path)
                for _, row in df_m.iterrows():
                    p_name = str(row.get("port_name", "")).strip()
                    if p_name and p_name not in self.ports:
                        self.ports[p_name] = {
                            "name": p_name,
                            "max_draft_m": float(row.get("max_permissible_draft_m", 14.5)),
                            "max_loa_m": float(row.get("max_loa_m", 260.0)),
                            "max_beam_m": float(row.get("max_beam_m", 43.0)),
                            "handling_rate_tpd": float(row.get("nominal_discharge_rate_tpd", 25000)),
                            "lat": 20.2644,
                            "lon": 86.6713
                        }
                logger.info(f"Loaded master port records from {master_path}")
            except Exception as e:
                logger.error(f"Error loading master port CSV {master_path}: {e}")

        # 2. Load Pub 150 CSV
        if os.path.exists(data_path):
            try:
                df = pd.read_csv(data_path)
                for _, row in df.iterrows():
                    p_name = str(row.get("port_name", "")).strip()
                    if p_name:
                        self.ports[p_name] = {
                            "name": p_name,
                            "max_draft_m": float(row.get("max_draft_m", 14.0)),
                            "max_loa_m": float(row.get("max_loa_m", 230.0)),
                            "max_beam_m": float(row.get("max_beam_m", 32.5)),
                            "handling_rate_tpd": float(row.get("handling_rate_tpd", 20000)),
                            "lat": float(row.get("latitude", 0.0)),
                            "lon": float(row.get("longitude", 0.0))
                        }
                logger.info(f"Loaded {len(df)} port records from {data_path}")
            except Exception as e:
                logger.error(f"Error loading port CSV {data_path}: {e}")

    def get_port_info(self, port_name: str) -> Dict[str, Any]:
        p_clean = port_name.strip().lower()
        # 1. Exact match (case-insensitive)
        for name, data in self.ports.items():
            if name.lower() == p_clean:
                return data
        # 2. Substring match
        for name, data in self.ports.items():
            if name.lower() in p_clean or p_clean in name.lower():
                return data
        # Default fallback (Paradip / standard East Coast port)
        return {
            "name": port_name,
            "max_draft_m": 14.5,
            "max_loa_m": 230.0,
            "max_beam_m": 33.0,
            "handling_rate_tpd": 25000,
            "lat": 20.2644,
            "lon": 86.6713
        }

    def check_port_compatibility(self, vessel_specs: Dict[str, Any], port_name: str, cargo_mt: float) -> Tuple[bool, list]:
        port_info = self.get_port_info(port_name)
        reasons = []
        is_feasible = True

        draft_ok, draft_msg = check_draft(vessel_specs["max_draft_m"], port_info["max_draft_m"])
        if not draft_ok:
            is_feasible = False
            reasons.append(draft_msg)

        loa_ok, loa_msg = check_loa(vessel_specs["max_loa_m"], port_info["max_loa_m"])
        if not loa_ok:
            is_feasible = False
            reasons.append(loa_msg)

        beam_ok, beam_msg = check_beam(vessel_specs["max_beam_m"], port_info["max_beam_m"])
        if not beam_ok:
            is_feasible = False
            reasons.append(beam_msg)

        cap_ok, cap_msg = check_cargo_capacity(cargo_mt, vessel_specs["typical_dwt"])
        if not cap_ok:
            # Capacity issue is an operational note rather than hard port prohibition if sub-shipment allowed,
            # but for single vessel recommendation it penalizes feasibility.
            reasons.append(cap_msg)

        return is_feasible, reasons
