import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, X } from 'lucide-react';
import { templatesApi } from '../services/templatesApi';
import type { Template, CreateTemplateDTO } from '../services/templatesApi';
import { TemplatesTable } from '../components/templates/TemplatesTable';
import { TemplateForm } from '../components/templates/TemplateForm';
import { DeleteTemplateDialog } from '../components/templates/DeleteTemplateDialog';

export function TemplatesPage() {
  const queryClient = useQueryClient();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);

  // Queries
  const { data: templates, isLoading, isError } = useQuery({
    queryKey: ['templates'],
    queryFn: templatesApi.getTemplates,
  });

  // Mutations
  const createMutation = useMutation({
    mutationFn: templatesApi.createTemplate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] });
      handleCloseForm();
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<CreateTemplateDTO> }) => 
      templatesApi.updateTemplate(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] });
      handleCloseForm();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: templatesApi.deleteTemplate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] });
      setIsDeleteDialogOpen(false);
      setSelectedTemplate(null);
    },
  });

  // Handlers
  const handleOpenForm = (template?: Template) => {
    setSelectedTemplate(template || null);
    setIsFormOpen(true);
  };

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setSelectedTemplate(null);
  };

  const handleSubmit = (data: CreateTemplateDTO) => {
    if (selectedTemplate) {
      updateMutation.mutate({ id: selectedTemplate.id, data });
    } else {
      createMutation.mutate(data);
    }
  };

  const handleDeleteClick = (template: Template) => {
    setSelectedTemplate(template);
    setIsDeleteDialogOpen(true);
  };

  const handleConfirmDelete = () => {
    if (selectedTemplate) {
      deleteMutation.mutate(selectedTemplate.id);
    }
  };

  const isMutating = createMutation.isPending || updateMutation.isPending;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">Templates</h1>
          <p className="text-slate-400 text-sm mt-1">Gerencie os modelos de orçamentos e itens padrão.</p>
        </div>
        <button
          onClick={() => handleOpenForm()}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Novo Template
        </button>
      </div>

      {/* Content */}
      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="w-8 h-8 border-4 border-slate-700 border-t-blue-500 rounded-full animate-spin" />
        </div>
      ) : isError ? (
        <div className="bg-red-400/10 border border-red-400/20 text-red-400 p-4 rounded-lg">
          Ocorreu um erro ao carregar os templates. Tente novamente.
        </div>
      ) : (
        <TemplatesTable 
          templates={templates || []} 
          onEdit={handleOpenForm}
          onDelete={handleDeleteClick}
        />
      )}

      {/* Form Modal */}
      {isFormOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="bg-slate-800 rounded-xl shadow-xl w-full max-w-2xl border border-slate-700 flex flex-col max-h-[90vh]">
            <div className="flex justify-between items-center p-6 border-b border-slate-700">
              <h2 className="text-xl font-semibold text-white">
                {selectedTemplate ? 'Editar Template' : 'Novo Template'}
              </h2>
              <button 
                onClick={handleCloseForm}
                className="text-slate-400 hover:text-white transition-colors"
                disabled={isMutating}
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto">
              <TemplateForm 
                initialData={selectedTemplate}
                onSubmit={handleSubmit}
                onCancel={handleCloseForm}
                isLoading={isMutating}
              />
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {isDeleteDialogOpen && selectedTemplate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="bg-slate-800 rounded-xl shadow-xl w-full max-w-md border border-slate-700">
            <div className="flex justify-between items-center p-6 border-b border-slate-700">
              <h2 className="text-xl font-semibold text-white">Excluir Template</h2>
              <button 
                onClick={() => setIsDeleteDialogOpen(false)}
                className="text-slate-400 hover:text-white transition-colors"
                disabled={deleteMutation.isPending}
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-6">
              <DeleteTemplateDialog 
                template={selectedTemplate}
                onConfirm={handleConfirmDelete}
                onCancel={() => setIsDeleteDialogOpen(false)}
                isLoading={deleteMutation.isPending}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
