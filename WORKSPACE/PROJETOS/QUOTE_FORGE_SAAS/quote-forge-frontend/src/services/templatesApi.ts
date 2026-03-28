import { api } from './api';

export interface TemplateItem {
  id: string;
  templateId: string;
  name: string;
  description?: string;
  price: number;
  quantityDefault: number;
}

export interface Template {
  id: string;
  tenantId: string;
  name: string;
  description?: string;
  createdAt: string;
  items: TemplateItem[];
}

export interface CreateTemplateItemDTO {
  name: string;
  description?: string;
  price: number;
  quantityDefault?: number;
}

export interface CreateTemplateDTO {
  name: string;
  description?: string;
  items?: CreateTemplateItemDTO[];
}

export const templatesApi = {
  getTemplates: async (): Promise<Template[]> => {
    const response = await api.get('/templates');
    return response.data;
  },

  getTemplate: async (id: string): Promise<Template> => {
    const response = await api.get(`/templates/${id}`);
    return response.data;
  },

  createTemplate: async (data: CreateTemplateDTO): Promise<Template> => {
    const response = await api.post('/templates', data);
    return response.data;
  },

  updateTemplate: async (id: string, data: Partial<CreateTemplateDTO>): Promise<Template> => {
    const response = await api.put(`/templates/${id}`, data);
    return response.data;
  },

  deleteTemplate: async (id: string): Promise<void> => {
    await api.delete(`/templates/${id}`);
  },

  addTemplateItem: async (templateId: string, item: CreateTemplateItemDTO): Promise<TemplateItem> => {
    const response = await api.post(`/templates/${templateId}/items`, item);
    return response.data;
  },

  deleteTemplateItem: async (itemId: string): Promise<void> => {
    await api.delete(`/template-items/${itemId}`);
  }
};
