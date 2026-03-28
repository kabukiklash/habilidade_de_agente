import { PrismaClient, Prisma } from '@prisma/client';

const prisma = new PrismaClient();

export const templatesService = {
  async createTemplate(tenantId: string, data: { name: string; description?: string; items?: any[] }) {
    const { items, ...templateData } = data;
    
    return prisma.template.create({
      data: {
        ...templateData,
        tenantId,
        items: items?.length ? {
          create: items.map(item => ({
            name: item.name,
            description: item.description,
            price: item.price,
            quantityDefault: item.quantityDefault || 1
          }))
        } : undefined
      },
      include: { items: true },
    });
  },

  async getTemplates(tenantId: string) {
    return prisma.template.findMany({
      where: { tenantId },
      include: { items: true },
      orderBy: { createdAt: 'desc' },
    });
  },

  async getTemplateById(id: string, tenantId: string) {
    return prisma.template.findFirst({
      where: { id, tenantId },
      include: { items: true },
    });
  },

  async updateTemplate(id: string, tenantId: string, data: { name?: string; description?: string; items?: any[] }) {
    // First, verify template ownership
    const existing = await prisma.template.findFirst({ where: { id, tenantId } });
    if (!existing) return null;

    const { items, ...updateData } = data;

    // Use a transaction if updating items
    return prisma.$transaction(async (tx) => {
      if (items !== undefined) {
        // Simple approach: delete all old items, create new ones. 
        // A more advanced approach would diff them, but this is an MVP.
        await tx.templateItem.deleteMany({
          where: { templateId: id }
        });
        
        if (items.length > 0) {
          await tx.templateItem.createMany({
            data: items.map(item => ({
              templateId: id,
              name: item.name,
              description: item.description,
              price: item.price,
              quantityDefault: item.quantityDefault || 1
            }))
          });
        }
      }

      return tx.template.update({
        where: { id },
        data: updateData,
        include: { items: true }
      });
    });
  },

  async deleteTemplate(id: string, tenantId: string) {
    // Check ownership first
    const existing = await prisma.template.findFirst({ where: { id, tenantId } });
    if (!existing) return { count: 0 };
    
    // Items are deleted via onDelete: Cascade
    return prisma.template.deleteMany({
      where: { id, tenantId },
    });
  },

  // Independent Item Management if needed later
  async addTemplateItem(templateId: string, tenantId: string, data: any) {
    const existing = await prisma.template.findFirst({ where: { id: templateId, tenantId } });
    if (!existing) return null;

    return prisma.templateItem.create({
      data: {
        ...data,
        templateId
      }
    });
  },

  async deleteTemplateItem(itemId: string, tenantId: string) {
    // Check if the item's template belongs to the tenant
    const existing = await prisma.templateItem.findFirst({
      where: { id: itemId, template: { tenantId } }
    });
    
    if (!existing) return { count: 0 };
    
    return prisma.templateItem.delete({
      where: { id: itemId }
    });
  }
};
