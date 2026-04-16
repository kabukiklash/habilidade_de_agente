# Mapeamento do Fluxo de Cálculo de Custos

Este documento detalha como o sistema AfixControl processa os custos e valores finais de venda, baseado na análise estática do código ([ajax/calculos.php](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/WORKSPACE/PROJETOS/AfixcontrolAfixgraf/ajax/calculos.php) e [classes/produtos.php](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/WORKSPACE/PROJETOS/AfixcontrolAfixgraf/classes/produtos.php)).

## 1. Fluxo de Sequência da Calculadora

```mermaid
sequenceDiagram
    participant U as Usuário (Interface)
    participant C as ajax/calculos.php
    participant P as Classe Produto
    participant DB as Banco de Dados
    participant ISO as CalculadoraCore (Shadow Mode)

    U->>C: Parâmetros (Produto, Largura, Altura, Quantidade, Margem)
    C->>DB: Busca Produto e Substrato correspondente
    DB-->>C: Retorna dados (produto_valor, substrato_peso, espessura)
    
    rect rgb(240, 240, 240)
        Note right of C: Cálculo de Área (m²)
        C->>C: area = (altura * largura) / 1.000.000
    end

    alt Cálculo Normal
        C->>C: Calcula Custo Base (Unitário ou m²)
        loop Para cada Processo Extra
            C->>DB: Busca Custo do Processo
            C->>C: Soma Adicionais (%, und ou m²)
        end
        C->>C: Aplica Fatores de Quantidade (Descontos/Acréscimos)
        C->>C: Aplica Margem (%)
        C->>C: Aplica Imposto (produto_imposto)
    else Cálculo Reverso (Valor Manual)
        C->>C: Identifica Valor Unitário Definido
        C->>C: Calcula Margem/Lucro real baseado no Custo Base
    end

    Note right of C: Auditoria Silenciosa (ISO Validation)
    C->>ISO: Valida com Motor ISO (CalculadoraCore)
    ISO-->>C: Retorna ISO Validated: true/false

    C-->>U: Retorna JSON (Total, Margem, Lucro, Detalhes HTML)
```

## 2. Pontos de Melhoria Identificados

1.  **Redundância de Código**: O cálculo de processos é repetido em múltiplos arquivos ([calculos.php](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/WORKSPACE/PROJETOS/AfixcontrolAfixgraf/ajax/calculos.php), [produtos.php](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/WORKSPACE/PROJETOS/AfixcontrolAfixgraf/ajax/produtos.php), `novo-orcamento.js`). Recomenda-se centralizar 100% no `CalculadoraCore`.
2.  **Arredondamento**: Existem divergências sutis de arredondamento (`round` vs `number_format`) entre o frontend e o backend que podem acumular centavos em tiragens grandes.
3.  **Peso/Volume**: O cálculo de peso em [calculos.php](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/WORKSPACE/PROJETOS/AfixcontrolAfixgraf/ajax/calculos.php) é simplificado. Poderia considerar o peso específico de cada componente se integrado à telemetria de produção.
