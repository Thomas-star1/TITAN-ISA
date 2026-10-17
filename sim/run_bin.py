
"""Executa arquivos binários da TITAN-ISA."""

import argparse
import sys
from pathlib import Path

from sim.binary_cpu import BinaryCPU
from sim.binary_loader import load_binary


def main():
    parser = argparse.ArgumentParser(
        description="Executa arquivos binários da TITAN-ISA."
    )
    parser.add_argument(
        "arquivo",
        type=Path,
        help="Caminho para o arquivo .bin",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="Limite de instruções executadas",
    )
    args = parser.parse_args()

    if args.max_steps < 1:
        parser.error("--max-steps deve ser maior que zero")

    try:
        program = load_binary(args.arquivo)
        cpu = BinaryCPU(program)
        cpu.run(max_steps=args.max_steps)

        print("\n=== TITAN-ISA: EXECUÇÃO BINÁRIA ===")
        print(f"Arquivo: {args.arquivo}")
        print(f"Instruções carregadas: {len(program)}")
        print(f"Instruções executadas: {cpu.steps}")
        print(f"PC final: {cpu.pc}")
        print("\nRegistradores:")

        for register in range(16):
            print(f"R{register:<2} = {cpu.read_reg(register)}")

    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
