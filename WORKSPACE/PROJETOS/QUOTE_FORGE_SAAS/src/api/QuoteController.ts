import { Request, Response } from 'express';
import { CreateQuote } from '../application/use-cases/CreateQuote';
import { ApproveQuote } from '../application/use-cases/ApproveQuote';

/**
 * ID: CP-FORGE-API-001
 * Controlador de Orçamentos: Expõe as funcionalidades do SaaS.
 */

export class QuoteController {
  static async create(req: Request, res: Response) {
    try {
      const { tenantId, userId } = (req as any).user;
      const quote = await CreateQuote.execute(tenantId, userId, req.body);
      return res.status(201).json(quote);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  }

  static async approve(req: Request, res: Response) {
    try {
      const { tenantId } = (req as any).user;
      const { id } = req.params;
      if (!id) throw new Error("ID do orçamento é obrigatório.");
      const quote = await ApproveQuote.execute(tenantId, id as string);
      return res.json(quote);
    } catch (error: any) {
      return res.status(400).json({ error: error.message });
    }
  }
}
