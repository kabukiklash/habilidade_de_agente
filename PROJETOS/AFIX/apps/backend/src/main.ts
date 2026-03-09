import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );
  app.enableCors({
    origin: process.env.FRONTEND_URL ?? 'http://localhost:5174',
    credentials: true,
  });
  const port = process.env.PORT ?? 3002;
  await app.listen(port);
  console.log(`[Afix] Backend rodando em http://localhost:${port}`);
}

bootstrap().catch(console.error);
