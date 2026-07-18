// API base URL for backend requests.
// In production, Railway injects REACT_APP_API_URL with the backend's public domain.
// Falls back to localhost for local development.

const apiUrl = import.meta.env.REACT_APP_API_URL || 'localhost:8000'

// Ensure the URL has the protocol
let API_BASE_URL = apiUrl
if (!API_BASE_URL.startsWith('http://') && !API_BASE_URL.startsWith('https://')) {
  // It's likely just a domain name from Railway, add https://
  API_BASE_URL = `https://${API_BASE_URL}`
}

// Remove trailing slashes
API_BASE_URL = API_BASE_URL.replace(/\/$/, '')

export { API_BASE_URL }

