# AfixControl: Escaneamento Profundo de Arquitetura de Classes

Este documento realiza a decomposição técnica das principais classes do sistema, explicando o funcionamento dos algoritmos e a lógica de governança de dados.

---

## 1. CalculadoraCore (`calculadora-core.php`)
O "Santo Graal" da precificação do sistema. Segue a versão **3.0.0-ISO**.

### 1.1 O Algoritmo de Cálculo (Passo a Passo)
1.  **Sanitização Decimal:** O método `parseDecimal` converte formatos brasileiros (`0,00`) para padrões computacionais (`0.00`), removendo símbolos monetários.
2.  **Cálculo de Custo Base:** 
    - Se o produto é por **m²**, calcula a área (`(L * A) / 1.000.000`).
    - Multiplica o valor base do produto pela área ou unidade.
3.  **Injeção de Adicionais (Processos):**
    - **Percentuais (%)**: Aplicados sobre o valor base.
    - **Fixos (und/m²)**: Somados ao total com base na quantidade ou área.
4.  **Fator de Quantidade (Volume):** Aplica multiplicadores baseados em faixas (ex: de 10 a 50 unidades, aplica X% de acréscimo ou desconto).
5.  **Margem de Lucro (Padrão Afix):** A margem de 100% é tratada como o **dobro do custo base**.
6.  **Imposto "Por Dentro":** O cálculo mais crítico. O imposto é aplicado dividindo o valor pelo complemento do imposto (`Valor / (1 - %)`), garantindo que a margem real não seja erodida pelo imposto.
7.  **Cálculo Físico:** Estima o peso (kg) e volume (cm³) com base na densidade do substrato.

---

## 2. Gestão de Layouts (`layouts.php` / `layouts_conversas.php`)
Sistema de colaboração entre o Comercial e o Setor de Arte.

### 2.1 Ciclo de Estados
- `Insert()`: Cria o registro inicial com briefing em JSON e anexos vetoriais (`.cdr`, `.ai`, `.eps`).
- `Sinalizar()`: Implementa um sistema de "Lock" visual. Quando um arte-finalista começa a trabalhar, o campo `layout_por` é preenchido, evitando que dois designers trabalhem na mesma peça.
- `Finalizar()`: Conclui o processo anexando o caminho do arquivo final aprovado.

---

## 3. Governança de Usuários (`usuarios.php`)
Implementa a camada de segurança **Sovereign Safety V2**.

### 3.1 Segurança de Query
O método `GetAll` utiliza um "Regex Militar" (Linha 76) para bloquear qualquer tentativa de SQL Injection em parâmetros dinâmicos de filtragem, permitindo apenas comandos `WHERE`, `ORDER BY` e `LIMIT` seguros.

### 3.2 Tokens de Integração
Gere dois níveis de tokens (`usuario_token_1` e `token_2`) usados primariamente para manter a conexão ativa com o gateway da **RD Station** sem expor a senha do usuário.

---

## 4. Integração VIPP (`vipp.php`)
Classe especialista em logística.

- **Função:** Serializa o objeto JSON de frete da proposta e o envia para o webservice da VIPP.
- **Payload:** Captura peso, dimensões calculadas na `CalculadoraCore` e dados de entrega do cliente para gerar a etiqueta de postagem em tempo real.

---
**Documento Gerado por Antigravity Sentry v3 - Escrutínio de Engenharia de Software.**
