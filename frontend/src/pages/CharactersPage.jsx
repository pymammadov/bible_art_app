import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getCharacters } from '../api';

export default function CharactersPage() {
  const [characters, setCharacters] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  useEffect(() => {
    setStatus('loading');
    setError('');
    getCharacters()
      .then((data) => {
        setCharacters(Array.isArray(data?.items) ? data.items : []);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load characters');
        setStatus('error');
      });
  }, []);

  if (status === 'loading') {
    return <p className="text-slate-600">Loading characters...</p>;
  }

  if (status === 'error') {
    return <p className="rounded-md bg-red-50 p-4 text-red-700">{error}</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Characters</h1>
        <p className="mt-2 text-slate-600">Browse biblical characters connected to stories.</p>
      </div>
      <ul className="grid gap-4 sm:grid-cols-2">
        {characters.map((character) => (
          <li key={character.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="text-lg font-semibold">
              <Link to={`/characters/${character.id}`} className="hover:text-indigo-600">
                {character.name}
              </Link>
            </h2>
            <p className="mt-1 text-sm text-slate-600">{character.testament}</p>
            <p className="mt-3 text-sm text-slate-700">{character.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
