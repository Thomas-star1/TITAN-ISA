# TITAN-ISA

**Experimental processor architecture, instruction set research, and reference simulator.**

TITAN-ISA is an experimental instruction set architecture (ISA) project developed in Python. It includes a reference simulator, a 32-bit instruction encoder and decoder, an assembler with label resolution, binary export, and direct execution of binary programs.

The project aims to explore processor architecture, instruction encoding, assembly language, simulation, and future hardware implementation.

## Current status

- ISA specification: v0.2
- Language: Python
- Automated tests: 55 passing in the latest local test run
- Platform tested: Windows with Python 3.12
- Hardware implementation: not yet available

## Features

- 16 general-purpose registers (`R0`–`R15`)
- `R0` is hardwired to zero
- 32-bit data values
- Arithmetic and logical instructions
- Simulated memory with `LOAD` and `STORE`
- Unconditional jumps and conditional branches
- Labels in assembly programs
- 32-bit instruction encoding and decoding
- Assembly source parsing and validation
- Export to little-endian binary files
- Direct loading and execution of `.bin` programs
- Configurable instruction execution limit
- Automated unit tests

## Instruction set

The current ISA defines the following instructions:

| Instruction | Purpose |
|---|---|
| `MOVI` | Load an immediate value into a register |
| `ADD` | Add two register values |
| `SUB` | Subtract register values |
| `AND` | Bitwise AND |
| `OR` | Bitwise OR |
| `XOR` | Bitwise XOR |
| `LOAD` | Load data from simulated memory |
| `STORE` | Store data in simulated memory |
| `JMP` | Unconditional jump |
| `BEQ` | Branch if equal |
| `BNE` | Branch if not equal |
| `HALT` | Stop execution |

See `docs/isa-v0.1.md` and `docs/isa-v0.2.md` for the architecture specifications.

## Project structure

```text
TITAN-ISA/
├── sim/
│   ├── titan.py
│   ├── encoder.py
│   ├── binary_cpu.py
│   ├── assembler.py
│   ├── run.py
│   ├── build.py
│   ├── binary_loader.py
│   └── run_bin.py
├── tests/
├── programas/
│   ├── somar.tasm
│   └── contagem.tasm
├── docs/
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12 or a compatible Python version
- Git, if you want to clone the repository

The project currently uses Python's standard library for its simulator and test suite.

## Getting started

Clone the repository:

```bash
git clone https://github.com/Thomas-star1/TITAN-ISA.git
cd TITAN-ISA
```

Run a source program:

```bash
python -m sim.run programas/contagem.tasm
```

Build a binary file:

```bash
python -m sim.build programas/contagem.tasm
```

By default, the binary is written to `build/contagem.bin`.

Run the compiled binary:

```bash
python -m sim.run_bin build/contagem.bin
```

Run the automated test suite:

```bash
python -m unittest discover -v
```

## Example program

The following program adds one to `R1` five times:

```asm
MOVI R1, 0
MOVI R2, 1
MOVI R3, 5

repetir:
ADD R1, R1, R2
SUB R3, R3, R2
BNE R3, R0, repetir
HALT
```

Expected final register values:

- `R1 = 5`
- `R2 = 1`
- `R3 = 0`

The example has been assembled, exported to a 28-byte binary file, and executed through the binary runner.

## Development and testing

Run the complete test suite after making changes:

```bash
python -m unittest discover -v
```

The tests cover the assembler, instruction encoding, binary CPU, binary exporter, binary loader, and original reference simulator.

## Roadmap

1. Improve ISA documentation and validation.
2. Expand assembler and binary execution tests.
3. Add debugging and execution tracing.
4. Improve memory and program-loading capabilities.
5. Explore a SystemVerilog implementation.
6. Validate a future hardware implementation against the software simulator.

## Current limitations

- This is an experimental ISA and simulator, not a commercial processor.
- Memory is simulated in software.
- There is no physical processor or completed RTL implementation.
- No operating system or application binary interface is implemented.
- The binary format is a project-specific instruction stream, not a standard executable format.

## Project status

TITAN-ISA is an ongoing experimental architecture research project. Features and specifications may change as the ISA evolves.

Contributions, testing, and technical feedback are welcome.