import { useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import type { CreateTemplateItemDTO } from '../../services/templatesApi';

interface TemplateItemsEditorProps {
  items: CreateTemplateItemDTO[];
  onChange: (items: CreateTemplateItemDTO[]) => void;
}

export function TemplateItemsEditor({ items, onChange }: TemplateItemsEditorProps) {
  const [newItem, setNewItem] = useState<CreateTemplateItemDTO>({
    name: '',
    description: '',
    price: 0,
    quantityDefault: 1
  });

  const handleAddItem = () => {
    if (!newItem.name || newItem.price < 0) return;
    onChange([...items, newItem]);
    setNewItem({ name: '', description: '', price: 0, quantityDefault: 1 });
  };

  const handleRemoveItem = (index: number) => {
    const newItems = [...items];
    newItems.splice(index, 1);
    onChange(newItems);
  };

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-semibold text-slate-300 border-b border-slate-700 pb-2">ITENS DO ORÇAMENTO</h3>
      
      {/* Lista de itens inseridos */}
      {items.length > 0 ? (
        <div className="space-y-2">
          {items.map((item, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-slate-900 rounded-md border border-slate-700">
              <div className="grid grid-cols-4 gap-4 w-full mr-4">
                <div className="col-span-2">
                  <p className="text-sm font-medium text-slate-200">{item.name}</p>
                  <p className="text-xs text-slate-400">{item.description}</p>
                </div>
                <div className="text-sm text-slate-300">R$ {Number(item.price).toFixed(2)}</div>
                <div className="text-sm text-slate-300">Qtd: {item.quantityDefault}</div>
              </div>
              <button
                type="button"
                onClick={() => handleRemoveItem(index)}
                className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-400/10 rounded transition-colors"
                title="Remover Item"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-slate-500 italic">Nenhum item adicionado a este template.</p>
      )}

      {/* Formulário de novo item rápido */}
      <div className="grid grid-cols-12 gap-3 items-end bg-slate-800/50 p-3 rounded-lg border border-dashed border-slate-700">
        <div className="col-span-4">
          <label className="block text-xs font-medium text-slate-400 mb-1">Nome</label>
          <input
            type="text"
            value={newItem.name}
            onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-white focus:outline-none focus:border-blue-500"
            placeholder="Nome do item"
          />
        </div>
        <div className="col-span-3">
          <label className="block text-xs font-medium text-slate-400 mb-1">Descrição</label>
          <input
            type="text"
            value={newItem.description || ''}
            onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-white focus:outline-none focus:border-blue-500"
            placeholder="Opcional"
          />
        </div>
        <div className="col-span-2">
          <label className="block text-xs font-medium text-slate-400 mb-1">Preço (R$)</label>
          <input
            type="number"
            step="0.01"
            min="0"
            value={newItem.price}
            onChange={(e) => setNewItem({ ...newItem, price: parseFloat(e.target.value) || 0 })}
            className="w-full bg-slate-900 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-white focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="col-span-2">
          <label className="block text-xs font-medium text-slate-400 mb-1">Qtd</label>
          <input
            type="number"
            min="1"
            value={newItem.quantityDefault}
            onChange={(e) => setNewItem({ ...newItem, quantityDefault: parseInt(e.target.value) || 1 })}
            className="w-full bg-slate-900 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-white focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="col-span-1">
          <button
            type="button"
            onClick={handleAddItem}
            disabled={!newItem.name}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-md p-1.5 flex justify-center items-center transition-colors"
          >
            <Plus className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
