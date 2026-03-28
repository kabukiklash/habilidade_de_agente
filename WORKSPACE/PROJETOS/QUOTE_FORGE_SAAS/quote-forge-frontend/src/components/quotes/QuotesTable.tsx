import { Pencil, Trash2, FileText } from 'lucide-react';
import type { Quote } from '../../services/quotesApi';

interface QuotesTableProps {
  quotes: Quote[];
  onEdit: (quote: Quote) => void;
  onDelete: (quote: Quote) => void;
}

const statusMap = {
  draft: { label: 'Rascunho', color: 'bg-slate-500/20 text-slate-400 border-slate-500/30' },
  sent: { label: 'Enviado', color: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
  approved: { label: 'Aprovado', color: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' },
  rejected: { label: 'Rejeitado', color: 'bg-red-500/20 text-red-400 border-red-500/30' },
};

const formatCurrency = (value: number, currency: string) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(value);
};

export function QuotesTable({ quotes, onEdit, onDelete }: QuotesTableProps) {
  if (quotes.length === 0) {
    return (
      <div className="bg-slate-800 rounded-xl border border-slate-700 p-8 text-center">
        <FileText className="w-12 h-12 text-slate-500 mx-auto mb-4" />
        <p className="text-slate-400">Nenhum orçamento cadastrado ainda.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-slate-800 border-b border-slate-700">
            <tr>
              <th className="px-6 py-4 text-sm font-semibold text-slate-300">Nº e Título</th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-300">Cliente</th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-300">Status</th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-300 text-right">Total</th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-300 text-center w-24">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {quotes.map((quote) => (
              <tr key={quote.id} className="hover:bg-slate-700/30 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex flex-col">
                     <span className="text-xs font-mono text-slate-500">{quote.quoteNumber}</span>
                     <span className="text-sm font-medium text-white">{quote.title}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                   <div className="text-sm text-slate-300">
                     {/* Se a API trouxer o object client populado, exibimos, senão mostramos o ID por enquanto */}
                     {quote.client?.name || quote.clientId}
                   </div>
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${statusMap[quote.status].color}`}>
                    {statusMap[quote.status].label}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-slate-300 text-right font-mono">
                  {formatCurrency(quote.total, quote.currency)}
                </td>
                <td className="px-6 py-4 h-full">
                  <div className="flex items-center justify-center gap-2">
                    <button
                      onClick={() => onEdit(quote)}
                      className="p-1.5 text-slate-400 hover:text-blue-400 hover:bg-slate-700 rounded-lg transition-colors"
                      title="Editar"
                    >
                      <Pencil className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onDelete(quote)}
                      className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-slate-700 rounded-lg transition-colors"
                      title="Excluir"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
