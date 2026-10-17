
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from sim.encoder import encode
from sim.debugger import run_debugger


class TestDebugger(unittest.TestCase):
    def run_commands(self, program, commands):
        output = io.StringIO()

        with patch("builtins.input", side_effect=commands):
            with redirect_stdout(output):
                cpu = run_debugger(program)

        return cpu, output.getvalue()

    def test_step_executes_one_instruction(self):
        program = [
            encode(("MOVI", 1, 7)),
            encode(("HALT",)),
        ]

        cpu, output = self.run_commands(program, ["s", "q"])

        self.assertEqual(cpu.steps, 1)
        self.assertEqual(cpu.read_reg(1), 7)
        self.assertFalse(cpu.halted)
        self.assertIn("PC=0000", output)

    def test_register_command_shows_registers(self):
        program = [
            encode(("MOVI", 1, 7)),
            encode(("HALT",)),
        ]

        _, output = self.run_commands(program, ["s", "r", "q"])

        self.assertIn("Registradores:", output)
        self.assertIn("R1  =          7", output)
        self.assertIn("PC: 4", output)

    def test_continue_runs_until_halt(self):
        program = [
            encode(("MOVI", 1, 7)),
            encode(("HALT",)),
        ]

        cpu, output = self.run_commands(program, ["c", "q"])

        self.assertTrue(cpu.halted)
        self.assertEqual(cpu.read_reg(1), 7)
        self.assertEqual(cpu.steps, 2)
        self.assertIn("Programa finalizado com HALT.", output)

    def test_memory_command_reads_stored_value(self):
        program = [
            encode(("MOVI", 1, 123)),
            encode(("STORE", 1, 0)),
            encode(("HALT",)),
        ]

        _, output = self.run_commands(program, ["c", "m 0", "q"])

        self.assertIn("Memória[0] = 123 (0x0000007B)", output)

    def test_trace_command_shows_execution_history(self):
        program = [
            encode(("MOVI", 1, 7)),
            encode(("HALT",)),
        ]

        _, output = self.run_commands(program, ["s", "t", "q"])

        self.assertIn("Passo 0001", output)
        self.assertIn("Alterações: R1: 0 -> 7", output)

    def test_unknown_command_shows_help(self):
        program = [encode(("HALT",))]

        _, output = self.run_commands(program, ["xyz", "q"])

        self.assertIn("Comando desconhecido", output)


if __name__ == "__main__":
    unittest.main()
