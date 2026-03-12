import { Link, useParams } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import { getStoryById } from '../api';

function RelatedList({ title, items, renderItem }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold">{title}</h2>
      {items.length === 0 ? (
        <p className="mt-2 text-sm text-slate-500">No related {title.toLowerCase()}.</p>
      ) : (
        <ul className="mt-3 space-y-2 text-sm">
          {items.map((item) => (
            <li key={item.id} className="rounded-md bg-slate-50 p-3">
              {renderItem(item)}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function LoadingStory() {
  return (
    <div className="space-y-4" aria-live="polite" aria-busy="true">
      <div className="h-4 w-36 animate-pulse rounded bg-slate-200" />
      <section className="animate-pulse rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="h-3 w-28 rounded bg-slate-200" />
        <div className="mt-3 h-7 w-2/3 rounded bg-slate-200" />
        <div className="mt-4 h-4 w-full rounded bg-slate-200" />
        <div className="mt-2 h-4 w-5/6 rounded bg-slate-200" />
      </section>
    </div>
  );
}

export default function StoryDetailPage() {
  const { storyId } = useParams();
  const [story, setStory] = useState(null);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const loadStory = useCallback(() => {
    if (!storyId) {
      setStory(null);
      setStatus('error');
      setError('Story id is missing.');
      return;
    }

    setStatus('loading');
    setError('');
    getStoryById(storyId)
      .then((data) => {
        if (!data || typeof data !== 'object') {
          throw new Error('Story data is invalid.');
        }
        setStory(data);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load story');
        setStory(null);
        setStatus('error');
      });
  }, [storyId]);

  useEffect(() => {
    loadStory();
  }, [loadStory]);

  if (status === 'loading') {
    return <LoadingStory />;
  }

  if (status === 'error' || !story) {
    return (
      <section className="space-y-4">
        <Link to="/" className="text-sm font-medium text-indigo-600 hover:underline">
          ← Back to stories
        </Link>
        <div className="rounded-md border border-red-200 bg-red-50 p-4 text-red-700">
          <p className="font-medium">Could not load this story.</p>
          <p className="mt-1 text-sm">{error || 'Unknown error'}</p>
          <button
            type="button"
            onClick={loadStory}
            className="mt-3 rounded-md bg-red-600 px-3 py-2 text-sm font-medium text-white hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </section>
    );
  }

  return (
    <div className="space-y-6">
      <Link to="/" className="text-sm font-medium text-indigo-600 hover:underline">
        ← Back to stories
      </Link>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="text-xs font-semibold uppercase tracking-wide text-indigo-600">{story.testament}</div>
        <h1 className="mt-1 text-2xl font-bold">{story.title}</h1>
        <p className="mt-4 text-slate-700">{story.summary || 'No summary available.'}</p>
      </section>

      <div className="grid gap-4 md:grid-cols-3">
        <RelatedList
          title="Characters"
          items={story.relationships?.characters || []}
          renderItem={(character) => (
            <>
              <Link to={`/characters/${character.id}`} className="font-medium text-indigo-600 hover:underline">
                {character.name}
              </Link>
              <p className="text-slate-600">{character.description}</p>
            </>
          )}
        />
        <RelatedList
          title="Locations"
          items={story.relationships?.locations || []}
          renderItem={(location) => (
            <>
              <Link to={`/locations/${location.id}`} className="font-medium text-indigo-600 hover:underline">
                {location.name}
              </Link>
              <p className="text-slate-600">{location.description}</p>
            </>
          )}
        />
        <RelatedList
          title="Artworks"
          items={story.relationships?.artworks || []}
          renderItem={(artwork) => (
            <>
              <Link to={`/artworks/${artwork.id}`} className="font-medium text-indigo-600 hover:underline">
                {artwork.title}
              </Link>
              <p className="text-slate-600">
                {artwork.artist} {artwork.year ? `(${artwork.year})` : ''}
              </p>
            </>
          )}
        />
      </div>
    </div>
  );
}
