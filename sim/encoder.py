
"""Codificador e decodificador binário da TITAN-ISA v0.2."""

OPCODES = {
    "MOVI": 0x01,
    "ADD":  0x02,
    "SUB":  0x03,
    "AND":  0x04,
    "OR":   0x05,
    "XOR":  0x06,
    "LOAD": 0x07,
    "STORE": 0x08,
    "JMP":  0x09,
    "BEQ":  0x0A,
    "BNE":  0x0B,
    "HALT": 0x0C,
}

NAMES_BY_OPCODE = {value: key for key, value in OPCODES.items()}

REG_BITS = 4
REG_MAX = 15

I_BITS = 22
I_MIN = -(1 << (I_BITS - 1))
I_MAX = (1 << (I_BITS - 1)) - 1

ADDRESS_BITS = 22
ADDRESS_MAX = (1 << ADDRESS_BITS) - 1

J_BITS = 26
J_MAX = (1 << J_BITS) - 1

B_BITS = 18
B_MIN = -(1 << (B_BITS - 1))
B_MAX = (1 << (B_BITS - 1)) - 1

WORD_MASK = 0xFFFFFFFF


def _check_register(reg):
    if not isinstance(reg, int) or isinstance(reg, bool):
        raise ValueError("Registrador deve ser um inteiro.")
    if not 0 <= reg <= REG_MAX:
        raise ValueError(f"Registrador inválido: R{reg}")


def _check_range(value, minimum, maximum, field):
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{field} deve ser um inteiro.")
    if not minimum <= value <= maximum:
        raise ValueError(
            f"{field} fora do intervalo permitido: "
            f"{minimum} a {maximum}."
        )


def _signed_decode(value, bits):
    sign_bit = 1 << (bits - 1)
    if value & sign_bit:
        return value - (1 << bits)
    return value


def encode(instruction):
    """Codifica uma tupla simbólica em uma palavra de 32 bits.

    Exemplos:
        ("ADD", 1, 2, 3)
        ("MOVI", 1, -7)
        ("LOAD", 1, 16)
        ("STORE", 2, 20)
        ("JMP", 4)
        ("BEQ", 1, 2, -3)
        ("HALT",)
    """
    if not isinstance(instruction, (tuple, list)) or not instruction:
        raise ValueError("A instrução deve ser uma tupla ou lista não vazia.")

    name = instruction[0]
    if not isinstance(name, str):
        raise ValueError("O nome da instrução deve ser texto.")

    name = name.upper()
    if name not in OPCODES:
        raise ValueError(f"Instrução desconhecida: {name}")

    args = instruction[1:]
    opcode = OPCODES[name] << 26

    if name in {"ADD", "SUB", "AND", "OR", "XOR"}:
        if len(args) != 3:
            raise ValueError(f"{name} exige rd, rs e rt.")
        rd, rs, rt = args
        for reg in (rd, rs, rt):
            _check_register(reg)
        return opcode | (rd << 22) | (rs << 18) | (rt << 14)

    if name == "MOVI":
        if len(args) != 2:
            raise ValueError("MOVI exige rd e imediato.")
        rd, immediate = args
        _check_register(rd)
        _check_range(immediate, I_MIN, I_MAX, "Imediato")
        return opcode | (rd << 22) | (immediate & ((1 << I_BITS) - 1))

    if name in {"LOAD", "STORE"}:
        if len(args) != 2:
            raise ValueError(f"{name} exige registrador e endereço.")
        reg, address = args
        _check_register(reg)
        _check_range(address, 0, ADDRESS_MAX, "Endereço")
        if address % 4 != 0:
            raise ValueError("O endereço deve ser múltiplo de 4.")
        return opcode | (reg << 22) | address

    if name == "JMP":
        if len(args) != 1:
            raise ValueError("JMP exige um índice de instrução.")
        index = args[0]
        _check_range(index, 0, J_MAX, "Índice de destino")
        return opcode | index

    if name in {"BEQ", "BNE"}:
        if len(args) != 3:
            raise ValueError(f"{name} exige rs, rt e deslocamento.")
        rs, rt, displacement = args
        _check_register(rs)
        _check_register(rt)
        _check_range(displacement, B_MIN, B_MAX, "Deslocamento")
        return (
            opcode
            | (rs << 22)
            | (rt << 18)
            | (displacement & ((1 << B_BITS) - 1))
        )

    if name == "HALT":
        if args:
            raise ValueError("HALT não recebe operandos.")
        return opcode

    raise ValueError(f"Codificação não implementada: {name}")


def decode(word):
    """Decodifica uma palavra de 32 bits em uma tupla simbólica."""
    _check_range(word, 0, WORD_MASK, "Palavra de instrução")

    opcode = (word >> 26) & 0x3F
    name = NAMES_BY_OPCODE.get(opcode)
    if name is None:
        raise ValueError(f"Opcode desconhecido: 0x{opcode:02X}")

    if name in {"ADD", "SUB", "AND", "OR", "XOR"}:
        if word & 0x3FFF:
            raise ValueError("Bits reservados do formato R devem ser zero.")
        rd = (word >> 22) & 0xF
        rs = (word >> 18) & 0xF
        rt = (word >> 14) & 0xF
        return (name, rd, rs, rt)

    if name == "MOVI":
        rd = (word >> 22) & 0xF
        immediate = _signed_decode(word & ((1 << I_BITS) - 1), I_BITS)
        return (name, rd, immediate)

    if name in {"LOAD", "STORE"}:
        reg = (word >> 22) & 0xF
        address = word & ((1 << ADDRESS_BITS) - 1)
        if address % 4 != 0:
            raise ValueError("O endereço de memória deve ser múltiplo de 4.")
        return (name, reg, address)

    if name == "JMP":
        return (name, word & ((1 << J_BITS) - 1))

    if name in {"BEQ", "BNE"}:
        rs = (word >> 22) & 0xF
        rt = (word >> 18) & 0xF
        displacement = _signed_decode(
            word & ((1 << B_BITS) - 1), B_BITS
        )
        return (name, rs, rt, displacement)

    if name == "HALT":
        if word & ((1 << 26) - 1):
            raise ValueError("Bits reservados de HALT devem ser zero.")
        return ("HALT",)

    raise ValueError(f"Decodificação não implementada: {name}")
