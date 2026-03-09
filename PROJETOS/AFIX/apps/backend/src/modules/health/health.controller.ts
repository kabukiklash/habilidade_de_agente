import { Controller, Get } from '@nestjs/common';

@Controller('health')
export class HealthController {
  @Get()
  check() {
    return {
      status: 'ok',
      service: 'afix-backend',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
    };
  }
}
