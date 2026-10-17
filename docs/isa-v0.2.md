# TITAN-ISA v0.2 — Especificação da Arquitetura

**Projeto:** TITAN-ISA  
**Versão:** 0.2  
**Status:** Em desenvolvimento  
**Formato de instrução:** 32 bits  
**Endianness:** Little-endian

## 1. Objetivo

A TITAN-ISA é uma arquitetura experimental de conjunto de instruções (ISA), desenvolvida para servir de base a um simulador de processador e, futuramente, a possíveis implementações em hardware.

A versão 0.2 formaliza a codificação binária das instruções, os registradores, a memória, os desvios de fluxo e os requisitos de validação.

## 2. Modelo do processador

- 16 registradores de uso geral: R0 a R15.
- Cada registrador possui 32 bits.
- R0 é permanentemente igual a zero.
- Os resultados aritméticos são mantidos em 32 bits.
- O contador de programa (PC) contém um endereço de byte.
- Cada instrução possui 32 bits (4 bytes).
- O PC inicial é zero.
- A execução normal avança o PC em 4 bytes.
- A memória de dados é endereçada por byte.
- Os acessos de 32 bits devem usar endereços múltiplos de 4.
- A capacidade efetiva da memória é definida pela implementação.

## 3. Tabela de instruções

| Opcode | Hexadecimal | Instrução | Formato |
|---|---|---|---|
| 000001 | 0x01 | MOVI | I |
| 000010 | 0x02 | ADD | R |
| 000011 | 0x03 | SUB | R |
| 000100 | 0x04 | AND | R |
| 000101 | 0x05 | OR | R |
| 000110 | 0x06 | XOR | R |
| 000111 | 0x07 | LOAD | M |
| 001000 | 0x08 | STORE | M |
| 001001 | 0x09 | JMP | J |
| 001010 | 0x0A | BEQ | B |
| 001011 | 0x0B | BNE | B |
| 001100 | 0x0C | HALT | H |

Opcodes não listados são inválidos nesta versão.

## 4. Formatos e posições dos campos

Os bits são numerados de 31 (mais significativo) a 0 (menos significativo).

### 4.1. Formato R — operações entre registradores

| Bits | Tamanho | Campo |
|---|---:|---|
| 31–26 | 6 | Opcode |
| 25–22 | 4 | rd |
| 21–18 | 4 | rs |
| 17–14 | 4 | rt |
| 13–0 | 14 | Reservado, deve ser zero |

Operações:

- `ADD rd, rs, rt`: rd = rs + rt.
- `SUB rd, rs, rt`: rd = rs - rt.
- `AND rd, rs, rt`: rd = rs AND rt.
- `OR rd, rs, rt`: rd = rs OR rt.
- `XOR rd, rs, rt`: rd = rs XOR rt.

Todos os resultados são limitados a 32 bits. Escritas em R0 são descartadas.

### 4.2. Formato I — imediato

| Bits | Tamanho | Campo |
|---|---:|---|
| 31–26 | 6 | Opcode |
| 25–22 | 4 | rd |
| 21–0 | 22 | Imediato com sinal |

Instrução:

`MOVI rd, imediato`

O imediato é um inteiro com sinal de 22 bits em complemento de dois, com intervalo de -2.097.152 a 2.097.151.

O valor é estendido com sinal para 32 bits antes de ser escrito em rd. Uma escrita em R0 não altera seu valor.

### 4.3. Formato M — acesso à memória

| Bits | Tamanho | Campo |
|---|---:|---|
| 31–26 | 6 | Opcode |
| 25–22 | 4 | Registrador |
| 21–0 | 22 | Endereço de byte sem sinal |

Instruções:

- `LOAD rd, endereço`: carrega 32 bits da memória para rd.
- `STORE rs, endereço`: grava 32 bits de rs na memória.

O endereço codificado varia de 0 a 4.194.303 bytes. Para acessos de 32 bits, deve ser múltiplo de 4.

Endereços fora da memória implementada geram erro. LOAD com destino R0 pode ser executado, mas o valor carregado é descartado.

### 4.4. Formato J — salto incondicional

| Bits | Tamanho | Campo |
|---|---:|---|
| 31–26 | 6 | Opcode |
| 25–0 | 26 | Índice da instrução de destino |

Instrução:

`JMP índice`

O destino é um índice de instrução, não um endereço de byte.

O endereço de destino é calculado por:

`PC_destino = índice × 4`

O destino deve corresponder a uma instrução existente e válida no programa em execução.

### 4.5. Formato B — desvio condicional

| Bits | Tamanho | Campo |
|---|---:|---|
| 31–26 | 6 | Opcode |
| 25–22 | 4 | rs |
| 21–18 | 4 | rt |
| 17–0 | 18 | Deslocamento com sinal |

Instruções:

- `BEQ rs, rt, deslocamento`: desvia se rs for igual a rt.
- `BNE rs, rt, deslocamento`: desvia se rs for diferente de rt.

O deslocamento é um inteiro com sinal de 18 bits, em complemento de dois, medido em instruções.

O destino é calculado por:

`PC_destino = PC_atual + 4 + (deslocamento × 4)`

O intervalo do deslocamento é de -131.072 a 131.071 instruções.

Se a condição for falsa, a execução continua na próxima instrução. Se for verdadeira, o destino deve ser válido e alinhado a 4 bytes.

### 4.6. Formato H — parada

| Bits | Tamanho | Campo |
|---|---:|---|
| 31–26 | 6 | Opcode |
| 25–0 | 26 | Reservado, deve ser zero |

Instrução:

`HALT`

Encerra a execução e define o estado do processador como HALT.

## 5. Memória e representação de dados

- A memória é endereçada por byte.
- Os valores carregados e armazenados têm 32 bits.
- A ordem dos bytes é little-endian.
- Um acesso de 32 bits exige alinhamento de 4 bytes.
- A implementação deve detectar acessos inválidos.
- A memória de instruções e a memória de dados podem ser separadas pelo simulador.
- A capacidade e os limites efetivos de cada memória devem ser documentados pela implementação.

## 6. Regras de execução

1. O processador começa com PC igual a zero.
2. O simulador busca a instrução correspondente ao PC.
3. A instrução é validada e decodificada.
4. Os operandos são lidos.
5. A operação é executada.
6. Os resultados são gravados quando aplicável.
7. O PC é atualizado conforme a instrução.
8. A execução termina em HALT ou quando ocorre um erro definido pela implementação.

O simulador deve possuir um limite configurável de instruções executadas para evitar execução indefinida causada por laços infinitos.

## 7. Codificador e decodificador

O projeto deverá implementar funções capazes de:

- Codificar instruções simbólicas em palavras de 32 bits.
- Decodificar palavras de 32 bits em instruções simbólicas.
- Validar opcodes e campos reservados.
- Validar os intervalos dos imediatos e deslocamentos.
- Rejeitar registradores fora do intervalo de R0 a R15.
- Rejeitar instruções malformadas.
- Preservar os valores sem sinal da palavra de instrução durante a codificação.

Para instruções válidas, a codificação e a decodificação devem ser consistentes: codificar uma instrução, decodificá-la e codificá-la novamente deve produzir a mesma palavra de 32 bits.

## 8. Erros e condições inválidas

O simulador deve detectar, de forma previsível:

- Opcode desconhecido.
- Campos reservados diferentes de zero.
- Imediatos fora do intervalo permitido.
- Deslocamentos fora do intervalo permitido.
- Registradores inválidos.
- Endereços de memória desalinhados.
- Acessos fora dos limites da memória.
- Destinos de salto inválidos.
- Busca de instrução fora dos limites do programa.
- Excesso do limite de execução configurado.

Erros devem apresentar informações úteis para diagnóstico, incluindo a instrução ou o endereço envolvido quando possível.

## 9. Requisitos de testes

A suíte automatizada deverá verificar:

1. Todas as instruções válidas.
2. Operações aritméticas e lógicas.
3. Comportamento permanente de R0.
4. Limitação dos resultados a 32 bits.
5. Valores imediatos positivos, negativos e limites.
6. Cálculo dos destinos de JMP, BEQ e BNE.
7. Acessos LOAD e STORE.
8. Alinhamento e limites de memória.
9. Rejeição de opcodes desconhecidos.
10. Rejeição de campos reservados inválidos.
11. Consistência entre codificador e decodificador.
12. Encerramento correto por HALT.
13. Tratamento do limite de instruções executadas.

Todos os testes devem ser executáveis localmente e repetíveis.

## 10. Compatibilidade e evolução

A versão 0.2 formaliza a representação binária, mas não exige que todos os recursos sejam implementados de uma só vez.

O simulador existente deverá continuar funcionando enquanto as mudanças forem introduzidas incrementalmente. Alterações incompatíveis devem ser documentadas.

Recursos futuros poderão incluir:

- Registradores especiais.
- Instruções de deslocamento de bits.
- Comparações adicionais.
- Interrupções e exceções.
- Modos de privilégio.
- Interface de depuração.
- Montador de linguagem assembly.
- Formato de programa binário executável.
- Implementação em hardware.

## 11. Critério de conclusão

A especificação v0.2 será considerada implementada quando os formatos binários estiverem documentados, o codificador e o decodificador estiverem testados, as instruções definidas funcionarem no simulador e a suíte automatizada passar.

**Fim da especificação TITAN-ISA v0.2.**