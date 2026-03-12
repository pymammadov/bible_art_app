import { Link } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import { getLocations } from '../api';
import { EmptyState, ErrorState, LoadingGrid } from '../components/AsyncViewStates';

export default function LocationsPage() {
  const [locations, setLocations] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const loadLocations = useCallback(() => {
    setStatus('loading');
    setError('');
    getLocations()
      .then((data) => {
        setLocations(Array.isArray(data?.items) ? data.items : []);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load locations');
        setLocations([]);
        setStatus('error');
      });
  }, []);

  useEffect(() => {
    loadLocations();
  }, [loadLocations]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Locations</h1>
        <p className="mt-2 text-slate-600">Explore biblical places and discover connected stories.</p>
      </div>

      {status === 'error' && <ErrorState title="Could not load locations." error={error} onRetry={loadLocations} />}

      {status === 'loading' ? (
        <LoadingGrid />
      ) : locations.length === 0 ? (
        <EmptyState message="No locations available yet." />
      ) : (
        <ul className="grid gap-4 sm:grid-cols-2">
          {locations.map((location) => (
            <li key={location.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md">
              <h2 className="text-lg font-semibold">
                <Link to={`/locations/${location.id}`} className="hover:text-indigo-600">
                  {location.name}
                </Link>
              </h2>
              <p className="mt-3 text-sm text-slate-700">{location.description || 'No description provided.'}</p>
              <p className="mt-3 text-xs text-slate-500">Related stories: {(location.relationships?.stories || []).length}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
