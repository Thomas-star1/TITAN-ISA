
import unittest

from sim.encoder import encode, decode


class TestEncoder(unittest.TestCase):
    def test_round_trip_all_formats(self):
        instructions = [
            ("MOVI", 1, -7),
            ("ADD", 1, 2, 3),
            ("SUB", 4, 5, 6),
            ("AND", 1, 2, 3),
            ("OR", 1, 2, 3),
            ("XOR", 1, 2, 3),
            ("LOAD", 1, 16),
            ("STORE", 2, 20),
            ("JMP", 4),
            ("BEQ", 1, 2, -3),
            ("BNE", 3, 4, 5),
            ("HALT",),
        ]

        for instruction in instructions:
            with self.subTest(instruction=instruction):
                word = encode(instruction)
                self.assertGreaterEqual(word, 0)
                self.assertLessEqual(word, 0xFFFFFFFF)
                self.assertEqual(decode(word), instruction)
                self.assertEqual(encode(decode(word)), word)

    def test_immediate_limits(self):
        self.assertEqual(
            decode(encode(("MOVI", 1, -2097152))),
            ("MOVI", 1, -2097152),
        )
        self.assertEqual(
            decode(encode(("MOVI", 1, 2097151))),
            ("MOVI", 1, 2097151),
        )

    def test_branch_limits(self):
        for displacement in (-131072, 131071):
            instruction = ("BEQ", 1, 2, displacement)
            self.assertEqual(decode(encode(instruction)), instruction)

    def test_invalid_register(self):
        with self.assertRaises(ValueError):
            encode(("ADD", 16, 1, 2))

    def test_immediate_out_of_range(self):
        with self.assertRaises(ValueError):
            encode(("MOVI", 1, 2097152))

    def test_unaligned_memory_address(self):
        with self.assertRaises(ValueError):
            encode(("LOAD", 1, 3))

    def test_unknown_opcode(self):
        with self.assertRaises(ValueError):
            decode(0xFC000000)

    def test_reserved_bits_in_r_format(self):
        word = encode(("ADD", 1, 2, 3)) | 1
        with self.assertRaises(ValueError):
            decode(word)

    def test_halt_reserved_bits(self):
        word = encode(("HALT",)) | 1
        with self.assertRaises(ValueError):
            decode(word)


if __name__ == "__main__":
    unittest.main()
