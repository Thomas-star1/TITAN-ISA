
import unittest
from sim.titan import TitanCPU


class TestTitanCPU(unittest.TestCase):
    def test_add_and_store(self):
        cpu = TitanCPU()
        program = [
            ("MOVI", 1, 7),
            ("MOVI", 2, 5),
            ("ADD", 3, 1, 2),
            ("STORE", 3, 0),
            ("HALT",),
        ]

        cpu.run(program)

        self.assertEqual(cpu.read_reg(3), 12)
        self.assertEqual(cpu.memory[0], 12)
        self.assertTrue(cpu.halted)

    def test_r0_is_always_zero(self):
        cpu = TitanCPU()
        cpu.write_reg(0, 99)

        self.assertEqual(cpu.read_reg(0), 0)

    def test_32_bit_overflow(self):
        cpu = TitanCPU()
        cpu.write_reg(1, 0xFFFFFFFF)
        cpu.write_reg(2, 1)
        cpu.write_reg(3, cpu.read_reg(1) + cpu.read_reg(2))

        self.assertEqual(cpu.read_reg(3), 0)

    def test_invalid_instruction(self):
        cpu = TitanCPU()

        with self.assertRaises(ValueError):
            cpu.run([("INVALID",), ("HALT",)])


if __name__ == "__main__":
    unittest.main()
