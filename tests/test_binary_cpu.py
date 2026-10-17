
import unittest

from sim.encoder import encode
from sim.binary_cpu import BinaryCPU


class TestBinaryCPU(unittest.TestCase):
    def test_arithmetic_and_memory(self):
        program = [
            encode(("MOVI", 1, 10)),
            encode(("MOVI", 2, 20)),
            encode(("ADD", 3, 1, 2)),
            encode(("STORE", 3, 0)),
            encode(("HALT",)),
        ]

        cpu = BinaryCPU(program).run()

        self.assertEqual(cpu.read_reg(3), 30)
        self.assertEqual(cpu.load_word(0), 30)
        self.assertTrue(cpu.halted)
        self.assertEqual(cpu.steps, 5)

    def test_r0_is_always_zero(self):
        program = [
            encode(("MOVI", 0, 123)),
            encode(("ADD", 1, 0, 0)),
            encode(("HALT",)),
        ]

        cpu = BinaryCPU(program).run()

        self.assertEqual(cpu.read_reg(0), 0)
        self.assertEqual(cpu.read_reg(1), 0)

    def test_conditional_branch(self):
        program = [
            encode(("MOVI", 1, 5)),
            encode(("MOVI", 2, 5)),
            encode(("BEQ", 1, 2, 1)),
            encode(("MOVI", 3, 99)),
            encode(("MOVI", 3, 7)),
            encode(("HALT",)),
        ]

        cpu = BinaryCPU(program).run()

        self.assertEqual(cpu.read_reg(3), 7)

    def test_unconditional_jump(self):
        program = [
            encode(("JMP", 2)),
            encode(("MOVI", 1, 99)),
            encode(("MOVI", 1, 7)),
            encode(("HALT",)),
        ]

        cpu = BinaryCPU(program).run()

        self.assertEqual(cpu.read_reg(1), 7)

    def test_load_and_store(self):
        program = [
            encode(("MOVI", 1, 1234)),
            encode(("STORE", 1, 4)),
            encode(("LOAD", 2, 4)),
            encode(("HALT",)),
        ]

        cpu = BinaryCPU(program).run()

        self.assertEqual(cpu.read_reg(2), 1234)

    def test_32_bit_overflow(self):
        program = [
            encode(("MOVI", 1, 2097151)),
            encode(("MOVI", 2, 1)),
            encode(("ADD", 3, 1, 2)),
            encode(("HALT",)),
        ]

        cpu = BinaryCPU(program).run()

        self.assertEqual(cpu.read_reg(3), 2097152)

    def test_invalid_jump_target(self):
        program = [
            encode(("JMP", 10)),
            encode(("HALT",)),
        ]

        cpu = BinaryCPU(program)

        with self.assertRaises(RuntimeError):
            cpu.step()

    def test_memory_out_of_bounds(self):
        program = [
            encode(("LOAD", 1, 16)),
            encode(("HALT",)),
        ]

        cpu = BinaryCPU(program, memory_size=16)

        with self.assertRaises(RuntimeError):
            cpu.step()

    def test_invalid_binary_instruction(self):
        cpu = BinaryCPU([0xFC000000])

        with self.assertRaises(RuntimeError):
            cpu.step()

    def test_execution_limit(self):
        program = [
            encode(("JMP", 0)),
        ]

        cpu = BinaryCPU(program)

        with self.assertRaises(RuntimeError):
            cpu.run(max_steps=5)

    def test_invalid_pc_after_last_instruction(self):
        cpu = BinaryCPU([encode(("MOVI", 1, 1))])
        cpu.step()

        with self.assertRaises(RuntimeError):
            cpu.step()


if __name__ == "__main__":
    unittest.main()
