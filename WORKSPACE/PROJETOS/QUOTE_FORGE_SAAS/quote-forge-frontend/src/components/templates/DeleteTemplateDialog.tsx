import { AlertTriangle } from 'lucide-react';
import type { Template } from '../../services/templatesApi';

interface DeleteTemplateDialogProps {
  template: Template;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading?: boolean;
}

export function DeleteTemplateDialog({ template, onConfirm, onCancel, isLoading }: DeleteTemplateDialogProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 text-red-400 p-4 bg-red-400/10 rounded-lg border border-red-400/20">
        <AlertTriangle className="w-5 h-5 flex-shrink-0" />
        <p className="text-sm">
          Tem certeza que deseja excluir o template <strong>{template.name}</strong>? Esta ação não pode ser desfeita e removerá todos os itens vinculados a ele.
        </p>
      </div>

      <div className="flex justify-end gap-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors"
          disabled={isLoading}
        >
          Cancelar
        </button>
        <button
          type="button"
          onClick={onConfirm}
          className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors flex items-center justify-center min-w-[100px]"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            'Excluir'
          )}
        </button>
      </div>
    </div>
  );
}
