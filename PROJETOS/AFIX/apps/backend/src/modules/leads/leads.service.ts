import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { LeadEntity } from '../../entities/lead.entity';
import { CreateLeadDto } from './dto/create-lead.dto';
import type { Lead } from '../../../../../packages/shared/src/entities/Lead';

@Injectable()
export class LeadsService {
  constructor(
    @InjectRepository(LeadEntity)
    private repo: Repository<LeadEntity>,
  ) {}

  private toLead(entity: LeadEntity): Lead {
    return {
      id: entity.id,
      nome: entity.nome,
      telefone: entity.telefone,
      email: entity.email ?? undefined,
      origem: entity.origem,
      tags: entity.tags ? entity.tags.split(',').filter(Boolean) : [],
      score: entity.score,
      estagioFunilId: entity.estagioFunilId,
      valorPotencial: entity.valorPotencial ? Number(entity.valorPotencial) : undefined,
      responsavelId: entity.responsavelId ?? undefined,
      empresaId: entity.empresaId,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
    };
  }

  async findAll(): Promise<Lead[]> {
    const entities = await this.repo.find({ order: { createdAt: 'DESC' } });
    return entities.map((e) => this.toLead(e));
  }

  async findById(id: string): Promise<Lead | null> {
    const entity = await this.repo.findOne({ where: { id } });
    return entity ? this.toLead(entity) : null;
  }

  async create(dto: CreateLeadDto): Promise<Lead> {
    const entity = this.repo.create({
      nome: dto.nome,
      telefone: dto.telefone,
      email: dto.email ?? null,
      origem: dto.origem,
      tags: (dto.tags ?? []).join(','),
      score: 0,
      estagioFunilId: dto.estagioFunilId,
      valorPotencial: dto.valorPotencial ?? null,
      responsavelId: dto.responsavelId ?? null,
      empresaId: dto.empresaId,
    });
    const saved = await this.repo.save(entity);
    return this.toLead(saved);
  }
}
