import { Link } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import { getArtworks } from '../api';
import { EmptyState, ErrorState, LoadingGrid } from '../components/AsyncViewStates';

export default function ArtworksPage() {
  const [artworks, setArtworks] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const loadArtworks = useCallback(() => {
    setStatus('loading');
    setError('');
    getArtworks()
      .then((data) => {
        setArtworks(Array.isArray(data?.items) ? data.items : []);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load artworks');
        setArtworks([]);
        setStatus('error');
      });
  }, []);

  useEffect(() => {
    loadArtworks();
  }, [loadArtworks]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Artworks</h1>
        <p className="mt-2 text-slate-600">Browse art inspired by biblical narratives and linked stories.</p>
      </div>

      {status === 'error' && <ErrorState title="Could not load artworks." error={error} onRetry={loadArtworks} />}

      {status === 'loading' ? (
        <LoadingGrid />
      ) : artworks.length === 0 ? (
        <EmptyState message="No artworks available yet." />
      ) : (
        <ul className="grid gap-4 sm:grid-cols-2">
          {artworks.map((artwork) => (
            <li key={artwork.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md">
              <h2 className="text-lg font-semibold">
                <Link to={`/artworks/${artwork.id}`} className="hover:text-indigo-600">
                  {artwork.title}
                </Link>
              </h2>
              <p className="mt-1 text-sm text-slate-600">
                {artwork.artist || 'Unknown artist'}
                {artwork.year ? ` (${artwork.year})` : ''}
              </p>
              <p className="mt-1 text-sm text-slate-600">{artwork.museum || 'Museum unknown'}</p>
              <p className="mt-3 text-sm text-slate-700">{artwork.description || 'No description provided.'}</p>
              <p className="mt-3 text-xs text-slate-500">Related stories: {(artwork.relationships?.stories || []).length}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
