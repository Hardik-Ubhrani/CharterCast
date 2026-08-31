import pickle
import pandas as pd

with open('backend/ml/portwise_vessel_model.pkl', 'rb') as f:
    bundle = pickle.load(f)

model = bundle['model']
inverse_mapper = bundle['inverse_mapper']
origin_categories = list(bundle['origin_categories'])
destination_categories = list(bundle['destination_categories'])
feature_columns = bundle['feature_columns']

def test_pred(origin, dest, cargo, budget, draft):
    df = pd.DataFrame([{
        "origin_port": origin,
        "destination_port": dest,
        "consignment_size": float(cargo),
        "budget": float(budget),
        "route_max_draft": float(draft)
    }])
    df["origin_port"] = pd.Categorical(df["origin_port"], categories=origin_categories)
    df["destination_port"] = pd.Categorical(df["destination_port"], categories=destination_categories)
    df = df[feature_columns]
    pred_int = int(model.predict(df)[0])
    return inverse_mapper[pred_int]

print("Case 1 with draft 14.5:", test_pred("Paradip Port", "Maurer", 50000, 150000, 14.5))
print("Case 1 with draft 11.0:", test_pred("Paradip Port", "Maurer", 50000, 150000, 11.0))

print("Case 2 with draft 14.0:", test_pred("Visakhapatnam (Vizag) Port", "Iharana", 140000, 220000, 14.0))
print("Case 2 with draft 14.5:", test_pred("Visakhapatnam (Vizag) Port", "Iharana", 140000, 220000, 14.5))
