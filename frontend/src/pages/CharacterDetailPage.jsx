import { Link, useParams } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import { getCharacterById } from '../api';
import { EmptyState, ErrorState } from '../components/AsyncViewStates';

export default function CharacterDetailPage() {
  const { characterId } = useParams();
  const [character, setCharacter] = useState(null);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const loadCharacter = useCallback(() => {
    if (!characterId) {
      setStatus('error');
      setError('Character id is missing.');
      return;
    }

    setStatus('loading');
    setError('');
    getCharacterById(characterId)
      .then((data) => {
        setCharacter(data);
        setStatus('ready');
      })
      .catch((err) => {
        setError(err.message || 'Unable to load character');
        setCharacter(null);
        setStatus('error');
      });
  }, [characterId]);

  useEffect(() => {
    loadCharacter();
  }, [loadCharacter]);

  if (status === 'loading') return <p className="text-slate-600">Loading character...</p>;

  if (status === 'error' || !character) {
    return (
      <div className="space-y-4">
        <Link to="/characters" className="text-sm font-medium text-indigo-600 hover:underline">
          ← Back to characters
        </Link>
        <ErrorState title="Could not load this character." error={error || 'Character not found'} onRetry={loadCharacter} />
      </div>
    );
  }

  const relatedStories = character.relationships?.stories || [];

  return (
    <div className="space-y-6">
      <Link to="/characters" className="text-sm font-medium text-indigo-600 hover:underline">
        ← Back to characters
      </Link>
      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h1 className="text-2xl font-bold">{character.name}</h1>
        <p className="mt-3 text-slate-700">{character.description || 'No description provided.'}</p>
      </section>
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold">Related stories</h2>
        {relatedStories.length === 0 ? (
          <EmptyState message="No related stories for this character." />
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
