import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { EstagioFunilEntity } from './estagio-funil.entity';

@Entity('leads')
export class LeadEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  nome: string;

  @Column()
  telefone: string;

  @Column({ nullable: true })
  email: string | null;

  @Column()
  origem: string;

  @Column('simple-array', { default: '' })
  tags: string;

  @Column({ type: 'int', default: 0 })
  score: number;

  @Column()
  estagioFunilId: string;

  @ManyToOne(() => EstagioFunilEntity)
  @JoinColumn({ name: 'estagioFunilId' })
  estagioFunil?: EstagioFunilEntity;

  @Column({ type: 'decimal', precision: 12, scale: 2, nullable: true })
  valorPotencial: number | null;

  @Column({ nullable: true })
  responsavelId: string | null;

  @Column()
  empresaId: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
