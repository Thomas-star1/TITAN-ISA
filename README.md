
# TITAN-ISA

Experimental processor architecture, instruction set research, and reference simulator.

## Current version

TITAN-ISA v0.1 — experimental reference simulator in Python.

## Initial features

- 16 registers (R0–R15), with R0 hardwired to zero
- 32-bit data values
- Arithmetic and logical instructions
- Simulated memory with LOAD and STORE
- Conditional and unconditional jumps
- HALT instruction
- Automated unit tests

## Project structure

- `sim/` — reference simulator
- `tests/` — automated tests
- `docs/` — architecture documentation

## Roadmap

1. Expand automated tests.
2. Define the 32-bit binary instruction encoding.
3. Create an assembler and binary instruction decoder.
4. Develop a SystemVerilog implementation.
5. Validate the hardware implementation against the simulator.

## Current limitations

- Instructions are represented symbolically in Python.
- Memory is simulated in software.
- No physical processor or RTL implementation exists yet.
- No operating system support is implemented.

## Project status

This is an experimental architecture research project.
