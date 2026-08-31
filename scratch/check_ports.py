import pickle
import sys
from backend.services.port_service import PortService

ps = PortService()

with open('backend/ml/portwise_vessel_model.pkl', 'rb') as f:
    bundle = pickle.load(f)

origin_cats = list(bundle['origin_categories'])
dest_cats = list(bundle['destination_categories'])

print("PortService ports count:", len(ps.ports))
print("Sample PortService port keys:", list(ps.ports.keys())[:10])

print("\nChecking origin categories against PortService:")
for p in origin_cats:
    info = ps.get_port_info(p)
    exact_in = p in ps.ports or any(k.lower() == p.lower() for k in ps.ports.keys())
    print(f"Origin '{p}': draft={info.get('max_draft_m')}, exact_match={exact_in}")

print("\nChecking sample destination categories against PortService:")
for p in dest_cats[:10]:
    info = ps.get_port_info(p)
    exact_in = p in ps.ports or any(k.lower() == p.lower() for k in ps.ports.keys())
    print(f"Dest '{p}': draft={info.get('max_draft_m')}, exact_match={exact_in}")

# Check specific test cases: "Paradip Port", "Maurer", "Visakhapatnam (Vizag) Port", "Iharana"
print("\nChecking test case ports:")
for p in ["Paradip Port", "Maurer", "Visakhapatnam (Vizag) Port", "Iharana", "Paradip", "Visakhapatnam"]:
    info = ps.get_port_info(p)
    print(f"Port '{p}': info={info}")
