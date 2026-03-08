import { Link, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
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

export default function StoryDetailPage() {
  const { storyId } = useParams();
  const [story, setStory] = useState(null);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  useEffect(() => {
    setStatus('loading');
    getStoryById(storyId)
      .then((data) => {
        setStory(data);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load story');
        setStatus('error');
      });
  }, [storyId]);

  if (status === 'loading') {
    return <p className="text-slate-600">Loading story...</p>;
  }

  if (status === 'error') {
    return <p className="rounded-md bg-red-50 p-4 text-red-700">{error}</p>;
  }

  return (
    <div className="space-y-6">
      <Link to="/" className="text-sm font-medium text-indigo-600 hover:underline">
        ← Back to stories
      </Link>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="text-xs font-semibold uppercase tracking-wide text-indigo-600">{story.testament}</div>
        <h1 className="mt-1 text-2xl font-bold">{story.title}</h1>
        <p className="mt-1 text-sm text-slate-600">{story.scripture_reference}</p>
        <p className="mt-4 text-slate-700">{story.summary}</p>
        <p className="mt-3 text-slate-600">{story.description}</p>
      </section>

      <div className="grid gap-4 md:grid-cols-3">
        <RelatedList
          title="Characters"
          items={story.relationships?.characters || []}
          renderItem={(character) => (
            <>
              <p className="font-medium text-slate-900">{character.name}</p>
              <p className="text-slate-600">{character.description}</p>
            </>
          )}
        />
        <RelatedList
          title="Locations"
          items={story.relationships?.locations || []}
          renderItem={(location) => (
            <>
              <p className="font-medium text-slate-900">{location.name}</p>
              <p className="text-slate-600">{location.region}</p>
            </>
          )}
        />
        <RelatedList
          title="Artworks"
          items={story.relationships?.artworks || []}
          renderItem={(artwork) => (
            <>
              <p className="font-medium text-slate-900">{artwork.title}</p>
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
