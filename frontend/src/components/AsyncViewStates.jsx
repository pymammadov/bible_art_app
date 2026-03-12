export function LoadingGrid({ count = 6 }) {
  return (
    <ul className="grid gap-4 sm:grid-cols-2" aria-live="polite" aria-busy="true">
      {Array.from({ length: count }).map((_, index) => (
        <li key={index} className="animate-pulse rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div className="h-5 w-1/2 rounded bg-slate-200" />
          <div className="mt-3 h-3 w-1/3 rounded bg-slate-200" />
          <div className="mt-2 h-3 w-5/6 rounded bg-slate-200" />
          <div className="mt-2 h-3 w-2/3 rounded bg-slate-200" />
        </li>
      ))}
    </ul>
  );
}

export function ErrorState({ title, error, onRetry }) {
  return (
    <section className="rounded-md border border-red-200 bg-red-50 p-4 text-red-700">
      <p className="font-medium">{title}</p>
      <p className="mt-1 text-sm">{error || 'Unknown error'}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 rounded-md bg-red-600 px-3 py-2 text-sm font-medium text-white hover:bg-red-700"
        >
          Retry
        </button>
      )}
    </section>
  );
}

export function EmptyState({ message }) {
  return <section className="rounded-lg border border-slate-200 bg-white p-6 text-center text-slate-600 shadow-sm">{message}</section>;
}
