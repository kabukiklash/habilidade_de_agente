import { useQuery } from '@tanstack/react-query';

const API_URL = '/api';

export function DashboardPage() {
  const { data: health, isLoading } = useQuery({
    queryKey: ['health'],
    queryFn: () => fetch(`${API_URL}/health`).then((r) => r.json()),
  });

  return (
    <div>
      <h1 style={{ marginBottom: '1rem' }}>Dashboard Afix</h1>
      <p style={{ color: 'var(--afix-text-muted)' }}>
        Plataforma de Gestão Inteligente de Atendimento via WhatsApp
      </p>
      <div
        style={{
          marginTop: '2rem',
          padding: '1rem',
          background: 'var(--afix-surface)',
          borderRadius: 'var(--afix-radius)',
          border: '1px solid var(--afix-border)',
        }}
      >
        <h3 style={{ margin: '0 0 0.5rem' }}>Status do Backend</h3>
        {isLoading ? (
          <p>Carregando...</p>
        ) : health?.status === 'ok' ? (
          <p style={{ color: 'green' }}>✓ Conectado — {health.service}</p>
        ) : (
          <p style={{ color: 'orange' }}>Backend não disponível. Execute: npm run dev:backend</p>
        )}
      </div>
    </div>
  );
}
