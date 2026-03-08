import { Link } from 'react-router-dom';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-5xl px-4 py-4 sm:px-6 lg:px-8">
          <Link to="/" className="text-xl font-semibold text-indigo-600">
            Bible Art App
          </Link>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
    </div>
  );
}
