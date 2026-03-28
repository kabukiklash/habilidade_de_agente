import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const clientsService = {
  async createClient(tenantId: string, data: any) {
    return prisma.client.create({
      data: {
        ...data,
        tenantId,
      },
    });
  },

  async getClients(tenantId: string) {
    return prisma.client.findMany({
      where: { tenantId },
      orderBy: { createdAt: 'desc' },
    });
  },

  async getClientById(id: string, tenantId: string) {
    return prisma.client.findFirst({
      where: { id, tenantId },
    });
  },

  async updateClient(id: string, tenantId: string, data: any) {
    // We use updateMany to safely enforce the tenantId condition
    return prisma.client.updateMany({
      where: { id, tenantId },
      data,
    });
  },

  async deleteClient(id: string, tenantId: string) {
    // We use deleteMany to safely enforce the tenantId condition
    return prisma.client.deleteMany({
      where: { id, tenantId },
    });
  }
};
