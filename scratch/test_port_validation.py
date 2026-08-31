import pickle
import pandas as pd
from backend.services.port_service import PortService

with open('backend/ml/portwise_vessel_model.pkl', 'rb') as f:
    bundle = pickle.load(f)

origin_cats = list(bundle['origin_categories'])
dest_cats = list(bundle['destination_categories'])

# Known ports set for prototype validation
KNOWN_DESTINATIONS = set(dest_cats).union({"Maurer", "Iharana"})

ps = PortService()

def normalize_origin_port(port_name: str) -> str:
    if not port_name or not isinstance(port_name, str):
        return None
    p_clean = port_name.strip()
    # Check exact match
    if p_clean in origin_cats:
        return p_clean
    # Check case-insensitive / substring match
    for cat in origin_cats:
        if p_clean.lower() in cat.lower() or cat.lower() in p_clean.lower():
            return cat
    # Check PortService
    if p_clean in ps.ports or any(p_clean.lower() in k.lower() for k in ps.ports.keys()):
        return p_clean
    return None

def normalize_dest_port(port_name: str) -> str:
    if not port_name or not isinstance(port_name, str):
        return None
    p_clean = port_name.strip()
    if p_clean in KNOWN_DESTINATIONS:
        return p_clean
    for cat in KNOWN_DESTINATIONS:
        if p_clean.lower() in cat.lower() or cat.lower() in p_clean.lower():
            return cat
    if p_clean in ps.ports or any(p_clean.lower() in k.lower() for k in ps.ports.keys()):
        return p_clean
    return None

print("Paradip Port origin match:", normalize_origin_port("Paradip Port"))
print("Paradip origin match:", normalize_origin_port("Paradip"))
print("Unknown origin match:", normalize_origin_port("UnknownOrigin123"))

print("Maurer dest match:", normalize_dest_port("Maurer"))
print("Iharana dest match:", normalize_dest_port("Iharana"))
print("Diego Garcia dest match:", normalize_dest_port("Diego Garcia"))
print("Unknown dest match:", normalize_dest_port("UnknownDest123"))
