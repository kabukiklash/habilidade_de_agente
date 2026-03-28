import type { Client } from '../../services/clientsApi';
import { AlertTriangle } from 'lucide-react';

interface DeleteClientDialogProps {
  client: Client;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading?: boolean;
}

export function DeleteClientDialog({ client, onConfirm, onCancel, isLoading }: DeleteClientDialogProps) {
  return (
    <div className="text-center">
      <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-900/30 mb-4">
        <AlertTriangle className="h-6 w-6 text-red-500" />
      </div>
      <h3 className="text-lg font-medium text-slate-100 mb-2">Excluir Cliente</h3>
      <p className="text-sm text-slate-400 mb-6">
        Tem certeza que deseja excluir o cliente <strong className="text-slate-200">{client.name}</strong>? Esta ação não poderá ser desfeita.
      </p>
      
      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          className="px-4 py-2 text-slate-300 hover:text-white transition-colors disabled:opacity-50"
        >
          Cancelar
        </button>
        <button
          type="button"
          onClick={onConfirm}
          disabled={isLoading}
          className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
        >
          {isLoading ? 'Excluindo...' : 'Sim, Excluir'}
        </button>
      </div>
    </div>
  );
}
