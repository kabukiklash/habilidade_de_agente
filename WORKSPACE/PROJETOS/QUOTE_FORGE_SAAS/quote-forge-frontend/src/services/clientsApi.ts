import { api } from './api';

export interface Client {
  id: string;
  tenantId: string;
  name: string;
  email: string | null;
  phone: string | null;
  company: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface CreateClientDTO {
  name: string;
  email?: string;
  phone?: string;
  company?: string;
}

export const clientsApi = {
  getClients: async (): Promise<Client[]> => {
    const response = await api.get('/clients');
    return response.data;
  },

  getClient: async (id: string): Promise<Client> => {
    const response = await api.get(`/clients/${id}`);
    return response.data;
  },

  createClient: async (data: CreateClientDTO): Promise<Client> => {
    const response = await api.post('/clients', data);
    return response.data;
  },

  updateClient: async (id: string, data: Partial<CreateClientDTO>): Promise<Client> => {
    const response = await api.put(`/clients/${id}`, data);
    return response.data;
  },

  deleteClient: async (id: string): Promise<void> => {
    await api.delete(`/clients/${id}`);
  }
};
