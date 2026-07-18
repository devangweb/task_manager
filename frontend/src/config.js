// API base URL for backend requests.
// In production, Railway injects REACT_APP_API_URL (set to the backend's public domain).
// Falls back to localhost for local development.
export const API_BASE_URL = import.meta.env.REACT_APP_API_URL || 'http://localhost:8000'
