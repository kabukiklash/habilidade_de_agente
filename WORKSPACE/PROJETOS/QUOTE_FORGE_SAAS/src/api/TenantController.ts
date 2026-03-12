import { Request, Response } from 'express';
import { LoginUser } from '../application/use-cases/LoginUser';

/**
 * ID: CP-FORGE-API-002
 * Controlador de Tenants/Usuários.
 */

export class TenantController {
  static async login(req: Request, res: Response) {
    try {
      const { email, password } = req.body;
      const result = await LoginUser.execute(email, password);
      return res.json(result);
    } catch (error: any) {
      return res.status(401).json({ error: error.message });
    }
  }
}
