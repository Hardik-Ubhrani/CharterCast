import { request } from './api';

/**
 * Recommends optimal vessel class using trained XGBoost ML model.
 * Frontend Adapter: Automatically supplies required backend default budget parameter (150,000 USD).
 * User input only requires Cargo Quantity, Origin Port, Destination Port.
 */
export async function recommendVessel({ cargoQuantityMt, originPort, destinationPort }) {
  if (!cargoQuantityMt || Number(cargoQuantityMt) <= 0) {
    throw new Error('Please enter a valid positive cargo quantity in MT.');
  }
  if (!originPort || !originPort.trim()) {
    throw new Error('Please select an origin port.');
  }
  if (!destinationPort || !destinationPort.trim()) {
    throw new Error('Please select a destination port.');
  }

  const payload = {
    origin_port: originPort.trim(),
    destination_port: destinationPort.trim(),
    consignment_size: Number(cargoQuantityMt),
    budget: 150000.0 // Adapter default value required by backend schema contract
  };

  return await request('/api/vessel/recommend', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}
