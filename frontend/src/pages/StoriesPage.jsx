import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getStories } from '../api';

export default function StoriesPage() {
  const [stories, setStories] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  useEffect(() => {
    getStories()
      .then((data) => {
        setStories(data.items || []);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load stories');
        setStatus('error');
      });
  }, []);

  if (status === 'loading') {
    return <p className="text-slate-600">Loading stories...</p>;
  }

  if (status === 'error') {
    return <p className="rounded-md bg-red-50 p-4 text-red-700">{error}</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Stories</h1>
        <p className="mt-2 text-slate-600">Browse biblical stories and their characters, locations, and artworks.</p>
      </div>

      <ul className="grid gap-4 sm:grid-cols-2">
        {stories.map((story) => (
          <li key={story.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-indigo-600">{story.testament}</div>
            <h2 className="text-lg font-semibold">
              <Link className="hover:text-indigo-600" to={`/stories/${story.id}`}>
                {story.title}
              </Link>
            </h2>
            <p className="mt-1 text-sm text-slate-600">{story.scripture_reference}</p>
            <p className="mt-3 text-sm text-slate-700">{story.summary}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
