import { Request, Response } from 'express';
import { quotesService } from './quotes.service';

export const quotesController = {
  async createQuote(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const data = req.body;
      
      if (!data.clientId || !data.title || !data.quoteNumber) {
        return res.status(400).json({ error: 'Fields clientId, title and quoteNumber are required' });
      }

      const quote = await quotesService.createQuote(tenantId, data);
      return res.status(201).json(quote);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async createFromTemplate(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const { clientId, templateId, title, quoteNumber } = req.body;

      if (!clientId || !templateId || !title || !quoteNumber) {
         return res.status(400).json({ error: 'Fields clientId, templateId, quoteNumber and title are required' });
      }

      const quote = await quotesService.createFromTemplate(tenantId, { clientId, templateId, title, quoteNumber });
      return res.status(201).json(quote);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async getQuotes(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const quotes = await quotesService.getQuotes(tenantId);
      return res.json(quotes);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async getQuote(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      
      const quote = await quotesService.getQuoteById(id, tenantId);
      if (!quote) return res.status(404).json({ error: 'Quote not found' });
      
      return res.json(quote);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async updateQuote(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      const data = req.body;
      
      // Prevent updating sensitive calculation fields directly via outer update
      delete data.subtotal;
      delete data.tax;
      delete data.total;

      const updatedQuote = await quotesService.updateQuote(id, tenantId, data);
      if (!updatedQuote) return res.status(404).json({ error: 'Quote not found or permission denied' });
      
      return res.json(updatedQuote);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async deleteQuote(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      
      const result = await quotesService.deleteQuote(id, tenantId);
      if ((result as any).count === 0) return res.status(404).json({ error: 'Quote not found or permission denied' });

      return res.status(200).json({ message: 'Quote deleted successfully' });
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  // Quote Items Endpoints
  async addQuoteItem(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const quoteId = req.params.id as string;
      const itemData = req.body;
      
      if (!itemData.name || itemData.price === undefined || itemData.quantity === undefined) {
         return res.status(400).json({ error: 'Name, price, and quantity are required for item' });
      }

      const item = await quotesService.addQuoteItem(quoteId, tenantId, itemData);
      if (!item) return res.status(404).json({ error: 'Quote not found' });
      
      return res.status(201).json(item);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async updateQuoteItem(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const itemId = req.params.id as string;
      const itemData = req.body;
      
      const item = await quotesService.updateQuoteItem(itemId, tenantId, itemData);
      if (!item) return res.status(404).json({ error: 'Item not found' });
      
      return res.status(200).json(item);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async deleteQuoteItem(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const itemId = req.params.id as string;
      
      const result = await quotesService.deleteQuoteItem(itemId, tenantId);
      if (result.count === 0) return res.status(404).json({ error: 'Item not found' });
      
      return res.status(200).json({ message: 'Item deleted' });
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  }
};
