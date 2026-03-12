import { IsString, IsOptional, IsNumber, IsArray, IsEmail } from 'class-validator';

export class CreateLeadDto {
  @IsString()
  nome: string;

  @IsString()
  telefone: string;

  @IsOptional()
  @IsEmail()
  email?: string;

  @IsString()
  origem: string;

  @IsOptional()
  @IsArray()
  @IsString({ each: true })
  tags?: string[];

  @IsString()
  estagioFunilId: string;

  @IsOptional()
  @IsNumber()
  valorPotencial?: number;

  @IsOptional()
  @IsString()
  responsavelId?: string;

  @IsString()
  empresaId: string;
}
