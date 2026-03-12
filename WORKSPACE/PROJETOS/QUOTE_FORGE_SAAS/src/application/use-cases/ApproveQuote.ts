import { DatabaseService } from "../../infrastructure/database/DatabaseService";

/**
 * ID: CP-FORGE-APP-003
 * Caso de Uso: Aprovar Orçamento (Snapshot Imutável).
 */

export class ApproveQuote {
  static async execute(tenantId: string, quoteId: string): Promise<any> {
    return await DatabaseService.executeInTenantContext(tenantId, async (tx) => {
      // 1. Buscar orçamento atual
      const quote = await tx.quote.findUniqueOrThrow({
        where: { id: quoteId },
        include: { items: true }
      });

      if (quote.status === 'approved') {
        throw new Error("Este orçamento já está aprovado.");
      }

      // 2. Marcar como aprovado e gerar log imutável
      const updatedQuote = await tx.quote.update({
        where: { id: quoteId },
        data: { status: 'approved' }
      });

      // 3. Registrar Log de Auditoria (Append-only)
      await tx.auditLog.create({
        data: {
          tenantId,
          userId: quote.userId,
          action: 'QUOTE_APPROVED',
          entityType: 'QUOTE',
          entityId: quoteId,
          newValue: { status: 'approved', totalPrice: quote.totalPrice }
        }
      });

      console.log(`✅ [APP] Orçamento ${quoteId} aprovado e selado.`);
      return updatedQuote;
    });
  }
}
