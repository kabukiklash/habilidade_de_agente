import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2, X, Check } from 'lucide-react';
import { quotesApi } from '../../services/quotesApi';
import type { QuoteItem, CreateQuoteItemDTO } from '../../services/quotesApi';

interface QuoteItemsEditorProps {
  quoteId: string;
  items: QuoteItem[];
  currency: string;
}

export function QuoteItemsEditor({ quoteId, items, currency }: QuoteItemsEditorProps) {
  const queryClient = useQueryClient();
  const [isAdding, setIsAdding] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form states
  const [formData, setFormData] = useState<CreateQuoteItemDTO>({
    name: '',
    description: '',
    price: 0,
    quantity: 1,
  });

  const resetForm = () => {
    setFormData({ name: '', description: '', price: 0, quantity: 1 });
    setIsAdding(false);
    setEditingId(null);
  };

  const startEdit = (item: QuoteItem) => {
    setFormData({
      name: item.name,
      description: item.description || '',
      price: item.price,
      quantity: item.quantity,
    });
    setEditingId(item.id);
    setIsAdding(false);
  };

  // Mutations
  const addMutation = useMutation({
    mutationFn: (data: CreateQuoteItemDTO) => quotesApi.addQuoteItem(quoteId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quote', quoteId] });
      resetForm();
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<CreateQuoteItemDTO> }) =>
      quotesApi.updateQuoteItem(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quote', quoteId] });
      resetForm();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: quotesApi.deleteQuoteItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quote', quoteId] });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingId) {
      updateMutation.mutate({ id: editingId, data: formData });
    } else {
      addMutation.mutate(formData);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(value);
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium text-white">Itens do Orçamento</h3>
        {!isAdding && !editingId && (
          <button
            onClick={() => setIsAdding(true)}
            className="text-sm bg-slate-700 hover:bg-slate-600 text-white px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5"
          >
            <Plus className="w-4 h-4" />
            Adicionar Item
          </button>
        )}
      </div>

      <div className="bg-slate-800/50 rounded-lg border border-slate-700 overflow-hidden">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-slate-800 border-b border-slate-700">
            <tr>
              <th className="px-4 py-3 font-medium">Nome / Descrição</th>
              <th className="px-4 py-3 font-medium text-right w-32">Preço Unit.</th>
              <th className="px-4 py-3 font-medium text-center w-24">Qtd</th>
              <th className="px-4 py-3 font-medium text-right w-32">Total</th>
              <th className="px-4 py-3 font-medium text-center w-20">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {items.map((item) => (
              <tr key={item.id} className={editingId === item.id ? 'bg-slate-700/30' : ''}>
                {editingId === item.id ? (
                  <td colSpan={5} className="p-0">
                    <form onSubmit={handleSubmit} className="flex flex-wrap p-2 gap-2">
                       <input
                          type="text"
                          required
                          value={formData.name}
                          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                          placeholder="Nome"
                          className="flex-1 min-w-[150px] bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white"
                        />
                        <input
                          type="text"
                          value={formData.description}
                          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                          placeholder="Descrição"
                          className="flex-none w-40 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white"
                        />
                        <input
                          type="number"
                          step="0.01"
                          required
                          value={formData.price}
                          onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) || 0 })}
                          placeholder="Preço"
                          className="w-24 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white text-right"
                        />
                        <input
                          type="number"
                          min="1"
                          required
                          value={formData.quantity}
                          onChange={(e) => setFormData({ ...formData, quantity: parseInt(e.target.value) || 1 })}
                          className="w-20 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white text-center"
                        />
                        <div className="flex items-center gap-1">
                          <button
                            type="submit"
                            disabled={updateMutation.isPending}
                            className="bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 p-1.5 rounded-md transition-colors"
                          >
                            <Check className="w-4 h-4" />
                          </button>
                          <button
                            type="button"
                            onClick={resetForm}
                            className="bg-red-500/20 text-red-400 hover:bg-red-500/30 p-1.5 rounded-md transition-colors"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                    </form>
                  </td>
                ) : (
                  <>
                    <td className="px-4 py-3">
                      <div className="font-medium text-white">{item.name}</div>
                      {item.description && <div className="text-xs text-slate-500 mt-0.5">{item.description}</div>}
                    </td>
                    <td className="px-4 py-3 text-right font-mono">{formatCurrency(item.price)}</td>
                    <td className="px-4 py-3 text-center">{item.quantity}</td>
                    <td className="px-4 py-3 text-right font-mono font-medium text-white">{formatCurrency(item.total)}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1">
                        <button
                          onClick={() => startEdit(item)}
                          className="p-1 hover:text-blue-400 transition-colors"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => deleteMutation.mutate(item.id)}
                          className="p-1 hover:text-red-400 transition-colors"
                          disabled={deleteMutation.isPending}
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </>
                )}
              </tr>
            ))}
            
            {/* Row for Adding New Item */}
            {isAdding && (
               <tr>
               <td colSpan={5} className="p-0 border-t border-slate-700">
                 <form onSubmit={handleSubmit} className="flex flex-wrap p-2 gap-2 bg-slate-700/20">
                    <input
                       type="text"
                       required
                       value={formData.name}
                       onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                       placeholder="Nome do Item"
                       className="flex-1 min-w-[150px] bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white"
                     />
                     <input
                       type="text"
                       value={formData.description}
                       onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                       placeholder="Descrição"
                       className="flex-none w-40 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white"
                     />
                     <input
                       type="number"
                       step="0.01"
                       required
                       value={formData.price}
                       onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) || 0 })}
                       placeholder="Preço"
                       className="w-24 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white text-right"
                     />
                     <input
                       type="number"
                       min="1"
                       required
                       value={formData.quantity}
                       onChange={(e) => setFormData({ ...formData, quantity: parseInt(e.target.value) || 1 })}
                       className="w-20 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-white text-center"
                     />
                     <div className="flex items-center gap-1">
                       <button
                         type="submit"
                         disabled={addMutation.isPending}
                         className="bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 p-1.5 rounded-md transition-colors"
                       >
                         <Check className="w-4 h-4" />
                       </button>
                       <button
                         type="button"
                         onClick={resetForm}
                         className="bg-red-500/20 text-red-400 hover:bg-red-500/30 p-1.5 rounded-md transition-colors"
                       >
                         <X className="w-4 h-4" />
                       </button>
                     </div>
                 </form>
               </td>
             </tr>
            )}

            {items.length === 0 && !isAdding && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-slate-500 text-sm">
                  Nenhum item adicionado a este orçamento.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
