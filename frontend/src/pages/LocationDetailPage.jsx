import { Link, useParams } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import { getLocationById } from '../api';
import { EmptyState, ErrorState } from '../components/AsyncViewStates';

export default function LocationDetailPage() {
  const { locationId } = useParams();
  const [location, setLocation] = useState(null);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const loadLocation = useCallback(() => {
    if (!locationId) {
      setStatus('error');
      setError('Location id is missing.');
      return;
    }

    setStatus('loading');
    setError('');
    getLocationById(locationId)
      .then((data) => {
        setLocation(data);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load location');
        setLocation(null);
        setStatus('error');
      });
  }, [locationId]);

  useEffect(() => {
    loadLocation();
  }, [loadLocation]);

  if (status === 'loading') return <p className="text-slate-600">Loading location...</p>;

  if (status === 'error' || !location) {
    return (
      <div className="space-y-4">
        <Link to="/locations" className="text-sm font-medium text-indigo-600 hover:underline">
          ← Back to locations
        </Link>
        <ErrorState title="Could not load this location." error={error || 'Location not found'} onRetry={loadLocation} />
      </div>
    );
  }

  const relatedStories = location.relationships?.stories || [];

  return (
    <div className="space-y-6">
      <Link to="/locations" className="text-sm font-medium text-indigo-600 hover:underline">
        ← Back to locations
      </Link>
      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h1 className="text-2xl font-bold">{location.name}</h1>
        <p className="mt-3 text-slate-700">{location.description || 'No description provided.'}</p>
      </section>
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold">Related stories</h2>
        {relatedStories.length === 0 ? (
          <EmptyState message="No related stories for this location." />
        ) : (
          <ul className="mt-2 space-y-2">
            {relatedStories.map((story) => (
              <li key={story.id} className="rounded-md bg-slate-50 p-3 text-sm">
                <Link className="font-medium text-indigo-600 hover:underline" to={`/stories/${story.id}`}>
                  {story.title}
                </Link>
                <p className="mt-1 text-slate-600">{story.summary}</p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
