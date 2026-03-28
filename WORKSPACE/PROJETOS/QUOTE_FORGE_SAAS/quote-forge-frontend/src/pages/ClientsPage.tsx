import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, X } from 'lucide-react';
import { clientsApi } from '../services/clientsApi';
import type { Client, CreateClientDTO } from '../services/clientsApi';
import { ClientsTable } from '../components/clients/ClientsTable';
import { ClientForm } from '../components/clients/ClientForm';
import { DeleteClientDialog } from '../components/clients/DeleteClientDialog';

export function ClientsPage() {
  const queryClient = useQueryClient();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);

  // Queries
  const { data: clients, isLoading, isError } = useQuery({
    queryKey: ['clients'],
    queryFn: clientsApi.getClients
  });

  // Mutations
  const createMutation = useMutation({
    mutationFn: (data: CreateClientDTO) => clientsApi.createClient(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clients'] });
      closeForm();
    }
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<CreateClientDTO> }) => 
      clientsApi.updateClient(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clients'] });
      closeForm();
    }
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => clientsApi.deleteClient(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clients'] });
      closeDeleteDialog();
    }
  });

  // Handlers
  const handleAddClick = () => {
    setSelectedClient(null);
    setIsFormOpen(true);
  };

  const handleEditClick = (client: Client) => {
    setSelectedClient(client);
    setIsFormOpen(true);
  };

  const handleDeleteClick = (client: Client) => {
    setSelectedClient(client);
    setIsDeleteDialogOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
    setSelectedClient(null);
  };

  const closeDeleteDialog = () => {
    setIsDeleteDialogOpen(false);
    setSelectedClient(null);
  };

  const handleFormSubmit = (data: CreateClientDTO) => {
    if (selectedClient) {
      updateMutation.mutate({ id: selectedClient.id, data });
    } else {
      createMutation.mutate(data);
    }
  };

  const handleDeleteConfirm = () => {
    if (selectedClient) {
      deleteMutation.mutate(selectedClient.id);
    }
  };

  // Modal Wrapper Component (Simple inline for MVP)
  const Modal = ({ isOpen, onClose, title, children }: any) => {
    if (!isOpen) return null;
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div className="bg-slate-900 rounded-xl shadow-2xl w-full max-w-md border border-slate-700 overflow-hidden">
          <div className="flex justify-between items-center p-4 border-b border-slate-800">
            <h2 className="text-lg font-semibold text-slate-100">{title}</h2>
            <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
              <X size={20} />
            </button>
          </div>
          <div className="p-4">
            {children}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Clientes</h1>
          <p className="text-slate-400">Gerencie a base de clientes do seu sistema.</p>
        </div>
        <button
          onClick={handleAddClick}
          className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center shadow-lg shadow-blue-900/20 transition-all font-medium"
        >
          <Plus size={20} className="mr-2" />
          Novo Cliente
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-10 text-slate-400">Carregando clientes...</div>
      ) : isError ? (
        <div className="text-center py-10 text-red-400">Erro ao carregar os clientes. Verifique sua conexão.</div>
      ) : (
        <ClientsTable 
          clients={clients || []} 
          onEdit={handleEditClick} 
          onDelete={handleDeleteClick} 
        />
      )}

      {/* Form Modal */}
      <Modal 
        isOpen={isFormOpen} 
        onClose={closeForm} 
        title={selectedClient ? "Editar Cliente" : "Novo Cliente"}
      >
        <ClientForm 
          initialData={selectedClient} 
          onSubmit={handleFormSubmit} 
          onCancel={closeForm}
          isLoading={createMutation.isPending || updateMutation.isPending}
        />
      </Modal>

      {/* Delete Dialog */}
      <Modal
        isOpen={isDeleteDialogOpen}
        onClose={closeDeleteDialog}
        title="Confirmar Ação"
      >
        {selectedClient && (
          <DeleteClientDialog
            client={selectedClient}
            onConfirm={handleDeleteConfirm}
            onCancel={closeDeleteDialog}
            isLoading={deleteMutation.isPending}
          />
        )}
      </Modal>
    </div>
  );
}
