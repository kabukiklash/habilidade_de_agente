import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { quotesApi } from '../services/quotesApi';
import { QuotesTable } from '../components/quotes/QuotesTable';

export function QuotesPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: quotes, isLoading, isError } = useQuery({
    queryKey: ['quotes'],
    queryFn: quotesApi.getQuotes,
  });

  const deleteMutation = useMutation({
    mutationFn: quotesApi.deleteQuote,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quotes'] });
    },
  });

  const handleDelete = (quote: any) => {
    if (window.confirm(`Tem certeza que deseja excluir o orçamento ${quote.quoteNumber}?`)) {
      deleteMutation.mutate(quote.id);
    }
  };

  const handleEdit = (quote: any) => {
    navigate(`/quotes/${quote.id}`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">Orçamentos</h1>
          <p className="text-slate-400 text-sm mt-1">Gerencie os orçamentos gerados para seus clientes.</p>
        </div>
        <button
          onClick={() => navigate('/quotes/new')}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Novo Orçamento
        </button>
      </div>

      {/* Content */}
      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="w-8 h-8 border-4 border-slate-700 border-t-blue-500 rounded-full animate-spin" />
        </div>
      ) : isError ? (
        <div className="bg-red-400/10 border border-red-400/20 text-red-400 p-4 rounded-lg">
          Ocorreu um erro ao carregar os orçamentos. Tente novamente.
        </div>
      ) : (
        <QuotesTable 
          quotes={quotes || []} 
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}
    </div>
  );
}
