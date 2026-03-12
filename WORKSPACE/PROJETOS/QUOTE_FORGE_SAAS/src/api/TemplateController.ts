import { Request, Response } from 'express';
import { DatabaseService } from '../infrastructure/database/DatabaseService';

/**
 * ID: CP-FORGE-API-003
 * Controlador de Templates: CRUD de modelos de produto.
 */

export class TemplateController {
  static async create(req: Request, res: Response) {
    try {
      const { tenantId } = (req as any).user;
      const { name, fields, formulaLogic } = req.body;

      const template = await DatabaseService.executeInTenantContext(tenantId, async (tx) => {
        return await tx.productTemplate.create({
          data: {
            tenantId,
            name,
            fields,
            formulaLogic
          }
        });
      });

      return res.status(201).json(template);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  }

  static async list(req: Request, res: Response) {
    try {
      const { tenantId } = (req as any).user;
      
      const templates = await DatabaseService.executeInTenantContext(tenantId, async (tx) => {
        return await tx.productTemplate.findMany();
      });

      return res.json(templates);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  }
}
