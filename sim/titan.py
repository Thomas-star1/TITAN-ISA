
MASK32 = 0xFFFFFFFF


class TitanCPU:
    def __init__(self):
        self.regs = [0] * 16
        self.pc = 0
        self.memory = {}
        self.halted = False

    def read_reg(self, index):
        if not 0 <= index < 16:
            raise ValueError(f"Registrador inválido: R{index}")
        return 0 if index == 0 else self.regs[index]

    def write_reg(self, index, value):
        if not 0 <= index < 16:
            raise ValueError(f"Registrador inválido: R{index}")
        if index != 0:
            self.regs[index] = value & MASK32

    def run(self, program, max_steps=1000):
        steps = 0

        while not self.halted:
            if steps >= max_steps:
                raise RuntimeError("Limite de instruções atingido")
            if self.pc % 4 != 0:
                raise ValueError("PC desalinhado")

            index = self.pc // 4
            if not 0 <= index < len(program):
                raise ValueError(f"PC fora do programa: {self.pc}")

            instruction = program[index]
            self.pc += 4
            steps += 1
            op = instruction[0]

            if op == "MOVI":
                _, rd, value = instruction
                self.write_reg(rd, value)

            elif op in ("ADD", "SUB", "AND", "OR", "XOR"):
                _, rd, rs, rt = instruction
                a = self.read_reg(rs)
                b = self.read_reg(rt)

                if op == "ADD":
                    result = a + b
                elif op == "SUB":
                    result = a - b
                elif op == "AND":
                    result = a & b
                elif op == "OR":
                    result = a | b
                else:
                    result = a ^ b

                self.write_reg(rd, result)

            elif op == "LOAD":
                _, rd, address = instruction
                if address < 0 or address % 4:
                    raise ValueError("Endereço LOAD inválido")
                self.write_reg(rd, self.memory.get(address, 0))

            elif op == "STORE":
                _, rs, address = instruction
                if address < 0 or address % 4:
                    raise ValueError("Endereço STORE inválido")
                self.memory[address] = self.read_reg(rs)

            elif op == "JMP":
                _, target = instruction
                self.pc = target

            elif op in ("BEQ", "BNE"):
                _, rs, rt, target = instruction
                equal = self.read_reg(rs) == self.read_reg(rt)
                should_branch = equal if op == "BEQ" else not equal
                if should_branch:
                    self.pc = target

            elif op == "HALT":
                self.halted = True

            else:
                raise ValueError(f"Instrução inválida: {op}")

        return steps


if __name__ == "__main__":
    program = [
        ("MOVI", 1, 7),
        ("MOVI", 2, 5),
        ("ADD", 3, 1, 2),
        ("STORE", 3, 0),
        ("HALT",),
    ]

    cpu = TitanCPU()
    steps = cpu.run(program)

    print("TITAN-ISA v0.1")
    print("R1 =", cpu.read_reg(1))
    print("R2 =", cpu.read_reg(2))
    print("R3 =", cpu.read_reg(3))
    print("MEM[0] =", cpu.memory[0])
    print("Instruções executadas =", steps)
    print("Estado =", "HALT" if cpu.halted else "RUNNING")
