import { api } from './api';
import type { Client } from './clientsApi';
import type { Template } from './templatesApi';

export interface QuoteItem {
  id: string;
  quoteId: string;
  name: string;
  description?: string;
  price: number;
  quantity: number;
  total: number;
}

export interface Quote {
  id: string;
  tenantId: string;
  clientId: string;
  templateId?: string;
  quoteNumber: string;
  title: string;
  status: 'draft' | 'sent' | 'approved' | 'rejected';
  notes?: string;
  currency: string;
  subtotal: number;
  tax: number;
  total: number;
  createdAt: string;
  items: QuoteItem[];
  client?: Client;
  template?: Template;
}

export interface CreateQuoteDTO {
  clientId: string;
  templateId?: string;
  quoteNumber: string;
  title: string;
  notes?: string;
  currency?: string;
}

export interface CreateFromTemplateDTO {
  clientId: string;
  templateId: string;
  quoteNumber: string;
  title: string;
}

export interface CreateQuoteItemDTO {
  name: string;
  description?: string;
  price: number;
  quantity: number;
}

export const quotesApi = {
  // Core Quote Actions
  getQuotes: async (): Promise<Quote[]> => {
    const { data } = await api.get('/quotes');
    return data;
  },

  getQuote: async (id: string): Promise<Quote> => {
    const { data } = await api.get(`/quotes/${id}`);
    return data;
  },

  createQuote: async (quoteData: CreateQuoteDTO): Promise<Quote> => {
    const { data } = await api.post('/quotes', quoteData);
    return data;
  },

  createFromTemplate: async (quoteData: CreateFromTemplateDTO): Promise<Quote> => {
    const { data } = await api.post('/quotes/from-template', quoteData);
    return data;
  },

  updateQuote: async (id: string, quoteData: Partial<CreateQuoteDTO>): Promise<Quote> => {
    const { data } = await api.put(`/quotes/${id}`, quoteData);
    return data;
  },

  deleteQuote: async (id: string): Promise<void> => {
    await api.delete(`/quotes/${id}`);
  },

  // Quote Item Actions
  addQuoteItem: async (quoteId: string, itemData: CreateQuoteItemDTO): Promise<QuoteItem> => {
    const { data } = await api.post(`/quotes/${quoteId}/items`, itemData);
    return data;
  },

  updateQuoteItem: async (itemId: string, itemData: Partial<CreateQuoteItemDTO>): Promise<QuoteItem> => {
    const { data } = await api.put(`/quote-items/${itemId}`, itemData);
    return data;
  },

  deleteQuoteItem: async (itemId: string): Promise<void> => {
    await api.delete(`/quote-items/${itemId}`);
  }
};
