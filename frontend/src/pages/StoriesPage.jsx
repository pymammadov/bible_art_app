import { Link } from 'react-router-dom';
import { useEffect, useMemo, useState } from 'react';
import { getStories } from '../api';

const TESTAMENTS = ['All', 'Old Testament', 'New Testament'];

export default function StoriesPage() {
  const [stories, setStories] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');
  const [testament, setTestament] = useState('All');
  const [search, setSearch] = useState('');

  useEffect(() => {
    setStatus('loading');
    setError('');

    const params = testament === 'All' ? {} : { testament };
    getStories(params)
      .then((data) => {
        setStories(data.items || []);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load stories');
        setStatus('error');
      });
  }, [testament]);

  const filteredStories = useMemo(() => {
    const normalized = search.toLowerCase().trim();
    if (!normalized) {
      return stories;
    }

    return stories.filter((story) => {
      return (
        story.title.toLowerCase().includes(normalized) ||
        story.summary.toLowerCase().includes(normalized) ||
        story.scripture_reference.toLowerCase().includes(normalized)
      );
    });
  }, [stories, search]);

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
        <p className="mt-2 text-slate-600">Explore Bible stories and connected characters, locations, and artworks.</p>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex flex-wrap gap-2">
            {TESTAMENTS.map((option) => (
              <button
                key={option}
                type="button"
                onClick={() => setTestament(option)}
                className={`rounded-full px-3 py-1 text-sm font-medium transition ${
                  testament === option ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                {option}
              </button>
            ))}
          </div>
          <input
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search title, summary, reference"
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-indigo-400 focus:outline-none sm:max-w-xs"
          />
        </div>
      </section>

      <p className="text-sm text-slate-500">Showing {filteredStories.length} stories.</p>

      <ul className="grid gap-4 sm:grid-cols-2">
        {filteredStories.map((story) => (
          <li key={story.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md">
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
