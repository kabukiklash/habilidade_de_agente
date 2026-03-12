import { Controller, Get } from '@nestjs/common';
import { EstagiosFunilService } from './estagios-funil.service';

@Controller('estagios-funil')
export class EstagiosFunilController {
  constructor(private readonly service: EstagiosFunilService) {}

  @Get()
  list() {
    return this.service.findAll();
  }
}
