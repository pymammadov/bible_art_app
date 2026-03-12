import { Link } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import { getCharacters } from '../api';
import { EmptyState, ErrorState, LoadingGrid } from '../components/AsyncViewStates';

export default function CharactersPage() {
  const [characters, setCharacters] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const loadCharacters = useCallback(() => {
    setStatus('loading');
    setError('');
    getCharacters()
      .then((data) => {
        setCharacters(Array.isArray(data?.items) ? data.items : []);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load characters');
        setCharacters([]);
        setStatus('error');
      });
  }, []);

  useEffect(() => {
    loadCharacters();
  }, [loadCharacters]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Characters</h1>
        <p className="mt-2 text-slate-600">Browse biblical characters and jump into related stories.</p>
      </div>

      {status === 'error' && <ErrorState title="Could not load characters." error={error} onRetry={loadCharacters} />}

      {status === 'loading' ? (
        <LoadingGrid />
      ) : characters.length === 0 ? (
        <EmptyState message="No characters available yet." />
      ) : (
        <ul className="grid gap-4 sm:grid-cols-2">
          {characters.map((character) => (
            <li key={character.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md">
              <h2 className="text-lg font-semibold">
                <Link to={`/characters/${character.id}`} className="hover:text-indigo-600">
                  {character.name}
                </Link>
              </h2>
              <p className="mt-3 text-sm text-slate-700">{character.description || 'No description provided.'}</p>
              <p className="mt-3 text-xs text-slate-500">
                Related stories: {(character.relationships?.stories || []).length}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
