import { Request, Response } from 'express';
import { templatesService } from './templates.service';

export const templatesController = {
  async createTemplate(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const { name, description, items } = req.body;
      
      if (!name) {
        return res.status(400).json({ error: 'Field "name" is required' });
      }

      const template = await templatesService.createTemplate(tenantId, { name, description, items });
      return res.status(201).json(template);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async getTemplates(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const templates = await templatesService.getTemplates(tenantId);
      return res.json(templates);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async getTemplate(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      
      const template = await templatesService.getTemplateById(id, tenantId);
      if (!template) {
        return res.status(404).json({ error: 'Template not found' });
      }
      return res.json(template);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async updateTemplate(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      const { name, description, items } = req.body;
      
      const updatedTemplate = await templatesService.updateTemplate(id, tenantId, { name, description, items });
      if (!updatedTemplate) {
        return res.status(404).json({ error: 'Template not found or permission denied' });
      }
      
      return res.json(updatedTemplate);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async deleteTemplate(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      
      const result = await templatesService.deleteTemplate(id, tenantId);
      // count might be undefined depending on how deleteMany resolves vs delete
      if ((result as any).count === 0) {
        return res.status(404).json({ error: 'Template not found or permission denied' });
      }

      return res.status(200).json({ message: 'Template deleted successfully' });
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  // Item Specific actions
  async addTemplateItem(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const templateId = req.params.id as string;
      const itemData = req.body;
      
      if (!itemData.name || itemData.price === undefined) {
         return res.status(400).json({ error: 'Name and price are required for item' });
      }

      const item = await templatesService.addTemplateItem(templateId, tenantId, itemData);
      if (!item) return res.status(404).json({ error: 'Template not found' });
      
      return res.status(201).json(item);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async deleteTemplateItem(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const itemId = req.params.id as string;
      
      const result = await templatesService.deleteTemplateItem(itemId, tenantId);
      if ((result as any).count === 0) return res.status(404).json({ error: 'Item not found' });
      
      return res.status(200).json({ message: 'Item deleted' });
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  }
};
