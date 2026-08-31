import pickle
import pandas as pd
import numpy as np
import shap

with open('backend/ml/portwise_vessel_model.pkl', 'rb') as f:
    bundle = pickle.load(f)

model = bundle['model']
target_mapper = bundle['target_mapper']
inverse_mapper = bundle['inverse_mapper']
origin_categories = list(bundle['origin_categories'])
destination_categories = list(bundle['destination_categories'])
feature_columns = bundle['feature_columns']

explainer = shap.TreeExplainer(model)

def get_recommendation(origin_port, destination_port, consignment_size, budget, route_max_draft):
    df = pd.DataFrame([{
        "origin_port": origin_port,
        "destination_port": destination_port,
        "consignment_size": float(consignment_size),
        "budget": float(budget),
        "route_max_draft": float(route_max_draft)
    }])
    
    df["origin_port"] = pd.Categorical(df["origin_port"], categories=origin_categories)
    df["destination_port"] = pd.Categorical(df["destination_port"], categories=destination_categories)
    df = df[feature_columns]
    
    pred_int = int(model.predict(df)[0])
    vessel_name = inverse_mapper[pred_int]
    
    # Calculate SHAP values
    shap_res = explainer(df)
    class_shap_values = shap_res.values[0, :, pred_int]
    
    explanation = {
        col: float(class_shap_values[i])
        for i, col in enumerate(feature_columns)
    }
    
    return {
        "recommended_vessel": vessel_name,
        "explanation": explanation
    }

print("Case 1 SHAP extraction:")
print(get_recommendation("Paradip Port", "Maurer", 50000, 150000, 11.0))

print("\nCase 2 SHAP extraction:")
print(get_recommendation("Visakhapatnam (Vizag) Port", "Iharana", 140000, 220000, 14.0))
