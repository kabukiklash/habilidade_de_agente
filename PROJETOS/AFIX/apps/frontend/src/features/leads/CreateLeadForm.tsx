import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import type { EstagioFunil } from '@afix/shared';

const EMPRESA_DEFAULT = 'empresa-default';

interface CreateLeadFormProps {
  estagios: EstagioFunil[];
  onSuccess?: () => void;
}

export function CreateLeadForm({ estagios, onSuccess }: CreateLeadFormProps) {
  const queryClient = useQueryClient();
  const [nome, setNome] = useState('');
  const [telefone, setTelefone] = useState('');
  const [email, setEmail] = useState('');
  const [origem, setOrigem] = useState('whatsapp');
  const [estagioFunilId, setEstagioFunilId] = useState(estagios[0]?.id ?? '');
  const [valorPotencial, setValorPotencial] = useState('');

  const createMutation = useMutation({
    mutationFn: (data: {
      nome: string;
      telefone: string;
      email?: string;
      origem: string;
      estagioFunilId: string;
      valorPotencial?: number;
      empresaId: string;
    }) => api.post('/leads', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['leads'] });
      setNome('');
      setTelefone('');
      setEmail('');
      setValorPotencial('');
      setEstagioFunilId(estagios[0]?.id ?? '');
      onSuccess?.();
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!nome.trim() || !telefone.trim() || !estagioFunilId) return;
    createMutation.mutate({
      nome: nome.trim(),
      telefone: telefone.trim(),
      email: email.trim() || undefined,
      origem,
      estagioFunilId,
      valorPotencial: valorPotencial ? parseFloat(valorPotencial) : undefined,
      empresaId: EMPRESA_DEFAULT,
    });
  };

  if (estagios.length === 0) {
    return (
      <div style={{ ...formStyle, opacity: 0.7 }}>
        <h3 style={{ margin: '0 0 1rem' }}>Novo Lead</h3>
        <p style={{ color: 'var(--afix-text-muted)', margin: 0 }}>
          Carregando estágios do funil...
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <h3 style={{ margin: '0 0 1rem' }}>Novo Lead</h3>
      <div style={fieldStyle}>
        <label htmlFor="nome">Nome *</label>
        <input
          id="nome"
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
          placeholder="Nome completo"
          style={inputStyle}
        />
      </div>
      <div style={fieldStyle}>
        <label htmlFor="telefone">Telefone *</label>
        <input
          id="telefone"
          type="tel"
          value={telefone}
          onChange={(e) => setTelefone(e.target.value)}
          required
          placeholder="(11) 99999-9999"
          style={inputStyle}
        />
      </div>
      <div style={fieldStyle}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email@exemplo.com"
          style={inputStyle}
        />
      </div>
      <div style={fieldStyle}>
        <label htmlFor="origem">Origem</label>
        <select
          id="origem"
          value={origem}
          onChange={(e) => setOrigem(e.target.value)}
          style={inputStyle}
        >
          <option value="whatsapp">WhatsApp</option>
          <option value="site">Site</option>
          <option value="indicacao">Indicação</option>
          <option value="campanha">Campanha</option>
          <option value="outro">Outro</option>
        </select>
      </div>
      <div style={fieldStyle}>
        <label htmlFor="estagio">Estágio do Funil</label>
        <select
          id="estagio"
          value={estagioFunilId}
          onChange={(e) => setEstagioFunilId(e.target.value)}
          required
          style={inputStyle}
        >
          {estagios.map((e) => (
            <option key={e.id} value={e.id}>
              {e.nome}
            </option>
          ))}
        </select>
      </div>
      <div style={fieldStyle}>
        <label htmlFor="valor">Valor Potencial (R$)</label>
        <input
          id="valor"
          type="number"
          step="0.01"
          min="0"
          value={valorPotencial}
          onChange={(e) => setValorPotencial(e.target.value)}
          placeholder="0,00"
          style={inputStyle}
        />
      </div>
      {createMutation.isError && (
        <p style={{ color: '#dc2626', margin: '0 0 0.5rem', fontSize: '0.875rem' }}>
          {createMutation.error instanceof Error ? createMutation.error.message : 'Erro ao salvar'}
        </p>
      )}
      <button type="submit" disabled={createMutation.isPending} style={buttonStyle}>
        {createMutation.isPending ? 'Salvando...' : 'Cadastrar Lead'}
      </button>
    </form>
  );
}

const formStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: '0.75rem',
  padding: '1.5rem',
  background: 'var(--afix-surface)',
  borderRadius: 'var(--afix-radius)',
  border: '1px solid var(--afix-border)',
};

const fieldStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: '0.25rem',
};

const inputStyle: React.CSSProperties = {
  padding: '0.5rem 0.75rem',
  border: '1px solid var(--afix-border)',
  borderRadius: 'var(--afix-radius)',
  fontSize: '1rem',
};

const buttonStyle: React.CSSProperties = {
  padding: '0.75rem 1rem',
  background: 'var(--afix-primary)',
  color: 'white',
  border: 'none',
  borderRadius: 'var(--afix-radius)',
  fontSize: '1rem',
  fontWeight: 500,
  cursor: 'pointer',
};
