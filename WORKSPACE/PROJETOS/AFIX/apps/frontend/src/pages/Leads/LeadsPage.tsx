import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import { CreateLeadForm } from '@/features/leads/CreateLeadForm';
import type { Lead, EstagioFunil } from '@afix/shared';

export function LeadsPage() {
  const { data: leads = [], isLoading } = useQuery<Lead[]>({
    queryKey: ['leads'],
    queryFn: () => api.get<Lead[]>('/leads'),
  });

  const { data: estagios = [], isLoading: loadingEstagios } = useQuery<EstagioFunil[]>({
    queryKey: ['estagios-funil'],
    queryFn: () => api.get<EstagioFunil[]>('/estagios-funil'),
  });

  return (
    <div>
      <h1 style={{ marginBottom: '1rem' }}>Leads</h1>
      <p style={{ color: 'var(--afix-text-muted)', marginBottom: '1.5rem' }}>
        Gestão de leads e funil de vendas (CRM)
      </p>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(280px, 320px) 1fr',
          gap: '2rem',
        }}
      >
        <aside>
          <CreateLeadForm estagios={estagios} />
        </aside>

        <section>
          {isLoading || loadingEstagios ? (
            <p>Carregando...</p>
          ) : leads.length === 0 ? (
            <div
              style={{
                padding: '2rem',
                background: 'var(--afix-surface)',
                borderRadius: 'var(--afix-radius)',
                border: '1px dashed var(--afix-border)',
                textAlign: 'center',
                color: 'var(--afix-text-muted)',
              }}
            >
              Nenhum lead cadastrado. Use o formulário ao lado para criar.
            </div>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
              {leads.map((lead) => (
                <li
                  key={lead.id}
                  style={{
                    padding: '1rem',
                    marginBottom: '0.5rem',
                    background: 'var(--afix-surface)',
                    borderRadius: 'var(--afix-radius)',
                    border: '1px solid var(--afix-border)',
                  }}
                >
                  <strong>{lead.nome}</strong> — {lead.telefone}
                  {lead.email && ` | ${lead.email}`}
                  <span style={{ marginLeft: '0.5rem', color: 'var(--afix-text-muted)' }}>
                    | Score: {lead.score}
                    {lead.valorPotencial != null && ` | R$ ${Number(lead.valorPotencial).toFixed(2)}`}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}
