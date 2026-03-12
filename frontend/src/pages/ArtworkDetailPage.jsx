import { Link, useParams } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import { getArtworkById } from '../api';
import { EmptyState, ErrorState } from '../components/AsyncViewStates';

export default function ArtworkDetailPage() {
  const { artworkId } = useParams();
  const [artwork, setArtwork] = useState(null);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const loadArtwork = useCallback(() => {
    if (!artworkId) {
      setStatus('error');
      setError('Artwork id is missing.');
      return;
    }

    setStatus('loading');
    setError('');
    getArtworkById(artworkId)
      .then((data) => {
        setArtwork(data);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load artwork');
        setArtwork(null);
        setStatus('error');
      });
  }, [artworkId]);

  useEffect(() => {
    loadArtwork();
  }, [loadArtwork]);

  if (status === 'loading') return <p className="text-slate-600">Loading artwork...</p>;

  if (status === 'error' || !artwork) {
    return (
      <div className="space-y-4">
        <Link to="/artworks" className="text-sm font-medium text-indigo-600 hover:underline">
          ← Back to artworks
        </Link>
        <ErrorState title="Could not load this artwork." error={error || 'Artwork not found'} onRetry={loadArtwork} />
      </div>
    );
  }

  const relatedStories = artwork.relationships?.stories || [];

  return (
    <div className="space-y-6">
      <Link to="/artworks" className="text-sm font-medium text-indigo-600 hover:underline">
        ← Back to artworks
      </Link>
      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h1 className="text-2xl font-bold">{artwork.title}</h1>
        <p className="mt-1 text-sm text-slate-600">
          {artwork.artist || 'Unknown artist'}
          {artwork.year ? ` (${artwork.year})` : ''}
        </p>
        <p className="mt-1 text-sm text-slate-600">{artwork.museum || 'Museum unknown'}</p>
        <p className="mt-3 text-slate-700">{artwork.description || 'No description provided.'}</p>
        {artwork.related_story_id && (
          <p className="mt-3 text-sm text-slate-600">
            Primary related story ID: <span className="font-medium">{artwork.related_story_id}</span>
          </p>
        )}
      </section>
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold">Related stories</h2>
        {relatedStories.length === 0 ? (
          <EmptyState message="No related stories for this artwork." />
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
