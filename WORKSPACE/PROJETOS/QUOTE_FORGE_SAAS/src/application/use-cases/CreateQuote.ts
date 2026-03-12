import { DatabaseService } from "../../infrastructure/database/DatabaseService";
import { CalculateQuote } from "./CalculateQuote";
import { QuoteDomain } from "../../domain/entities/Interfaces";

/**
 * ID: CP-FORGE-APP-002
 * Caso de Uso: Criar Orçamento.
 */

export class CreateQuote {
  static async execute(tenantId: string, userId: string, payload: any): Promise<QuoteDomain> {
    const { clientData, items } = payload;

    return await DatabaseService.executeInTenantContext(tenantId, async (tx) => {
      let total = 0;
      const processedItems = [];

      for (const item of items) {
        // Buscar template
        const template = await tx.productTemplate.findUniqueOrThrow({
          where: { id: item.templateId }
        });

        // Calcular preço do item via Use Case
        const itemPrice = await CalculateQuote.execute(template as any, item.inputs);
        total += itemPrice;

        processedItems.push({
          productTemplateId: item.templateId,
          inputValues: item.inputs,
          calculatedPrice: itemPrice
        });
      }

      // Criar Orçamento no Banco
      const quote = await tx.quote.create({
        data: {
          tenantId,
          userId,
          clientData,
          totalPrice: total,
          status: 'draft',
          items: {
            create: processedItems
          }
        },
        include: { items: true }
      });

      return quote as any;
    });
  }
}
