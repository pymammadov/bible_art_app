import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getLocations } from '../api';

export default function LocationsPage() {
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

  if (status === 'loading') return <p className="text-slate-600">Loading locations...</p>;
  if (status === 'error') return <p className="rounded-md bg-red-50 p-4 text-red-700">{error}</p>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Locations</h1>
        <p className="mt-2 text-slate-600">Explore traditional and probable biblical places.</p>
      </div>
      <ul className="grid gap-4 sm:grid-cols-2">
        {locations.map((location) => (
          <li key={location.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="text-lg font-semibold">
              <Link to={`/locations/${location.id}`} className="hover:text-indigo-600">
                {location.name}
              </Link>
            </h2>
            <p className="mt-1 text-sm text-slate-600">{location.region}</p>
            <p className="mt-1 text-sm text-slate-600">certainty: {location.certainty_level || 'unknown'}</p>
            <p className="mt-3 text-sm text-slate-700">{location.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
