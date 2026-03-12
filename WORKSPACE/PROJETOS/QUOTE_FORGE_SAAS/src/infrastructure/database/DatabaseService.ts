import { PrismaClient } from '@prisma/client';

/**
 * ID: CP-FORGE-DB-001
 * Client Prisma Gerenciado: Injeta automaticamente o contexto de RLS.
 */

const prisma = new PrismaClient();

export class DatabaseService {
  /**
   * Executa uma operação dentro de um contexto de Tenant (RLS).
   * @param tenantId UUID do inquilino
   * @param work Callback com as operações do Prisma
   */
  static async executeInTenantContext<T>(tenantId: string, work: (tx: PrismaClient) => Promise<T>): Promise<T> {
    return await prisma.$transaction(async (tx) => {
      // Define a variável de sessão para o RLS do Postgres
      await tx.$executeRawUnsafe(`SET LOCAL app.tenant_id = '${tenantId}'`);
      return await work(tx as any);
    });
  }

  static get client() {
    return prisma;
  }
}
