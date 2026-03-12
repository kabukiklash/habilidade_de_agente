import { DatabaseService } from "../../infrastructure/database/DatabaseService";
import { SecurityService } from "../../infrastructure/security/SecurityService";

/**
 * ID: CP-FORGE-APP-004
 * Caso de Uso: Autenticar Usuário e Injetar Tenant.
 */

export class LoginUser {
  static async execute(email: string, password: string): Promise<{ token: string }> {
    const user = await DatabaseService.client.user.findUnique({
      where: { email },
      include: { tenant: true }
    });

    if (!user) throw new Error("Credenciais inválidas.");

    const isValid = await SecurityService.verifyPassword(password, user.passwordHash);
    if (!isValid) throw new Error("Credenciais inválidas.");

    const token = SecurityService.generateToken({
      userId: user.id,
      tenantId: user.tenantId,
      role: user.role
    });

    return { token };
  }
}
