import { Injectable, OnModuleInit } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { EstagioFunilEntity } from '../../entities/estagio-funil.entity';

const EMPRESA_DEFAULT = 'empresa-default';

@Injectable()
export class EstagiosFunilService implements OnModuleInit {
  constructor(
    @InjectRepository(EstagioFunilEntity)
    private repo: Repository<EstagioFunilEntity>,
  ) {}

  async onModuleInit() {
    const count = await this.repo.count();
    if (count === 0) {
      await this.repo.save([
        { nome: 'Novo', ordem: 1, cor: '#94a3b8', empresaId: EMPRESA_DEFAULT, probabilidadeConversao: 10 },
        { nome: 'Qualificado', ordem: 2, cor: '#3b82f6', empresaId: EMPRESA_DEFAULT, probabilidadeConversao: 30 },
        { nome: 'Proposta', ordem: 3, cor: '#8b5cf6', empresaId: EMPRESA_DEFAULT, probabilidadeConversao: 50 },
        { nome: 'Negociação', ordem: 4, cor: '#f59e0b', empresaId: EMPRESA_DEFAULT, probabilidadeConversao: 70 },
        { nome: 'Fechado', ordem: 5, cor: '#22c55e', empresaId: EMPRESA_DEFAULT, probabilidadeConversao: 100 },
      ]);
    }
  }

  async findAll(empresaId?: string): Promise<EstagioFunilEntity[]> {
    return this.repo.find({
      where: { empresaId: empresaId ?? EMPRESA_DEFAULT },
      order: { ordem: 'ASC' },
    });
  }
}
