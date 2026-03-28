import { Request, Response } from 'express';
import { clientsService } from './clients.service';

export const clientsController = {
  async createClient(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const { name, email, phone, company } = req.body;
      
      if (!name) {
        return res.status(400).json({ error: 'Field "name" is required' });
      }

      const client = await clientsService.createClient(tenantId, { name, email, phone, company });
      return res.status(201).json(client);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async getClients(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const clients = await clientsService.getClients(tenantId);
      return res.json(clients);
    } catch (error: any) {
      console.error(error);
      return res.status(400).json({ error: error.message });
    }
  },

  async getClient(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      const client = await clientsService.getClientById(id, tenantId);
      
      if (!client) {
        return res.status(404).json({ error: 'Client not found' });
      }
      return res.json(client);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async updateClient(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      const { name, email, phone, company } = req.body;
      
      const result = await clientsService.updateClient(id, tenantId, { name, email, phone, company });
      if (result.count === 0) {
        return res.status(404).json({ error: 'Client not found or you do not have permission' });
      }
      
      // Fetch updated client
      const updatedClient = await clientsService.getClientById(id, tenantId);
      return res.json(updatedClient);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  },

  async deleteClient(req: Request, res: Response): Promise<Response> {
    try {
      const { tenantId } = (req as any).user;
      const id = req.params.id as string;
      
      const result = await clientsService.deleteClient(id, tenantId);
      if (result.count === 0) {
        return res.status(404).json({ error: 'Client not found or you do not have permission' });
      }

      return res.status(200).json({ message: 'Client deleted successfully' });
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  }
};
