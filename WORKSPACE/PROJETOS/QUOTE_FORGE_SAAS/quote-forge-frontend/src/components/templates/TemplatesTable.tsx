import { Pencil, Trash2 } from 'lucide-react';
import type { Template } from '../../services/templatesApi';

interface TemplatesTableProps {
  templates: Template[];
  onEdit: (template: Template) => void;
  onDelete: (template: Template) => void;
}

export function TemplatesTable({ templates, onEdit, onDelete }: TemplatesTableProps) {
  if (templates.length === 0) {
    return (
      <div className="bg-slate-800 rounded-lg p-8 text-center border border-slate-700">
        <p className="text-slate-400">Nenhum template cadastrado ainda.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-700 bg-slate-800/50">
              <th className="p-4 text-sm font-semibold text-slate-300">NOME</th>
              <th className="p-4 text-sm font-semibold text-slate-300">DESCRIÇÃO</th>
              <th className="p-4 text-sm font-semibold text-slate-300">ITENS</th>
              <th className="p-4 text-sm font-semibold text-slate-300 w-24">AÇÕES</th>
            </tr>
          </thead>
          <tbody>
            {templates.map((template) => (
              <tr 
                key={template.id}
                className="border-b border-slate-700 hover:bg-slate-700/50 transition-colors"
              >
                <td className="p-4 text-slate-200">{template.name}</td>
                <td className="p-4 text-slate-400">{template.description || '-'}</td>
                <td className="p-4 text-slate-400">{template.items?.length || 0}</td>
                <td className="p-4">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => onEdit(template)}
                      className="p-1.5 text-slate-400 hover:text-blue-400 hover:bg-blue-400/10 rounded transition-colors"
                      title="Editar"
                    >
                      <Pencil className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onDelete(template)}
                      className="p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-400/10 rounded transition-colors"
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
