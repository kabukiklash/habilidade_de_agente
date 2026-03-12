import { Controller, Get, Post, Body, Param, NotFoundException } from '@nestjs/common';
import { LeadsService } from './leads.service';
import { CreateLeadDto } from './dto/create-lead.dto';

@Controller('leads')
export class LeadsController {
  constructor(private readonly leadsService: LeadsService) {}

  @Get()
  async list() {
    return this.leadsService.findAll();
  }

  @Get(':id')
  async get(@Param('id') id: string) {
    const lead = await this.leadsService.findById(id);
    if (!lead) throw new NotFoundException('Lead não encontrado');
    return lead;
  }

  @Post()
  async create(@Body() dto: CreateLeadDto) {
    return this.leadsService.create(dto);
  }
}
