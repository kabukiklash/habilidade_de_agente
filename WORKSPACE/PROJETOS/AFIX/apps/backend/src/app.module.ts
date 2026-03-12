import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { HealthModule } from './modules/health/health.module';
import { LeadsModule } from './modules/leads/leads.module';
import { EstagiosFunilModule } from './modules/estagios-funil/estagios-funil.module';
import { LeadEntity } from './entities/lead.entity';
import { EstagioFunilEntity } from './entities/estagio-funil.entity';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST ?? 'localhost',
      port: parseInt(process.env.DB_PORT ?? '15432', 10),
      username: process.env.DB_USER ?? 'afix',
      password: process.env.DB_PASSWORD ?? 'afix_dev',
      database: process.env.DB_NAME ?? 'afix',
      entities: [LeadEntity, EstagioFunilEntity],
      synchronize: true,
    }),
    HealthModule,
    EstagiosFunilModule,
    LeadsModule,
  ],
})
export class AppModule {}
