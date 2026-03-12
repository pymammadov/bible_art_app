import { Link } from 'react-router-dom';
import { useEffect, useMemo, useState } from 'react';
import { getLocations } from '../api';

export default function LocationsMapPage() {
  const [locations, setLocations] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

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

  const [withCoordinates, withoutCoordinates] = useMemo(() => {
    const withCoords = [];
    const withoutCoords = [];
    locations.forEach((location) => {
      const hasCoords = location.latitude !== null && location.longitude !== null;
      if (hasCoords) {
        withCoords.push(location);
      } else {
        withoutCoords.push(location);
      }
    });
    return [withCoords, withoutCoords];
  }, [locations]);

  if (status === 'loading') return <p className="text-slate-600">Loading map-ready locations...</p>;
  if (status === 'error') return <p className="rounded-md bg-red-50 p-4 text-red-700">{error}</p>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Map-ready locations</h1>
        <p className="mt-2 text-slate-600">This view prepares location data for a future interactive map component.</p>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold">Locations with coordinates ({withCoordinates.length})</h2>
        <ul className="mt-3 space-y-2 text-sm">
          {withCoordinates.map((location) => (
            <li key={location.id} className="rounded-md bg-slate-50 p-3">
              <Link to={`/locations/${location.id}`} className="font-medium text-indigo-600 hover:underline">
                {location.name}
              </Link>
              <p className="text-slate-700">
                lat: {location.latitude}, lng: {location.longitude} · certainty: {location.certainty_level || 'unknown'}
              </p>
            </li>
          ))}
        </ul>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold">Locations without coordinates ({withoutCoordinates.length})</h2>
        <p className="mt-2 text-sm text-slate-600">These can still be displayed in map side-panels or fallback lists.</p>
        <ul className="mt-3 space-y-2 text-sm">
          {withoutCoordinates.map((location) => (
            <li key={location.id} className="rounded-md bg-slate-50 p-3">
              <Link to={`/locations/${location.id}`} className="font-medium text-indigo-600 hover:underline">
                {location.name}
              </Link>
              <p className="text-slate-700">certainty: {location.certainty_level || 'unknown'}</p>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
