
import unittest

from sim.assembler import assemble, assemble_instruction
from sim.encoder import encode


class TestAssembler(unittest.TestCase):

    def test_movi(self):
        self.assertEqual(
            assemble_instruction("MOVI R1, 10"),
            encode(("MOVI", 1, 10)),
        )

    def test_arithmetic_instructions(self):
        for name in ("ADD", "SUB", "AND", "OR", "XOR"):
            with self.subTest(instruction=name):
                self.assertEqual(
                    assemble_instruction(f"{name} R3, R1, R2"),
                    encode((name, 3, 1, 2)),
                )

    def test_load_and_store(self):
        self.assertEqual(
            assemble_instruction("LOAD R1, 16"),
            encode(("LOAD", 1, 16)),
        )
        self.assertEqual(
            assemble_instruction("STORE R2, 20"),
            encode(("STORE", 2, 20)),
        )

    def test_jumps_and_branches(self):
        self.assertEqual(
            assemble_instruction("JMP 4"),
            encode(("JMP", 4)),
        )
        self.assertEqual(
            assemble_instruction("BEQ R1, R2, -3"),
            encode(("BEQ", 1, 2, -3)),
        )
        self.assertEqual(
            assemble_instruction("BNE R1, R2, 2"),
            encode(("BNE", 1, 2, 2)),
        )

    def test_halt(self):
        self.assertEqual(
            assemble_instruction("HALT"),
            encode(("HALT",)),
        )

    def test_case_insensitive(self):
        self.assertEqual(
            assemble_instruction("movi r1, 10"),
            encode(("MOVI", 1, 10)),
        )

    def test_comments_and_blank_lines(self):
        source = """
        # Programa de teste

        MOVI R1, 10  # carrega 10
        HALT
        """
        self.assertEqual(
            assemble(source),
            [encode(("MOVI", 1, 10)), encode(("HALT",))],
        )

    def test_empty_program(self):
        self.assertEqual(assemble(""), [])

    def test_invalid_register(self):
        with self.assertRaises(ValueError):
            assemble_instruction("MOVI R16, 10")

    def test_unknown_instruction(self):
        with self.assertRaises(ValueError):
            assemble_instruction("INVALID R1")

    def test_wrong_argument_count(self):
        with self.assertRaises(ValueError):
            assemble_instruction("ADD R1, R2")

    def test_invalid_number(self):
        with self.assertRaises(ValueError):
            assemble_instruction("MOVI R1, abc")

    def test_unaligned_memory_address(self):
        with self.assertRaises(ValueError):
            assemble_instruction("LOAD R1, 3")

    def test_error_includes_line_number(self):
        with self.assertRaisesRegex(ValueError, "Linha 2"):
            assemble("MOVI R1, 10\nINVALID R2")

    def test_non_text_program(self):
        with self.assertRaises(TypeError):
            assemble(None)


if __name__ == "__main__":
    unittest.main()
