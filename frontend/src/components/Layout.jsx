import { Link, NavLink } from 'react-router-dom';

const NAV_ITEMS = [
  { to: '/', label: 'Stories', end: true },
  { to: '/characters', label: 'Characters' },
  { to: '/locations', label: 'Locations' },
  { to: '/locations-map', label: 'Map-ready' },
  { to: '/artworks', label: 'Artworks' },
];

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-5xl flex-col gap-3 px-4 py-4 sm:px-6 lg:px-8">
          <Link to="/" className="text-xl font-semibold text-indigo-600">
            Bible Art App
          </Link>
          <nav className="flex flex-wrap gap-2">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `rounded-md px-3 py-1 text-sm font-medium ${
                    isActive ? 'bg-indigo-100 text-indigo-700' : 'text-slate-700 hover:bg-slate-100'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
    </div>
  );
}
