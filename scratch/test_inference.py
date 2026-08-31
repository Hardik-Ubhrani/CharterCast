import pickle
import pandas as pd
import numpy as np
import traceback

with open('backend/ml/portwise_vessel_model.pkl', 'rb') as f:
    bundle = pickle.load(f)

model = bundle['model']
target_mapper = bundle['target_mapper']
inverse_mapper = bundle['inverse_mapper']
origin_categories = list(bundle['origin_categories'])
destination_categories = list(bundle['destination_categories'])
feature_columns = bundle['feature_columns']

print("Origin categories count:", len(origin_categories))
print("Destination categories count:", len(destination_categories))
print("Destination categories sample:", destination_categories[:10])

# Check if Maurer and Iharana are in destination_categories
print("'Maurer' in destination_categories?", "Maurer" in destination_categories)
print("'Iharana' in destination_categories?", "Iharana" in destination_categories)
print("'Paradip Port' in origin_categories?", "Paradip Port" in origin_categories)
print("'Visakhapatnam (Vizag) Port' in origin_categories?", "Visakhapatnam (Vizag) Port" in origin_categories)

# Let's inspect how pandas categorical features were constructed during training.
# Model params has enable_categorical=True.
# When enable_categorical=True in XGBoost with pandas DataFrame, categorical columns must be of dtype 'category'.
# Specifically: pd.Categorical([val], categories=categories)

def predict_case(origin, destination, consignment_size, budget, route_max_draft):
    df = pd.DataFrame([{
        "origin_port": pd.Categorical([origin], categories=origin_categories)[0],
        "destination_port": pd.Categorical([destination], categories=destination_categories)[0],
        "consignment_size": float(consignment_size),
        "budget": float(budget),
        "route_max_draft": float(route_max_draft)
    }])
    df = df[feature_columns]
    
    # Ensure dtypes: origin_port & destination_port category, numeric as float
    df['origin_port'] = pd.Categorical(df['origin_port'], categories=origin_categories)
    df['destination_port'] = pd.Categorical(df['destination_port'], categories=destination_categories)
    
    pred_int = model.predict(df)[0]
    # Handle scalar or array return from predict
    if hasattr(pred_int, 'item'):
        pred_int = pred_int.item()
    pred_name = inverse_mapper[pred_int]
    print(f"Prediction for ({origin}, {destination}, {consignment_size}, {budget}, {route_max_draft}): {pred_int} -> {pred_name}")
    
    # Test SHAP
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(df)
        print("SHAP values shape/type:", type(shap_values), shap_values.shape)
        # Check SHAP feature contribution extraction
        print("SHAP values sample:", shap_values.values)
    except Exception as e:
        print("SHAP error:")
        traceback.print_exc()

print("\n--- CASE 1 ---")
# Paradip Port draft = 14.5, Maurer draft = ? Let's check or test with 11.0 draft as stated in prompt
predict_case("Paradip Port", "Maurer", 50000, 150000, 11.0)

print("\n--- CASE 2 ---")
predict_case("Visakhapatnam (Vizag) Port", "Iharana", 140000, 220000, 14.0)
