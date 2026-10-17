# TITAN-ISA

**Experimental processor architecture, instruction set research, and reference simulator.**

TITAN-ISA is an experimental instruction set architecture (ISA) project developed in Python. It includes a reference simulator, a 32-bit instruction encoder and decoder, an assembler with label resolution, binary export, binary execution, and an interactive debugger.

The project explores processor architecture, instruction encoding, assembly language, simulation, and a possible future hardware implementation.

## Current status

- ISA specification: v0.2
- Project development milestone: preparing version 0.3
- Language: Python
- Platform tested: Windows with Python 3.12
- Automated tests: 63 passing
- Hardware implementation: not yet available

Run the test suite to verify the current result:

```bash
python -m unittest discover -s tests -v
```

## Features

- 16 general-purpose registers (`R0`-`R15`)
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
- Optional CPU execution trace
- Interactive binary debugger
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
│   ├── run_bin.py
│   └── debugger.py
├── tests/
│   ├── test_assembler.py
│   ├── test_binary_cpu.py
│   ├── test_binary_loader.py
│   ├── test_build.py
│   ├── test_encoder.py
│   ├── test_titan.py
│   └── test_debugger.py
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

The simulator and test suite currently use Python's standard library.

## Getting started

Clone the repository:

```bash
git clone https://github.com/Thomas-star1/TITAN-ISA.git
cd TITAN-ISA
```

Run an assembly source program:

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

## Interactive debugger

Start the debugger with a compiled binary:

```bash
python -m sim.debugger build/contagem.bin
```

Available commands:

| Command | Description |
|---|---|
| `s` | Execute one instruction |
| `r` | Display the program counter and registers |
| `m N` | Read a word from data memory at address `N` |
| `t` | Display the recorded execution trace |
| `c` | Continue until `HALT` or the execution limit |
| `q` | Exit the debugger |

Example session:

```text
TITAN> s
TITAN> r
TITAN> t
TITAN> c
TITAN> q
```

The debugger enables tracing so that each executed instruction and its register changes can be inspected. The `m N` command reads simulated data memory, not the encoded instruction stream.

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

The program can be assembled, exported to a binary file, and executed through the binary runner or interactive debugger.

## Development and testing

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

The suite covers the assembler, instruction encoding, binary CPU, binary exporter, binary loader, original reference simulator, and interactive debugger.

## Roadmap

1. Keep the ISA specification and implementation aligned.
2. Expand automated tests, including debugger error cases.
3. Improve memory inspection and program-loading capabilities.
4. Document instruction formats and execution semantics.
5. Explore a SystemVerilog implementation.
6. Validate a future hardware implementation against the software simulator.

## Current limitations

- This is an experimental ISA and software simulator, not a commercial processor.
- Memory is simulated in software.
- There is no physical processor or completed RTL implementation.
- No operating system or application binary interface is implemented.
- The binary format is a project-specific instruction stream, not a standard executable format.
- The debugger currently operates on compiled binary programs.

## Project status

TITAN-ISA is an ongoing experimental architecture research project. Features and specifications may change as the ISA evolves.

Contributions, testing, and technical feedback are welcome.
