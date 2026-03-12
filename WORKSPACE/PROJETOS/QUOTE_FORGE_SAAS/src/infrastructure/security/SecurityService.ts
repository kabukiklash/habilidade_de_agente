import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';

/**
 * ID: CP-FORGE-SEC-001
 * Serviço de Segurança: Autenticação e Criptografia Soberana.
 */

const JWT_SECRET = process.env.JWT_SECRET || 'SOVEREIGN_FALLBACK_SECRET';

export class SecurityService {
  /**
   * Gera um hash seguro para senhas.
   */
  static async hashPassword(password: string): Promise<string> {
    const salt = await bcrypt.genSalt(12);
    return await bcrypt.hash(password, salt);
  }

  /**
   * Verifica se a senha corresponde ao hash.
   */
  static async verifyPassword(password: string, hash: string): Promise<boolean> {
    return await bcrypt.compare(password, hash);
  }

  /**
   * Cria um token JWT contendo o Tenant ID.
   */
  static generateToken(payload: { userId: string, tenantId: string, role: string }): string {
    return jwt.sign(payload, JWT_SECRET, { expiresIn: '8h' });
  }

  /**
   * Valida um token JWT.
   */
  static verifyToken(token: string): any {
    try {
      return jwt.verify(token, JWT_SECRET);
    } catch {
      throw new Error("Token inválido ou expirado.");
    }
  }
}
