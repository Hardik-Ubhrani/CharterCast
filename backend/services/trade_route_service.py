import os
import joblib
import networkx as nx
from typing import Optional, Dict, Any, List
from backend.models.schemas import TradeRouteOptimizeRequest, TradeRouteOptimizeResponse


class TradeRouteService:
    def __init__(self, pkl_path: Optional[str] = None):
        if pkl_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pkl_path = os.path.join(base_dir, "ml", "weights", "trade_route_engine.pkl")

        if not os.path.exists(pkl_path):
            raise FileNotFoundError(f"Trade Route Engine configuration file not found at: {pkl_path}")

        engine_data = joblib.load(pkl_path)
        self.graph: nx.Graph = engine_data.get("graph")
        self.chokepoint_rules: Dict[str, Dict[str, bool]] = engine_data.get("chokepoint_rules", {})
        self.port_drafts: Dict[str, float] = engine_data.get("port_drafts", {})
        self.vessel_drafts: Dict[str, float] = engine_data.get("vessel_drafts", {})

    def _normalize_vessel_class(self, vessel_class: str) -> str:
        """
        Normalize input vessel class string to match dictionary keys.
        """
        if not vessel_class:
            return "Capesize"
        
        v_clean = vessel_class.strip()
        if v_clean in self.vessel_drafts:
            return v_clean
        
        # Alias mappings
        alias_map = {
            "supramax": "Handymax / Supramax",
            "handymax": "Handymax / Supramax",
            "handymax/supramax": "Handymax / Supramax",
            "handymax / supramax": "Handymax / Supramax",
            "handysize": "Handysize",
            "panamax": "Panamax",
            "capesize": "Capesize",
            "aframax": "Aframax",
            "suezmax": "Suezmax",
            "vlcc": "VLCC",
            "ulcc": "ULCC",
            "malaccamax": "Malaccamax",
            "seawaymax": "Seawaymax",
            "valemax": "Valemax",
            "new panamax": "New Panamax"
        }

        v_lower = v_clean.lower()
        if v_lower in alias_map:
            return alias_map[v_lower]

        # Partial matching
        for k in self.vessel_drafts.keys():
            if v_lower in k.lower() or k.lower() in v_lower:
                return k

        return v_clean

    def _normalize_node_name(self, name: str) -> Optional[str]:
        """
        Normalize port/region name to match graph nodes.
        """
        if not name:
            return None
        
        clean_name = name.strip()
        nodes = list(self.graph.nodes())
        
        if clean_name in nodes:
            return clean_name
        
        # Direct alias map for common dropdown options
        alias_map = {
            "paradip port": "Paradip",
            "visakhapatnam (vizag) port": "Visakhapatnam",
            "dhamra port": "Dhamra",
            "haldia dock complex (smp kolkata)": "Haldia",
            "gangavaram port": "Gangavaram",
            "australia (bulk region)": "Australia",
            "indonesia (coal hub)": "Indonesia",
            "south africa (richards bay)": "South Africa"
        }
        
        clean_lower = clean_name.lower()
        if clean_lower in alias_map:
            return alias_map[clean_lower]
        
        # Partial match
        for node in nodes:
            if clean_lower in node.lower() or node.lower() in clean_lower:
                return node
                
        return clean_name

    def _get_port_draft(self, port_name: str) -> Optional[float]:
        """
        Lookup max draft for a port from port_drafts dictionary.
        """
        if not port_name:
            return None
        
        clean_name = port_name.strip()
        if clean_name in self.port_drafts:
            return self.port_drafts[clean_name]
        
        # Normalized lookup
        norm_name = self._normalize_node_name(clean_name)
        if norm_name and norm_name in self.port_drafts:
            return self.port_drafts[norm_name]
        
        clean_lower = clean_name.lower()
        for p, d in self.port_drafts.items():
            if clean_lower in p.lower() or p.lower() in clean_lower:
                return d
                
        return None

    def optimize_route(self, request: TradeRouteOptimizeRequest) -> TradeRouteOptimizeResponse:
        vessel_class_norm = self._normalize_vessel_class(request.vessel_class)
        v_draft = self.vessel_drafts.get(vessel_class_norm, 15.0)

        # 1. Draft Checks
        dest_draft = self._get_port_draft(request.destination)
        if dest_draft is not None and v_draft > dest_draft:
            return TradeRouteOptimizeResponse(
                origin=request.origin,
                destination=request.destination,
                vessel_class=request.vessel_class,
                recommended_route=[],
                distance_nm=None,
                route_feasible=False,
                reason=f"Vessel draft ({v_draft}m for {vessel_class_norm}) exceeds destination port draft ({dest_draft}m for {request.destination}).",
                engine_name="Constraint-Aware A* Route Engine"
            )

        orig_draft = self._get_port_draft(request.origin)
        if orig_draft is not None and v_draft > orig_draft:
            return TradeRouteOptimizeResponse(
                origin=request.origin,
                destination=request.destination,
                vessel_class=request.vessel_class,
                recommended_route=[],
                distance_nm=None,
                route_feasible=False,
                reason=f"Vessel draft ({v_draft}m for {vessel_class_norm}) exceeds origin port draft ({orig_draft}m for {request.origin}).",
                engine_name="Constraint-Aware A* Route Engine"
            )

        # 2. Graph Node Resolution
        orig_node = self._normalize_node_name(request.origin)
        dest_node = self._normalize_node_name(request.destination)

        # 3. Chokepoint Constraints & Subgraph Construction
        v_chokepoints = self.chokepoint_rules.get(vessel_class_norm, {})
        forbidden_nodes = [
            node for node in self.graph.nodes()
            if node in v_chokepoints and not v_chokepoints[node]
        ]

        subgraph = self.graph.copy()
        subgraph.remove_nodes_from(forbidden_nodes)

        if orig_node not in subgraph:
            return TradeRouteOptimizeResponse(
                origin=request.origin,
                destination=request.destination,
                vessel_class=request.vessel_class,
                recommended_route=[],
                distance_nm=None,
                route_feasible=False,
                reason=f"Origin '{request.origin}' is not reachable in maritime network graph.",
                engine_name="Constraint-Aware A* Route Engine"
            )

        if dest_node not in subgraph:
            return TradeRouteOptimizeResponse(
                origin=request.origin,
                destination=request.destination,
                vessel_class=request.vessel_class,
                recommended_route=[],
                distance_nm=None,
                route_feasible=False,
                reason=f"Destination '{request.destination}' is not reachable in maritime network graph.",
                engine_name="Constraint-Aware A* Route Engine"
            )

        # 4. NetworkX A* Search
        try:
            path = nx.astar_path(subgraph, orig_node, dest_node, weight="weight")
            distance = nx.astar_path_length(subgraph, orig_node, dest_node, weight="weight")

            return TradeRouteOptimizeResponse(
                origin=request.origin,
                destination=request.destination,
                vessel_class=request.vessel_class,
                recommended_route=path,
                distance_nm=float(distance),
                route_feasible=True,
                reason=None,
                engine_name="Constraint-Aware A* Route Engine"
            )
        except nx.NetworkXNoPath:
            return TradeRouteOptimizeResponse(
                origin=request.origin,
                destination=request.destination,
                vessel_class=request.vessel_class,
                recommended_route=[],
                distance_nm=None,
                route_feasible=False,
                reason=f"No feasible maritime route found from {request.origin} to {request.destination} for vessel class {request.vessel_class} due to chokepoint/navigation constraints.",
                engine_name="Constraint-Aware A* Route Engine"
            )
