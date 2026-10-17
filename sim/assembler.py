
"""Assembler da TITAN-ISA v0.3 com suporte a labels."""

import re

from sim.encoder import encode


REGISTER_PATTERN = re.compile(r"R([0-9]|1[0-5])$", re.IGNORECASE)
LABEL_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
LABEL_PREFIX_PATTERN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):")


def parse_register(token):
    """Converte R0..R15 em número de registrador."""
    match = REGISTER_PATTERN.fullmatch(token.strip())

    if not match:
        raise ValueError(f"Registrador inválido: {token}")

    return int(match.group(1))


def parse_number(token):
    """Aceita números decimais e hexadecimais."""
    try:
        return int(token.strip(), 0)
    except ValueError as exc:
        raise ValueError(f"Número inválido: {token}") from exc


def assemble_instruction(line):
    """Converte uma instrução sem labels em uma palavra de máquina."""
    line = line.split("#", 1)[0].strip()

    if not line:
        return None

    parts = line.replace(",", " ").split()
    mnemonic = parts[0].upper()
    args = parts[1:]

    formats = {
        "MOVI": (2, lambda a: (
            "MOVI", parse_register(a[0]), parse_number(a[1])
        )),
        "ADD": (3, lambda a: (
            "ADD", parse_register(a[0]),
            parse_register(a[1]), parse_register(a[2])
        )),
        "SUB": (3, lambda a: (
            "SUB", parse_register(a[0]),
            parse_register(a[1]), parse_register(a[2])
        )),
        "AND": (3, lambda a: (
            "AND", parse_register(a[0]),
            parse_register(a[1]), parse_register(a[2])
        )),
        "OR": (3, lambda a: (
            "OR", parse_register(a[0]),
            parse_register(a[1]), parse_register(a[2])
        )),
        "XOR": (3, lambda a: (
            "XOR", parse_register(a[0]),
            parse_register(a[1]), parse_register(a[2])
        )),
        "LOAD": (2, lambda a: (
            "LOAD", parse_register(a[0]), parse_number(a[1])
        )),
        "STORE": (2, lambda a: (
            "STORE", parse_register(a[0]), parse_number(a[1])
        )),
        "JMP": (1, lambda a: (
            "JMP", parse_number(a[0])
        )),
        "BEQ": (3, lambda a: (
            "BEQ", parse_register(a[0]),
            parse_register(a[1]), parse_number(a[2])
        )),
        "BNE": (3, lambda a: (
            "BNE", parse_register(a[0]),
            parse_register(a[1]), parse_number(a[2])
        )),
        "HALT": (0, lambda a: ("HALT",)),
    }

    if mnemonic not in formats:
        raise ValueError(f"Instrução desconhecida: {mnemonic}")

    expected_count, make_instruction = formats[mnemonic]

    if len(args) != expected_count:
        raise ValueError(
            f"{mnemonic} espera {expected_count} argumento(s), "
            f"mas recebeu {len(args)}."
        )

    try:
        return encode(make_instruction(args))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Erro na instrução '{line}': {exc}") from exc


def _remove_labels(line):
    """Extrai labels no início da linha e retorna o código restante."""
    remaining = line.split("#", 1)[0].strip()
    found = []

    while remaining:
        match = LABEL_PREFIX_PATTERN.match(remaining)
        if not match:
            break

        found.append(match.group(1))
        remaining = remaining[match.end():].strip()

    return found, remaining


def assemble(source):
    """Monta um programa em duas passagens, resolvendo labels."""
    if not isinstance(source, str):
        raise TypeError("O programa deve ser fornecido como texto.")

    labels = {}
    instructions = []

    # Primeira passagem: descobrir o índice de cada label.
    for line_number, original_line in enumerate(
        source.splitlines(), start=1
    ):
        names, line = _remove_labels(original_line)

        for name in names:
            if name in labels:
                raise ValueError(
                    f"Linha {line_number}: label duplicado: {name}"
                )

            labels[name] = len(instructions)

        if line:
            instructions.append((line_number, line))

    # Segunda passagem: resolver destinos e codificar instruções.
    program = []

    for instruction_index, (line_number, line) in enumerate(instructions):
        parts = line.replace(",", " ").split()
        mnemonic = parts[0].upper()
        args = parts[1:]

        if mnemonic in ("JMP", "BEQ", "BNE") and args:
            target = args[-1]

            if LABEL_PATTERN.fullmatch(target):
                if target not in labels:
                    raise ValueError(
                        f"Linha {line_number}: "
                        f"label inexistente: {target}"
                    )

                target_index = labels[target]

                if mnemonic == "JMP":
                    args[-1] = str(target_index)
                else:
                    # BEQ/BNE contam o deslocamento a partir
                    # da instrução seguinte.
                    displacement = target_index - (instruction_index + 1)
                    args[-1] = str(displacement)

                line = " ".join([parts[0], *args])

        try:
            word = assemble_instruction(line)
        except ValueError as exc:
            raise ValueError(f"Linha {line_number}: {exc}") from exc

        if word is not None:
            program.append(word)

    return program
