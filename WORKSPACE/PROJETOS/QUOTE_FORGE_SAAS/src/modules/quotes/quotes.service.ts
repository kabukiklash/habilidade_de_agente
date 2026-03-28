import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const quotesService = {
  // Reusable core calculation method
  async recalculateTotals(quoteId: string, tenantId: string) {
    const items = await prisma.quoteItem.findMany({ where: { quoteId, quote: { tenantId } } });
    
    // Calculate subtotal
    const subtotal = items.reduce((sum, item) => sum + item.total, 0);
    // Future: Tax logic could be added here
    const tax = 0; 
    const total = subtotal + tax;

    await prisma.quote.update({
      where: { id: quoteId },
      data: { subtotal, tax, total }
    });
  },

  async createQuote(tenantId: string, data: { clientId: string, templateId?: string, quoteNumber: string, title: string, notes?: string, currency?: string }) {
    return prisma.quote.create({
      data: {
        tenantId,
        clientId: data.clientId,
        templateId: data.templateId,
        quoteNumber: data.quoteNumber,
        title: data.title,
        notes: data.notes,
        currency: data.currency || "BRL",
        status: "draft"
      },
      include: { items: true, tenant: true } // We query what we might need
    });
  },

  async createFromTemplate(tenantId: string, data: { clientId: string, templateId: string, title: string, quoteNumber: string }) {
    // 1. Validate template
    const template = await prisma.template.findFirst({
      where: { id: data.templateId, tenantId },
      include: { items: true }
    });

    if (!template) {
      throw new Error("Template not found or unauthorized");
    }

    // 2. Wrap in transaction to guarantee consistency
    return prisma.$transaction(async (tx) => {
      // Create empty quote
      const quote = await tx.quote.create({
        data: {
          tenantId,
          clientId: data.clientId,
          templateId: data.templateId,
          quoteNumber: data.quoteNumber,
          title: data.title,
          currency: "BRL", // Default
          status: "draft"
        }
      });

      // Insert snapshot of template items into QuoteItems
      if (template.items.length > 0) {
        await tx.quoteItem.createMany({
          data: template.items.map(item => ({
            quoteId: quote.id,
            name: item.name,
            description: item.description,
            price: item.price,
            quantity: item.quantityDefault,
            total: item.price * item.quantityDefault
          }))
        });
      }

      // Calculate totals inline for the transaction
      const subtotal = template.items.reduce((sum, item) => sum + (item.price * item.quantityDefault), 0);
      
      const completeQuote = await tx.quote.update({
        where: { id: quote.id },
        data: { subtotal, tax: 0, total: subtotal },
        include: { items: true }
      });

      return completeQuote;
    });
  },

  async getQuotes(tenantId: string) {
    return prisma.quote.findMany({
      where: { tenantId },
      orderBy: { createdAt: 'desc' },
      include: { items: true }
    });
  },

  async getQuoteById(id: string, tenantId: string) {
    return prisma.quote.findFirst({
      where: { id, tenantId },
      include: { items: true }
    });
  },

  async updateQuote(id: string, tenantId: string, data: any) {
    const existing = await prisma.quote.findFirst({ where: { id, tenantId } });
    if (!existing) return null;

    return prisma.quote.update({
      where: { id },
      data,
      include: { items: true }
    });
  },

  async deleteQuote(id: string, tenantId: string) {
    const existing = await prisma.quote.findFirst({ where: { id, tenantId } });
    if (!existing) return { count: 0 };

    return prisma.quote.deleteMany({
      where: { id, tenantId },
    });
  },

  // Quote Items logic
  async addQuoteItem(quoteId: string, tenantId: string, data: { name: string, description?: string, price: number, quantity: number }) {
    const existing = await prisma.quote.findFirst({ where: { id: quoteId, tenantId } });
    if (!existing) return null;

    const total = data.price * data.quantity;
    
    const item = await prisma.quoteItem.create({
      data: {
        ...data,
        quoteId,
        total
      }
    });

    await this.recalculateTotals(quoteId, tenantId);
    return item;
  },

  async updateQuoteItem(itemId: string, tenantId: string, data: { name?: string, description?: string, price?: number, quantity?: number }) {
    const existingItem = await prisma.quoteItem.findFirst({
      where: { id: itemId, quote: { tenantId } },
      include: { quote: true }
    });
    if (!existingItem) return null;

    const price = data.price ?? existingItem.price;
    const quantity = data.quantity ?? existingItem.quantity;
    const total = price * quantity;

    const updatedItem = await prisma.quoteItem.update({
      where: { id: itemId },
      data: { ...data, total }
    });

    await this.recalculateTotals(existingItem.quoteId, tenantId);
    return updatedItem;
  },

  async deleteQuoteItem(itemId: string, tenantId: string) {
    const existingItem = await prisma.quoteItem.findFirst({
      where: { id: itemId, quote: { tenantId } }
    });
    
    if (!existingItem) return { count: 0 };
    
    await prisma.quoteItem.delete({
      where: { id: itemId }
    });

    await this.recalculateTotals(existingItem.quoteId, tenantId);
    return { count: 1 };
  }
};
