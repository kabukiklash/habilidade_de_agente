import { Request, Response, NextFunction } from 'express';
import { SecurityService } from '../infrastructure/security/SecurityService';

/**
 * ID: CP-FORGE-API-MID-001
 * Middleware de Autenticação: Garante o isolamento por Tenant ID.
 */

export const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  // Ignora rotas públicas dentro do roteador /api
  if (req.path === '/auth/login' || req.path === '/health') {
    return next();
  }

  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: "Token de acesso ausente ou inválido." });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = SecurityService.verifyToken(token);
    
    // Injeta o usuário decodificado na request
    (req as any).user = {
      userId: decoded.userId,
      tenantId: decoded.tenantId,
      role: decoded.role
    };

    next();
  } catch (error: any) {
    return res.status(401).json({ error: error.message });
  }
};
