import { Link, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getLocationById } from '../api';

export default function LocationDetailPage() {
  const { locationId } = useParams();
  const [location, setLocation] = useState(null);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  useEffect(() => {
    setStatus('loading');
    setError('');
    getLocationById(locationId)
      .then((data) => {
        setLocation(data);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load location');
        setStatus('error');
      });
  }, [locationId]);

  if (status === 'loading') return <p className="text-slate-600">Loading location...</p>;
  if (status === 'error' || !location) return <p className="rounded-md bg-red-50 p-4 text-red-700">{error || 'Location not found'}</p>;

  return (
    <div className="space-y-6">
      <Link to="/locations" className="text-sm font-medium text-indigo-600 hover:underline">← Back to locations</Link>
      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h1 className="text-2xl font-bold">{location.name}</h1>
        <p className="mt-1 text-sm text-slate-600">{location.region}</p>
        <p className="mt-3 text-slate-700">{location.description}</p>
      </section>
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold">Stories</h2>
        {(location.relationships?.stories || []).length === 0 ? (
          <p className="mt-2 text-sm text-slate-500">No related stories.</p>
        ) : (
          <ul className="mt-2 space-y-2">
            {location.relationships.stories.map((story) => (
              <li key={story.id} className="text-sm">
                <Link className="text-indigo-600 hover:underline" to={`/stories/${story.id}`}>
                  {story.title}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
