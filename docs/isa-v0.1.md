
# TITAN-ISA v0.1

## Objetivo

Projeto experimental de arquitetura de conjunto de instruções (ISA),
com simulador de referência em Python e evolução futura para hardware.

## Especificações iniciais

- Instruções: representação simbólica no simulador.
- Largura planejada das instruções: 32 bits.
- Registradores: 16, de R0 a R15.
- R0: sempre retorna zero.
- Dados: inteiros de 32 bits sem sinal no modelo inicial.
- PC: contador de programa com avanço de 4 bytes.
- Memória: simulada por endereços alinhados em 4 bytes.

## Instruções implementadas

- MOVI: carrega um valor imediato.
- ADD, SUB: soma e subtração.
- AND, OR, XOR: operações lógicas.
- LOAD, STORE: leitura e escrita na memória simulada.
- JMP: salto incondicional.
- BEQ, BNE: saltos condicionais.
- HALT: encerra a execução.

## Limitações conhecidas

- A codificação binária das instruções ainda não foi implementada.
- A memória é simulada em Python.
- Não existe ainda implementação em hardware.
- A arquitetura ainda não possui suporte a sistema operacional.

## Próximas etapas

1. Expandir os testes.
2. Definir a codificação binária de cada instrução.
3. Especificar os limites dos imediatos e endereços.
4. Criar programas de exemplo.
5. Desenvolver uma implementação RTL em SystemVerilog.
