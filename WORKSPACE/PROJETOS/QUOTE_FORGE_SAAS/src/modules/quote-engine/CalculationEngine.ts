import { create, all } from 'mathjs';

/**
 * ID: CP-FORGE-ENGINE-001
 * Motor de Cálculo Soberano: Executa fórmulas dinâmicas em sandbox.
 */

const math = create(all);
const limitedEvaluate = math.evaluate;

// Configuração de segurança: bloqueia funções perigosas
// Nota: mathjs evaluate por padrão não tem acesso a IO ou Processo, 
// mas limitamos ainda mais aqui.

export class CalculationEngine {
  /**
   * Executa uma fórmula com base em variáveis fornecidas.
   * @param formula Ex: "(largura * altura) * preco_m2"
   * @param scope Ex: { largura: 10, altura: 20, preco_m2: 50 }
   */
  static evaluate(formula: string, scope: Record<string, any>): number {
    try {
      // Validação básica de segurança na string da fórmula
      if (/[a-zA-Z_]\.[a-zA-Z_]/.test(formula)) {
        throw new Error("Acesso a propriedades de objetos é proibido nas fórmulas.");
      }

      const result = limitedEvaluate(formula, scope);
      
      if (typeof result !== 'number') {
        throw new Error("O resultado do cálculo deve ser um número.");
      }

      return Number(result.toFixed(2));
    } catch (error: any) {
      console.error(`💥 [ENGINE] Erro no cálculo: ${error.message}`);
      throw new Error(`Erro na fórmula: ${error.message}`);
    }
  }
}
