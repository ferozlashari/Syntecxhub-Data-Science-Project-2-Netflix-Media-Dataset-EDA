// Thin fetch wrapper for the FastAPI backend.
// In dev, Vite proxies /api and /static to http://127.0.0.1:8000 (see vite.config.js).
// In production, set VITE_API_BASE_URL to the deployed backend's origin.

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

async function getJSON(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`Request to ${path} failed with status ${res.status}`);
  }
  return res.json();
}

export function fetchNetflixAnalysis() {
  return getJSON("/api/netflix/analysis");
}

export function refreshNetflixAnalysis() {
  return getJSON("/api/netflix/analysis/refresh");
}

export function chartUrl(filename) {
  return `${API_BASE}/static/charts/netflix/${filename}`;
}
