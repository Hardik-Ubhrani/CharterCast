import { request } from './api';

/**
 * Service abstraction for Trade Route Optimization model.
 * Connects to backend /api/trade-route/optimize endpoint using centralized request service.
 */
export async function optimizeTradeRoute(params = {}) {
  const { origin, destination, commodity, vesselClass, vessel_class, cargoQuantity, cargo_quantity } = params;

  const payload = {
    origin: (origin || 'Australia').trim(),
    destination: (destination || 'Dhamra').trim(),
    commodity: commodity || 'Coking Coal',
    vessel_class: vessel_class || vesselClass || 'Capesize',
  };

  if (cargo_quantity || cargoQuantity) {
    payload.cargo_quantity = Number(cargo_quantity || cargoQuantity);
  }

  const data = await request('/api/trade-route/optimize', {
    method: 'POST',
    body: JSON.stringify(payload)
  });

  return {
    pending: false,
    data
  };
}

export async function recommendTradeRoute(params = {}) {
  try {
    return await optimizeTradeRoute(params);
  } catch (err) {
    return {
      pending: false,
      error: err.message || 'Trade route optimization error.',
      data: null
    };
  }
}


