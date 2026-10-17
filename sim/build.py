
"""Exporta programas TITAN-ISA para arquivos binários."""

import argparse
import sys
from pathlib import Path

from sim.assembler import assemble


def build_file(source_path, output_path):
    """Monta o assembly e grava cada instrução em 4 bytes."""
    source_path = Path(source_path)
    output_path = Path(output_path)

    source = source_path.read_text(encoding="utf-8")
    program = assemble(source)

    binary = bytearray()

    for instruction in program:
        binary.extend(instruction.to_bytes(4, byteorder="little"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(binary)

    return len(program)


def main():
    parser = argparse.ArgumentParser(
        description="Gera arquivos binários da TITAN-ISA."
    )
    parser.add_argument("arquivo", type=Path, help="Arquivo .tasm de entrada")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Arquivo .bin de saída (opcional)",
    )
    args = parser.parse_args()

    output_path = args.output or Path("build") / f"{args.arquivo.stem}.bin"

    try:
        count = build_file(args.arquivo, output_path)
    except (OSError, ValueError, OverflowError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    print("=== TITAN-ISA: BUILD CONCLUÍDO ===")
    print(f"Entrada: {args.arquivo}")
    print(f"Saída: {output_path}")
    print(f"Instruções: {count}")
    print(f"Tamanho: {count * 4} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
