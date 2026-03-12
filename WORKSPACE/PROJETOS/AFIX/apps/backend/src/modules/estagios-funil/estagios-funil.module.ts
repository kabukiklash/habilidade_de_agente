import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { EstagioFunilEntity } from '../../entities/estagio-funil.entity';
import { EstagiosFunilController } from './estagios-funil.controller';
import { EstagiosFunilService } from './estagios-funil.service';

@Module({
  imports: [TypeOrmModule.forFeature([EstagioFunilEntity])],
  controllers: [EstagiosFunilController],
  providers: [EstagiosFunilService],
  exports: [EstagiosFunilService],
})
export class EstagiosFunilModule {}
