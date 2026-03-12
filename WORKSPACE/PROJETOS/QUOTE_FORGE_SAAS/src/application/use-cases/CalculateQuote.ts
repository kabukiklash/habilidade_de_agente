import { CalculationEngine } from "../../modules/quote-engine/CalculationEngine";
import { ProductTemplateDomain } from "../../domain/entities/Interfaces";

/**
 * ID: CP-FORGE-APP-001
 * Caso de Uso: Calcular Orçamento.
 * Orquestra a lógica de produto e o motor de cálculo.
 */

export class CalculateQuote {
  static async execute(template: ProductTemplateDomain, inputs: Record<string, any>): Promise<number> {
    console.log(`🧮 [APP] Calculando item para template: ${template.name}`);
    
    // 1. Validar se todos os campos obrigatórios estão presentes
    for (const field of template.fields) {
      if (inputs[field.name] === undefined) {
        throw new Error(`Campo obrigatório ausente: ${field.name}`);
      }
    }

    // 2. Executar Motor de Cálculo (T11 Engine)
    return CalculationEngine.evaluate(template.formulaLogic, inputs);
  }
}
