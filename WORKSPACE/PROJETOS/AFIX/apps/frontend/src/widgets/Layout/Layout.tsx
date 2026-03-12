import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside
        style={{
          width: 240,
          background: 'var(--afix-surface)',
          borderRight: '1px solid var(--afix-border)',
          padding: '1.5rem 1rem',
        }}
      >
        <h2 style={{ margin: '0 0 1.5rem', fontSize: '1.25rem' }}>Afix</h2>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <Link to="/" style={{ padding: '0.5rem', borderRadius: 'var(--afix-radius)' }}>
            Dashboard
          </Link>
          <Link to="/leads" style={{ padding: '0.5rem', borderRadius: 'var(--afix-radius)' }}>
            Leads
          </Link>
        </nav>
      </aside>
      <main style={{ flex: 1, padding: '2rem', overflow: 'auto' }}>{children}</main>
    </div>
  );
}
