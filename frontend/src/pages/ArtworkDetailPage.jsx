import { Link, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getArtworkById } from '../api';

export default function ArtworkDetailPage() {
  const { artworkId } = useParams();
  const [artwork, setArtwork] = useState(null);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  useEffect(() => {
    setStatus('loading');
    setError('');
    getArtworkById(artworkId)
      .then((data) => {
        setArtwork(data);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load artwork');
        setStatus('error');
      });
  }, [artworkId]);

  if (status === 'loading') return <p className="text-slate-600">Loading artwork...</p>;
  if (status === 'error' || !artwork) return <p className="rounded-md bg-red-50 p-4 text-red-700">{error || 'Artwork not found'}</p>;

  return (
    <div className="space-y-6">
      <Link to="/artworks" className="text-sm font-medium text-indigo-600 hover:underline">← Back to artworks</Link>
      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h1 className="text-2xl font-bold">{artwork.title}</h1>
        <p className="mt-1 text-sm text-slate-600">{artwork.artist} {artwork.year ? `(${artwork.year})` : ''}</p>
        <p className="mt-1 text-sm text-slate-600">{artwork.medium}</p>
        <p className="mt-1 text-sm text-slate-600">{artwork.current_location}</p>
        <p className="mt-3 text-slate-700">{artwork.description}</p>
      </section>
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold">Related stories</h2>
        {(artwork.relationships?.stories || []).length === 0 ? (
          <p className="mt-2 text-sm text-slate-500">No related stories.</p>
        ) : (
          <ul className="mt-2 space-y-2">
            {artwork.relationships.stories.map((story) => (
              <li key={story.id} className="text-sm">
                <Link className="text-indigo-600 hover:underline" to={`/stories/${story.id}`}>
                  {story.title}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
      {artwork.relationships?.related_story && (
        <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold">Primary related story</h2>
          <Link className="mt-2 inline-block text-sm text-indigo-600 hover:underline" to={`/stories/${artwork.relationships.related_story.id}`}>
            {artwork.relationships.related_story.title}
          </Link>
        </section>
      )}
    </div>
  );
}
