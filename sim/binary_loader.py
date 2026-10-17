
"""Carregador de arquivos binários da TITAN-ISA."""

from pathlib import Path


INSTRUCTION_SIZE = 4


def load_binary(path):
    """Carrega instruções de 32 bits em little-endian."""
    path = Path(path)
    data = path.read_bytes()

    if len(data) % INSTRUCTION_SIZE != 0:
        raise ValueError(
            "Arquivo binário inválido: o tamanho deve ser "
            "múltiplo de 4 bytes."
        )

    return [
        int.from_bytes(data[i:i + INSTRUCTION_SIZE], "little")
        for i in range(0, len(data), INSTRUCTION_SIZE)
    ]
