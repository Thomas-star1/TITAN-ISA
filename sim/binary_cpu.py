
"""CPU binária para a TITAN-ISA v0.2."""

from sim.encoder import decode

WORD_MASK = 0xFFFFFFFF
DEFAULT_MEMORY_SIZE = 1 << 22  # 4 MiB


class BinaryCPU:
    """Executa instruções de 32 bits da TITAN-ISA v0.2."""

    def __init__(
        self,
        program,
        memory_size=DEFAULT_MEMORY_SIZE,
        trace=False,
    ):
        if not isinstance(memory_size, int) or isinstance(memory_size, bool):
            raise ValueError("memory_size deve ser um inteiro.")

        if memory_size <= 0 or memory_size % 4 != 0:
            raise ValueError("memory_size deve ser positivo e múltiplo de 4.")

        if not isinstance(trace, bool):
            raise ValueError("trace deve ser True ou False.")

        self.program = list(program)
        self.memory_size = memory_size
        self.registers = [0] * 16
        self.memory = {}
        self.pc = 0
        self.halted = False
        self.steps = 0

        self.trace_enabled = trace
        self.trace_log = []

        for index, word in enumerate(self.program):
            if (
                not isinstance(word, int)
                or isinstance(word, bool)
                or not 0 <= word <= WORD_MASK
            ):
                raise ValueError(
                    f"Palavra inválida na instrução {index}: {word!r}"
                )

    def read_reg(self, reg):
        """Lê um registrador. R0 sempre retorna zero."""
        if not isinstance(reg, int) or isinstance(reg, bool):
            raise ValueError("Registrador inválido.")

        if not 0 <= reg < 16:
            raise ValueError(f"Registrador inválido: R{reg}")

        if reg == 0:
            return 0

        return self.registers[reg]

    def write_reg(self, reg, value):
        """Escreve em um registrador, mantendo R0 igual a zero."""
        if not isinstance(reg, int) or isinstance(reg, bool):
            raise ValueError("Registrador inválido.")

        if not 0 <= reg < 16:
            raise ValueError(f"Registrador inválido: R{reg}")

        if reg != 0:
            self.registers[reg] = value & WORD_MASK

        self.registers[0] = 0

    def _validate_pc(self, pc):
        """Valida o PC como endereço de uma instrução existente."""
        if pc % 4 != 0:
            raise RuntimeError(f"PC desalinhado: {pc}")

        index = pc // 4

        if not 0 <= index < len(self.program):
            raise RuntimeError(f"Destino de execução inválido: PC={pc}")

    def _check_memory_address(self, address):
        """Valida endereço alinhado e dentro da memória simulada."""
        if not isinstance(address, int) or isinstance(address, bool):
            raise RuntimeError(f"Endereço de memória inválido: {address!r}")

        if address % 4 != 0:
            raise RuntimeError(
                f"Endereço de memória desalinhado: {address}"
            )

        if address < 0 or address + 4 > self.memory_size:
            raise RuntimeError(
                f"Endereço de memória fora dos limites: {address}"
            )

    def load_word(self, address):
        """Lê uma palavra de 32 bits; memória não inicializada vale zero."""
        self._check_memory_address(address)
        return self.memory.get(address, 0)

    def store_word(self, address, value):
        """Armazena uma palavra de 32 bits."""
        self._check_memory_address(address)
        self.memory[address] = value & WORD_MASK

    def _record_trace(
        self,
        pc_before,
        instruction,
        pc_after,
        registers_before,
    ):
        """Registra e imprime uma instrução quando o trace está ativado."""
        if not self.trace_enabled:
            return

        changes = []

        for reg in range(1, 16):
            old_value = registers_before[reg]
            new_value = self.registers[reg]

            if old_value != new_value:
                changes.append(
                    f"R{reg}: {old_value} -> {new_value}"
                )

        entry = {
            "step": self.steps,
            "pc_before": pc_before,
            "instruction": instruction,
            "pc_after": pc_after,
            "register_changes": changes,
        }

        self.trace_log.append(entry)

        changes_text = ", ".join(changes) if changes else "nenhum"

        print(
            f"[PASSO {self.steps:04}] "
            f"PC={pc_before:04} "
            f"{instruction} | "
            f"PC seguinte={pc_after:04} | "
            f"Registradores: {changes_text}"
        )

    def step(self):
        """Executa uma instrução. Retorna False quando a CPU para."""
        if self.halted:
            return False

        self._validate_pc(self.pc)

        current_pc = self.pc
        word = self.program[current_pc // 4]

        try:
            instruction = decode(word)
        except ValueError as exc:
            raise RuntimeError(
                f"Instrução inválida no PC={current_pc}: {exc}"
            ) from exc

        registers_before = self.registers.copy()
        name = instruction[0]
        next_pc = current_pc + 4

        if name == "MOVI":
            _, rd, immediate = instruction
            self.write_reg(rd, immediate)

        elif name in {"ADD", "SUB", "AND", "OR", "XOR"}:
            _, rd, rs, rt = instruction

            a = self.read_reg(rs)
            b = self.read_reg(rt)

            if name == "ADD":
                result = a + b
            elif name == "SUB":
                result = a - b
            elif name == "AND":
                result = a & b
            elif name == "OR":
                result = a | b
            else:
                result = a ^ b

            self.write_reg(rd, result)

        elif name == "LOAD":
            _, rd, address = instruction
            self.write_reg(rd, self.load_word(address))

        elif name == "STORE":
            _, rs, address = instruction
            self.store_word(address, self.read_reg(rs))

        elif name == "JMP":
            _, target_index = instruction
            next_pc = target_index * 4

        elif name in {"BEQ", "BNE"}:
            _, rs, rt, displacement = instruction

            equal = self.read_reg(rs) == self.read_reg(rt)
            should_branch = equal if name == "BEQ" else not equal

            if should_branch:
                next_pc = current_pc + 4 + displacement * 4

        elif name == "HALT":
            self.halted = True
            self.steps += 1
            self.registers[0] = 0

            self._record_trace(
                current_pc,
                instruction,
                self.pc,
                registers_before,
            )

            return False

        else:
            raise RuntimeError(
                f"Instrução não implementada: {name}"
            )

        # Saltos e desvios tomados precisam apontar
        # para uma instrução existente.
        if name == "JMP" or (
            name in {"BEQ", "BNE"}
            and next_pc != current_pc + 4
        ):
            self._validate_pc(next_pc)

        self.pc = next_pc
        self.steps += 1
        self.registers[0] = 0

        self._record_trace(
            current_pc,
            instruction,
            self.pc,
            registers_before,
        )

        return True

    def run(self, max_steps=10000):
        """Executa até HALT ou até atingir o limite de passos."""
        if (
            not isinstance(max_steps, int)
            or isinstance(max_steps, bool)
            or max_steps <= 0
        ):
            raise ValueError("max_steps deve ser um inteiro positivo.")

        initial_steps = self.steps

        while not self.halted:
            if self.steps - initial_steps >= max_steps:
                raise RuntimeError(
                    f"Limite de execução atingido: "
                    f"{max_steps} instruções."
                )

            self.step()

        return self
