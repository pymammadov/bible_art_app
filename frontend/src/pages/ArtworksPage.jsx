import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getArtworks } from '../api';

export default function ArtworksPage() {
  const [artworks, setArtworks] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  useEffect(() => {
    setStatus('loading');
    setError('');
    getArtworks()
      .then((data) => {
        setArtworks(Array.isArray(data?.items) ? data.items : []);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load artworks');
        setStatus('error');
      });
  }, []);

  if (status === 'loading') return <p className="text-slate-600">Loading artworks...</p>;
  if (status === 'error') return <p className="rounded-md bg-red-50 p-4 text-red-700">{error}</p>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Artworks</h1>
        <p className="mt-2 text-slate-600">Browse artwork inspired by biblical narratives.</p>
      </div>
      <ul className="grid gap-4 sm:grid-cols-2">
        {artworks.map((artwork) => (
          <li key={artwork.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="text-lg font-semibold">
              <Link to={`/artworks/${artwork.id}`} className="hover:text-indigo-600">
                {artwork.title}
              </Link>
            </h2>
            <p className="mt-1 text-sm text-slate-600">{artwork.artist} {artwork.year ? `(${artwork.year})` : ''}</p>
            <p className="mt-3 text-sm text-slate-700">{artwork.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
