function inferDefaultApiBaseUrl() {
  if (typeof window === 'undefined' || !window.location) {
    return 'http://127.0.0.1:8000';
  }

  const { protocol, hostname } = window.location;

  if (hostname.endsWith('.app.github.dev')) {
    const codespacesHost = hostname.replace(/-\d+\.app\.github\.dev$/, '-8000.app.github.dev');
    return `${protocol}//${codespacesHost}`;
  }

  return 'http://127.0.0.1:8000';
}

const RAW_API_BASE_URL = import.meta.env.VITE_API_BASE_URL || inferDefaultApiBaseUrl();
const API_BASE_URL = RAW_API_BASE_URL.replace(/\/+$/, '');
const REQUEST_TIMEOUT_MS = 10000;

class ApiError extends Error {
  constructor(message, status = null, payload = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.payload = payload;
  }
}

function toQueryString(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      query.set(key, String(value));
    }
  });
  const encoded = query.toString();
  return encoded ? `?${encoded}` : '';
}

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') || '';
  const isJson = contentType.includes('application/json');

  if (!isJson) {
    return null;
  }

  try {
    return await response.json();
  } catch {
    return null;
  }
}

async function request(path, options = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      signal: controller.signal,
    });

    const payload = await parseResponse(response);

    if (!response.ok) {
      const detail = payload?.detail;
      const message = typeof detail === 'string' ? detail : `Request failed with status ${response.status}`;
      throw new ApiError(message, response.status, payload);
    }

    if (!payload) {
      throw new ApiError('API returned a non-JSON response.', response.status);
    }

    return payload;
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new ApiError(`Request timed out after ${REQUEST_TIMEOUT_MS / 1000} seconds. API URL: ${API_BASE_URL}`);
    }

    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(
      `Network error while calling ${API_BASE_URL}${path}. Verify backend is running, CORS is enabled, and VITE_API_BASE_URL is correct.`,
    );
  } finally {
    clearTimeout(timeoutId);
  }
}

export function getStories(params = {}) {
  return request(`/stories${toQueryString(params)}`);
}

export function getStoryById(storyId) {
  return request(`/stories/${storyId}`);
}

export function getCharacters(params = {}) {
  return request(`/characters${toQueryString(params)}`);
}

export function getCharacterById(characterId) {
  return request(`/characters/${characterId}`);
}

export function getLocations(params = {}) {
  return request(`/locations${toQueryString(params)}`);
}

export function getLocationById(locationId) {
  return request(`/locations/${locationId}`);
}

export function getArtworks(params = {}) {
  return request(`/artworks${toQueryString(params)}`);
}

export function getArtworkById(artworkId) {
  return request(`/artworks/${artworkId}`);
}

export { API_BASE_URL, ApiError };
