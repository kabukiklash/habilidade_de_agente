import { useState, useEffect } from 'react';
import type { CreateTemplateDTO, CreateTemplateItemDTO, Template } from '../../services/templatesApi';
import { TemplateItemsEditor } from './TemplateItemsEditor';

interface TemplateFormProps {
  initialData?: Template | null;
  onSubmit: (data: CreateTemplateDTO) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

export function TemplateForm({ initialData, onSubmit, onCancel, isLoading }: TemplateFormProps) {
  const [formData, setFormData] = useState<CreateTemplateDTO>({
    name: '',
    description: '',
    items: [],
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        description: initialData.description || '',
        items: initialData.items.map(i => ({ 
          name: i.name, 
          description: i.description, 
          price: i.price, 
          quantityDefault: i.quantityDefault 
        }))
      });
    }
  }, [initialData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleItemsChange = (newItems: CreateTemplateItemDTO[]) => {
    setFormData(prev => ({ ...prev, items: newItems }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-slate-300 mb-1">
            Nome do Template *
          </label>
          <input
            type="text"
            id="name"
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
            placeholder="Ex: Identidade Visual PRO"
          />
        </div>
        
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-slate-300 mb-1">
            Descrição
          </label>
          <textarea
            id="description"
            rows={3}
            value={formData.description || ''}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors resize-none"
            placeholder="Descreva o propósito deste template..."
          />
        </div>
      </div>

      <TemplateItemsEditor 
        items={formData.items || []} 
        onChange={handleItemsChange} 
      />

      <div className="flex justify-end gap-3 pt-4 border-t border-slate-700">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors"
          disabled={isLoading}
        >
          Cancelar
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors flex items-center justify-center min-w-[100px]"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            'Salvar'
          )}
        </button>
      </div>
    </form>
  );
}
