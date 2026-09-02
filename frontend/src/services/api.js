/**
 * Centralized API HTTP Service for CHARTER CAST
 * Communicates with the FastAPI backend at VITE_API_BASE_URL.
 */

const RAW_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '';
const BASE_URL = RAW_BASE_URL.replace(/\/+$/, '');

export async function request(endpoint, options = {}) {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${BASE_URL}${cleanEndpoint}`;
  
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...(options.headers || {}),
  };

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else if (Array.isArray(errorData.detail)) {
            errorMessage = errorData.detail.map(d => d.msg || JSON.stringify(d)).join('; ');
          }
        } else if (errorData.message) {
          errorMessage = errorData.message;
        }
      } catch {
        // Failed to parse JSON error response, use default message
      }
      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (err) {
    if (err.name === 'TypeError' || (err.message && err.message.toLowerCase().includes('fetch'))) {
      throw new Error('Unable to connect to the Charter Cast AI backend.');
    }
    throw err;
  }
}

export async function checkBackendHealth() {
  try {
    const data = await request('/api/health');
    return { online: Boolean(data), data };
  } catch (err) {
    return { online: false, error: err.message };
  }
}
