import { Link } from 'react-router-dom';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { MapContainer, Marker, Popup, TileLayer, useMap, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { getLocations } from '../api';

const DEFAULT_CENTER = [31.8, 35.2];
const DEFAULT_ZOOM = 6;
const TESTAMENT_OPTIONS = ['All', 'Old Testament', 'New Testament'];

const LOCATION_COORDINATES = {
  Babylon: { latitude: 32.54, longitude: 44.42, region: 'Mesopotamia', certainty_level: 'probable' },
  Bethlehem: { latitude: 31.7054, longitude: 35.2024, region: 'Judea', certainty_level: 'high' },
  Egypt: { latitude: 30.0444, longitude: 31.2357, region: 'North Africa', certainty_level: 'probable' },
  Galilee: { latitude: 32.8, longitude: 35.5, region: 'Northern Israel', certainty_level: 'probable' },
  'Jordan River': { latitude: 31.82, longitude: 35.55, region: 'Jordan Valley', certainty_level: 'probable' },
  Jericho: { latitude: 31.8667, longitude: 35.45, region: 'Jordan Valley', certainty_level: 'high' },
  Jerusalem: { latitude: 31.7767, longitude: 35.2345, region: 'Judea', certainty_level: 'high' },
  'Mount Carmel': { latitude: 32.66, longitude: 35.04, region: 'Northern Israel', certainty_level: 'probable' },
  'Mount Sinai': { latitude: 28.5392, longitude: 33.975, region: 'Sinai Peninsula', certainty_level: 'traditional' },
  Nazareth: { latitude: 32.7, longitude: 35.303, region: 'Galilee', certainty_level: 'high' },
  Nineveh: { latitude: 36.36, longitude: 43.15, region: 'Assyria', certainty_level: 'probable' },
};


const markerIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

function MapViewportWatcher({ onBoundsChange }) {
  const map = useMapEvents({
    moveend: () => onBoundsChange(map.getBounds()),
    zoomend: () => onBoundsChange(map.getBounds()),
  });

  useEffect(() => {
    onBoundsChange(map.getBounds());
  }, [map, onBoundsChange]);

  return null;
}

function FocusMapOnLocation({ location }) {
  const map = useMap();

  useEffect(() => {
    if (!location) return;
    map.flyTo([location.latitude, location.longitude], Math.max(map.getZoom(), 8), {
      duration: 0.6,
    });
  }, [location, map]);

  return null;
}

function normalizeTestamentName(value) {
  if (!value) return null;
  const normalized = value.toLowerCase();
  if (normalized.startsWith('old')) return 'Old Testament';
  if (normalized.startsWith('new')) return 'New Testament';
  return null;
}

function toTestamentLabel(location) {
  const stories = location.relationships?.stories || [];
  const hasOld = stories.some((story) => normalizeTestamentName(story.testament) === 'Old Testament');
  const hasNew = stories.some((story) => normalizeTestamentName(story.testament) === 'New Testament');

  if (hasOld && hasNew) return 'Both';
  if (hasOld) return 'Old Testament';
  if (hasNew) return 'New Testament';
  return 'Unknown';
}

export default function LocationsMapPage() {
  const [locations, setLocations] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');
  const [testamentFilter, setTestamentFilter] = useState('All');
  const [focusedLocationId, setFocusedLocationId] = useState(null);
  const [mapBounds, setMapBounds] = useState(null);

  useEffect(() => {
    setStatus('loading');
    setError('');

    getLocations()
      .then((data) => {
        setLocations(Array.isArray(data?.items) ? data.items : []);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load locations');
        setStatus('error');
      });
  }, []);

  const mapLocations = useMemo(
    () =>
      locations
        .map((location) => ({
          ...location,
          ...LOCATION_COORDINATES[location.name],
        }))
        .filter((location) => Number.isFinite(location.latitude) && Number.isFinite(location.longitude)),
    [locations],
  );

  const filteredMapLocations = useMemo(() => {
    if (testamentFilter === 'All') {
      return mapLocations;
    }

    return mapLocations.filter((location) => {
      const stories = location.relationships?.stories || [];
      return stories.some((story) => normalizeTestamentName(story.testament) === testamentFilter);
    });
  }, [mapLocations, testamentFilter]);

  const visibleLocations = useMemo(() => {
    if (!mapBounds) {
      return filteredMapLocations;
    }

    return filteredMapLocations.filter((location) => mapBounds.contains([location.latitude, location.longitude]));
  }, [filteredMapLocations, mapBounds]);

  const focusedLocation = useMemo(
    () => filteredMapLocations.find((location) => location.id === focusedLocationId) || null,
    [filteredMapLocations, focusedLocationId],
  );

  useEffect(() => {
    if (focusedLocationId && !filteredMapLocations.some((location) => location.id === focusedLocationId)) {
      setFocusedLocationId(null);
    }
  }, [filteredMapLocations, focusedLocationId]);

  const handleBoundsChange = useCallback((bounds) => {
    setMapBounds(bounds);
  }, []);

  if (status === 'loading') return <p className="text-slate-600">Loading map-ready locations...</p>;
  if (status === 'error') return <p className="rounded-md bg-red-50 p-4 text-red-700">{error}</p>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Locations map</h1>
        <p className="mt-2 text-slate-600">
          Explore biblical places with map markers, contextual details, and a side list of locations currently visible on screen.
        </p>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold">Interactive map</h2>
            <p className="text-sm text-slate-600">
              Showing {visibleLocations.length} visible of {filteredMapLocations.length} mapped locations.
            </p>
          </div>
          <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
            Testament
            <select
              value={testamentFilter}
              onChange={(event) => setTestamentFilter(event.target.value)}
              className="rounded-md border border-slate-300 px-2 py-1.5 text-sm"
            >
              {TESTAMENT_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="mt-4 grid gap-4 lg:grid-cols-[2fr,1fr]">
          <div className="overflow-hidden rounded-md border border-slate-200">
            <MapContainer center={DEFAULT_CENTER} zoom={DEFAULT_ZOOM} className="h-[540px] w-full" scrollWheelZoom>
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <MapViewportWatcher onBoundsChange={handleBoundsChange} />
              <FocusMapOnLocation location={focusedLocation} />

              {filteredMapLocations.map((location) => (
                <Marker key={location.id} position={[location.latitude, location.longitude]} icon={markerIcon}>
                  <Popup>
                    <div className="min-w-[220px] space-y-2 text-sm">
                      <div>
                        <p className="text-base font-semibold text-slate-900">{location.name}</p>
                        <p className="text-xs text-slate-500">{location.region || 'Unknown region'}</p>
                      </div>
                      <p className="text-slate-700">{location.description || 'No description available.'}</p>
                      <div className="space-y-1 rounded-md bg-slate-50 p-2 text-xs text-slate-600">
                        <p>Certainty: {location.certainty_level || 'unknown'}</p>
                        <p>Tradition: {toTestamentLabel(location)}</p>
                        <p>
                          Coordinates: {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
                        </p>
                      </div>
                      <Link to={`/locations/${location.id}`} className="inline-block font-medium text-indigo-600 hover:underline">
                        Open location details →
                      </Link>
                    </div>
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>

          <aside className="rounded-md border border-slate-200 bg-slate-50 p-3">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-700">Visible locations</h3>
            <p className="mt-1 text-xs text-slate-600">Pan or zoom the map to update this list.</p>
            <ul className="mt-3 max-h-[470px] space-y-2 overflow-y-auto pr-1">
              {visibleLocations.map((location) => (
                <li key={location.id}>
                  <button
                    type="button"
                    onClick={() => setFocusedLocationId(location.id)}
                    className="w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-left text-sm transition hover:border-indigo-300 hover:bg-indigo-50"
                  >
                    <p className="font-medium text-slate-900">{location.name}</p>
                    <p className="text-xs text-slate-600">
                      {location.region || 'Unknown region'} · {toTestamentLabel(location)}
                    </p>
                  </button>
                </li>
              ))}
              {visibleLocations.length === 0 ? (
                <li className="rounded-md border border-dashed border-slate-300 bg-white px-3 py-4 text-center text-xs text-slate-500">
                  No locations visible in this viewport.
                </li>
              ) : null}
            </ul>
          </aside>
        </div>
      </section>
    </div>
  );
}
