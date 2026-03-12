import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function seed() {
  console.log('🌱 Seeding database for validation...');

  // 1. Criar Tenant ACME
  const acme = await prisma.tenant.upsert({
    where: { id: 'acme-id-001' }, // Dummy ID for reference in tests
    update: {},
    create: {
      id: 'acme-id-001',
      name: 'ACME Comunicação Visual'
    }
  });

  // 2. Criar Admin ACME
  const salt = await bcrypt.genSalt(10);
  const passwordHash = await bcrypt.hash('admin123', salt);

  await prisma.user.upsert({
    where: { email: 'admin@acme.com' },
    update: { passwordHash },
    create: {
      tenantId: acme.id,
      email: 'admin@acme.com',
      passwordHash,
      role: 'admin'
    }
  });

  // 3. Criar Tenant GLOBEX (para Teste de RLS)
  const globex = await prisma.tenant.upsert({
    where: { id: 'globex-id-002' },
    update: {},
    create: {
      id: 'globex-id-002',
      name: 'GLOBEX Corporation'
    }
  });

  await prisma.user.upsert({
    where: { email: 'spy@globex.com' },
    update: { passwordHash },
    create: {
      tenantId: globex.id,
      email: 'spy@globex.com',
      passwordHash,
      role: 'admin'
    }
  });

  console.log('✅ Seed complete.');
  await prisma.$disconnect();
}

seed().catch(err => {
  console.error(err);
  process.exit(1);
});
