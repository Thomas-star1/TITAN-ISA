
# TITAN-ISA

Experimental processor architecture and instruction set simulator.

## Current version

TITAN-ISA v0.1 — reference simulator in Python.

## Initial features

- 16 general-purpose registers (R0–R15)
- 32-bit data values
- Arithmetic and logical instructions
- Simulated memory with LOAD and STORE
- Conditional and unconditional jumps
- Automated unit tests

## Project structure

- `sim/` — reference simulator
- `tests/` — automated tests
- `docs/` — architecture documentation

## Roadmap

1. Expand automated tests.
2. Define the 32-bit binary instruction encoding.
3. Build a reference assembler.
4. Develop a SystemVerilog implementation.
5. Validate the hardware against the simulator.

## Status

This is an experimental project. It does not yet implement a physical processor.
