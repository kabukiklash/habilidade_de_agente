import type { Client } from '../../services/clientsApi';
import { Pencil, Trash2 } from 'lucide-react';

interface ClientsTableProps {
  clients: Client[];
  onEdit: (client: Client) => void;
  onDelete: (client: Client) => void;
}

export function ClientsTable({ clients, onEdit, onDelete }: ClientsTableProps) {
  if (clients.length === 0) {
    return (
      <div className="bg-slate-800 rounded-lg p-8 text-center text-slate-400">
        Nenhum cliente cadastrado.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto bg-slate-800 rounded-xl border border-slate-700">
      <table className="w-full text-left text-sm text-slate-300">
        <thead className="bg-slate-900/50 text-xs text-slate-400 uppercase">
          <tr>
            <th className="px-6 py-4 font-semibold">Nome</th>
            <th className="px-6 py-4 font-semibold">Empresa</th>
            <th className="px-6 py-4 font-semibold">Email</th>
            <th className="px-6 py-4 font-semibold">Telefone</th>
            <th className="px-6 py-4 font-semibold text-right">Ações</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-700">
          {clients.map((client) => (
            <tr key={client.id} className="hover:bg-slate-700/50 transition-colors">
              <td className="px-6 py-4 font-medium text-slate-100">{client.name}</td>
              <td className="px-6 py-4">{client.company || '-'}</td>
              <td className="px-6 py-4">{client.email || '-'}</td>
              <td className="px-6 py-4">{client.phone || '-'}</td>
              <td className="px-6 py-4 text-right space-x-3">
                <button
                  onClick={() => onEdit(client)}
                  className="text-blue-400 hover:text-blue-300 transition-colors"
                  title="Editar"
                >
                  <Pencil size={18} />
                </button>
                <button
                  onClick={() => onDelete(client)}
                  className="text-red-400 hover:text-red-300 transition-colors"
                  title="Excluir"
                >
                  <Trash2 size={18} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
