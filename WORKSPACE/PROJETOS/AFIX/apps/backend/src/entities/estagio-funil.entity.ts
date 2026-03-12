import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('estagios_funil')
export class EstagioFunilEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  nome: string;

  @Column({ type: 'int', default: 0 })
  ordem: number;

  @Column({ default: '#2563eb' })
  cor: string;

  @Column()
  empresaId: string;

  @Column({ type: 'int', default: 0 })
  probabilidadeConversao: number;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
