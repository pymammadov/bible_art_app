import { Link } from 'react-router-dom';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { API_BASE_URL, getStories } from '../api';

const TESTAMENTS = ['All', 'Old Testament', 'New Testament'];

function LoadingStories() {
  return (
    <ul className="grid gap-4 sm:grid-cols-2" aria-live="polite" aria-busy="true">
      {Array.from({ length: 6 }).map((_, index) => (
        <li key={index} className="animate-pulse rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div className="h-3 w-28 rounded bg-slate-200" />
          <div className="mt-3 h-5 w-2/3 rounded bg-slate-200" />
          <div className="mt-4 h-3 w-full rounded bg-slate-200" />
          <div className="mt-2 h-3 w-5/6 rounded bg-slate-200" />
        </li>
      ))}
    </ul>
  );
}

export default function StoriesPage() {
  const [stories, setStories] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');
  const [testament, setTestament] = useState('All');
  const [search, setSearch] = useState('');

  const loadStories = useCallback(() => {
    setStatus('loading');
    setError('');

    const params = testament === 'All' ? {} : { testament };
    getStories(params)
      .then((data) => {
        const items = Array.isArray(data?.items) ? data.items : [];
        setStories(items);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load stories');
        setStories([]);
        setStatus('error');
      });
  }, [testament]);

  useEffect(() => {
    loadStories();
  }, [loadStories]);

  const filteredStories = useMemo(() => {
    const normalized = search.toLowerCase().trim();
    if (!normalized) {
      return stories;
    }

    return stories.filter((story) => {
      const title = story?.title || '';
      const summary = story?.summary || '';
      return title.toLowerCase().includes(normalized) || summary.toLowerCase().includes(normalized);
    });
  }, [stories, search]);

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
            placeholder="Search title or summary"
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-indigo-400 focus:outline-none sm:max-w-xs"
          />
        </div>
      </section>

      {status === 'error' && (
        <section className="rounded-md border border-red-200 bg-red-50 p-4 text-red-700">
          <p className="font-medium">Could not load stories.</p>
          <p className="mt-1 text-sm">{error}</p>
          <p className="mt-1 text-xs">
            Current API base URL: <code>{API_BASE_URL}</code>
          </p>
          <button
            type="button"
            onClick={loadStories}
            className="mt-3 rounded-md bg-red-600 px-3 py-2 text-sm font-medium text-white hover:bg-red-700"
          >
            Retry
          </button>
        </section>
      )}

      {status === 'loading' ? (
        <LoadingStories />
      ) : (
        <>
          <p className="text-sm text-slate-500">Showing {filteredStories.length} stories.</p>
          {filteredStories.length === 0 ? (
            <section className="rounded-lg border border-slate-200 bg-white p-6 text-center text-slate-600 shadow-sm">
              No stories match your current filters.
            </section>
          ) : (
            <ul className="grid gap-4 sm:grid-cols-2">
              {filteredStories.map((story) => (
                <li
                  key={story.id}
                  className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md"
                >
                  <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-indigo-600">{story.testament}</div>
                  <h2 className="text-lg font-semibold">
                    <Link className="hover:text-indigo-600" to={`/stories/${story.id}`}>
                      {story.title}
                    </Link>
                  </h2>
                  <p className="mt-3 text-sm text-slate-700">{story.summary}</p>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  );
}
