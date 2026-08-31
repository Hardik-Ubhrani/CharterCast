# PORTWISE AI — ML Model Integration Guide

This directory manages the machine learning model abstraction layer for **PORTWISE AI**.

## Architecture Overview

All forecasting models extend the `ForecastModel` interface defined in [`model_interface.py`](file:///c:/Users/Meet%20Jeswani/OneDrive/Desktop/portwise/backend/ml/model_interface.py).

```text
               ForecastModel (Abstract Class)
                             │
     ┌───────────────────────┼───────────────────────┐
     ↓                       ↓                       ↓
MockForecaster         TFTForecaster         PatchTSTForecaster
(Development)         (PyTorch TFT)         (PyTorch PatchTST)
```

## How to Plug in Trained ML Models

### 1. Place Model Weights
Drop your trained model checkpoint into `backend/ml/weights/`:
- `backend/ml/weights/tft_model.pt`
- `backend/ml/weights/patchtst_model.pt`

### 2. Implement Inference Logic
Open [`tft_forecaster.py`](file:///c:/Users/Meet%20Jeswani/OneDrive/Desktop/portwise/backend/ml/tft_forecaster.py) or [`patchtst_forecaster.py`](file:///c:/Users/Meet%20Jeswani/OneDrive/Desktop/portwise/backend/ml/patchtst_forecaster.py) and update the `predict()` method to load your PyTorch tensor / model instance and convert the input dataframe into `ForecastPoint` predictions.

### 3. Verification
Call `POST /api/forecast` with `"model": "tft"` or `"model": "patchtst"`.
The backend will automatically detect the weights, run your model inference, and return standard JSON outputs to the frontend without any contract changes!
