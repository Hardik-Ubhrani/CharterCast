import json
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

print("=== LIVE API VERIFICATION ===")

print("\n--- TEST CASE 1 ---")
case1_payload = {
    "origin_port": "Paradip Port",
    "destination_port": "Maurer",
    "consignment_size": 50000,
    "budget": 150000
}
res1 = client.post("/api/vessel/recommend", json=case1_payload)
print("Status Code:", res1.status_code)
print("Response JSON:")
print(json.dumps(res1.json(), indent=2))

print("\n--- TEST CASE 2 ---")
case2_payload = {
    "origin_port": "Visakhapatnam (Vizag) Port",
    "destination_port": "Iharana",
    "consignment_size": 140000,
    "budget": 220000
}
res2 = client.post("/api/vessel/recommend", json=case2_payload)
print("Status Code:", res2.status_code)
print("Response JSON:")
print(json.dumps(res2.json(), indent=2))

print("\n--- TEST UNKNOWN ORIGIN PORT ---")
res3 = client.post("/api/vessel/recommend", json={
    "origin_port": "InvalidPort999",
    "destination_port": "Maurer",
    "consignment_size": 50000,
    "budget": 150000
})
print("Status Code:", res3.status_code)
print("Response JSON:", res3.json())

print("\n--- TEST UNKNOWN DESTINATION PORT ---")
res4 = client.post("/api/vessel/recommend", json={
    "origin_port": "Paradip Port",
    "destination_port": "InvalidPort999",
    "consignment_size": 50000,
    "budget": 150000
})
print("Status Code:", res4.status_code)
print("Response JSON:", res4.json())
