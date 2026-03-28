import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, Save, Copy } from 'lucide-react';
import { quotesApi } from '../services/quotesApi';
import { clientsApi } from '../services/clientsApi';
import { templatesApi } from '../services/templatesApi';
import { QuoteItemsEditor } from '../components/quotes/QuoteItemsEditor';
import { QuoteSummary } from '../components/quotes/QuoteSummary';
import type { CreateFromTemplateDTO, CreateQuoteDTO } from '../services/quotesApi';

export function QuoteBuilderPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isNew = id === 'new';

  // Local Form State for Creation
  const [clientId, setClientId] = useState('');
  const [templateId, setTemplateId] = useState('');
  const [title, setTitle] = useState('');
  const [quoteNumber, setQuoteNumber] = useState('');
  const [notes, setNotes] = useState('');

  // Local Form State for Edit mode updates
  const [editTitle, setEditTitle] = useState('');
  const [editNotes, setEditNotes] = useState('');

  // Queries
  const { data: clients, isLoading: loadingClients } = useQuery({
    queryKey: ['clients'],
    queryFn: clientsApi.getClients,
    enabled: isNew
  });

  const { data: templates, isLoading: loadingTemplates } = useQuery({
    queryKey: ['templates'],
    queryFn: templatesApi.getTemplates,
    enabled: isNew
  });

  const { data: quote, isLoading: loadingQuote } = useQuery({
    queryKey: ['quote', id],
    queryFn: () => quotesApi.getQuote(id!),
    enabled: !isNew,
  });

  // Keep Edit fields in sync when quote loads
  if (!isNew && quote && !editTitle && editTitle !== quote.title) {
    setEditTitle(quote.title);
    setEditNotes(quote.notes || '');
  }

  // Mutations
  const createFromTemplateMutation = useMutation({
    mutationFn: (data: CreateFromTemplateDTO) => quotesApi.createFromTemplate(data),
    onSuccess: (newQuote) => {
      queryClient.invalidateQueries({ queryKey: ['quotes'] });
      navigate(`/quotes/${newQuote.id}`, { replace: true });
    },
  });

  const createBlankMutation = useMutation({
    mutationFn: (data: CreateQuoteDTO) => quotesApi.createQuote(data),
    onSuccess: (newQuote) => {
      queryClient.invalidateQueries({ queryKey: ['quotes'] });
      navigate(`/quotes/${newQuote.id}`, { replace: true });
    },
  });

  const updateQuoteMutation = useMutation({
    mutationFn: (data: Partial<CreateQuoteDTO>) => quotesApi.updateQuote(id!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quote', id] });
      queryClient.invalidateQueries({ queryKey: ['quotes'] });
      // Show success toast maybe? We'll just rely on the query invalidation.
    },
  });

  // Handlers
  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!clientId || !title || !quoteNumber) return;

    if (templateId) {
      createFromTemplateMutation.mutate({ clientId, templateId, title, quoteNumber });
    } else {
      createBlankMutation.mutate({ clientId, title, quoteNumber, notes });
    }
  };

  const handleUpdate = () => {
    if (!quote) return;
    updateQuoteMutation.mutate({ title: editTitle, notes: editNotes });
  };

  const isMutating = createFromTemplateMutation.isPending || createBlankMutation.isPending || updateQuoteMutation.isPending;

  if (loadingQuote && !isNew) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="w-8 h-8 border-4 border-slate-700 border-t-blue-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button 
          onClick={() => navigate('/quotes')}
          className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-white">
            {isNew ? 'Criar Novo Orçamento' : `Orçamento ${quote?.quoteNumber}`}
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            {isNew ? 'Selecione um cliente e opcionalmente um template para iniciar.' : quote?.title}
          </p>
        </div>
        {!isNew && (
          <button
            onClick={handleUpdate}
            disabled={isMutating}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
          >
            <Save className="w-5 h-5" />
            Salvar Alterações
          </button>
        )}
      </div>

      {isNew ? (
        /* CREATE VIEW */
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
          <form onSubmit={handleCreate} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
               <div className="space-y-4">
                 <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">
                      Nº do Orçamento *
                    </label>
                    <input
                      required
                      type="text"
                      value={quoteNumber}
                      onChange={(e) => setQuoteNumber(e.target.value)}
                      placeholder="Ex: QF-001"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    />
                 </div>
                 <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">
                      Título do Projeto *
                    </label>
                    <input
                      required
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      placeholder="Ex: Refatoração de Website"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                    />
                 </div>
               </div>
               <div className="space-y-4">
                 <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">
                      Cliente *
                    </label>
                    <select
                      required
                      value={clientId}
                      onChange={(e) => setClientId(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none"
                    >
                      <option value="" disabled>Selecione um cliente...</option>
                      {clients?.map((c) => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                      ))}
                    </select>
                 </div>
                 <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">
                      Usar Template (Opcional)
                    </label>
                    <div className="relative">
                      <select
                        value={templateId}
                        onChange={(e) => setTemplateId(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-blue-500 outline-none appearance-none"
                      >
                        <option value="">Iniciar em branco</option>
                        {templates?.map((t) => (
                          <option key={t.id} value={t.id}>{t.name}</option>
                        ))}
                      </select>
                      <Copy className="w-4 h-4 text-slate-400 absolute right-4 top-3 pointer-events-none" />
                    </div>
                 </div>
               </div>
            </div>

            <div className="flex justify-end pt-4 border-t border-slate-700">
               <button
                 type="submit"
                 disabled={isMutating || !clientId || !title || !quoteNumber}
                 className="bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-medium transition-colors"
               >
                 Gerar Orçamento
               </button>
            </div>
          </form>
        </div>
      ) : (
        /* EDIT / BUILDER VIEW */
        quote && (
          <div className="space-y-6">
            {/* Meta Data Editor */}
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                 <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">Título</label>
                    <input
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white outline-none"
                    />
                 </div>
                 <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">Cliente</label>
                    <input
                      type="text"
                      disabled
                      value={quote.client?.name || quote.clientId}
                      className="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2 text-slate-400 outline-none cursor-not-allowed"
                    />
                 </div>
                 <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-slate-300 mb-1">Observações Internas</label>
                    <textarea
                      value={editNotes}
                      onChange={(e) => setEditNotes(e.target.value)}
                      rows={2}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white outline-none resize-none"
                    />
                 </div>
               </div>
            </div>

            {/* Items Editor */}
            <QuoteItemsEditor 
              quoteId={quote.id} 
              items={quote.items || []} 
              currency={quote.currency}
            />

            {/* Totals Widget */}
            <div className="flex justify-end pt-4">
              <QuoteSummary 
                subtotal={quote.subtotal} 
                tax={quote.tax} 
                total={quote.total} 
                currency={quote.currency} 
              />
            </div>
          </div>
        )
      )}
    </div>
  );
}
