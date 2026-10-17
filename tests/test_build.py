
"""Testes do exportador binário da TITAN-ISA."""

import tempfile
import unittest
from pathlib import Path

from sim.assembler import assemble
from sim.build import build_file


class TestBuild(unittest.TestCase):
    def test_exporta_programa_como_binario(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pasta = Path(temp_dir)
            origem = pasta / "programa.tasm"
            destino = pasta / "programa.bin"

            origem.write_text("MOVI R1, 5\nHALT\n", encoding="utf-8")

            quantidade = build_file(origem, destino)

            programa = assemble("MOVI R1, 5\nHALT\n")
            esperado = b"".join(
                instrucao.to_bytes(4, byteorder="little")
                for instrucao in programa
            )

            self.assertEqual(quantidade, 2)
            self.assertEqual(destino.read_bytes(), esperado)
            self.assertEqual(destino.stat().st_size, 8)

    def test_cria_pasta_de_saida(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pasta = Path(temp_dir)
            origem = pasta / "programa.tasm"
            destino = pasta / "nova_pasta" / "programa.bin"

            origem.write_text("HALT\n", encoding="utf-8")

            build_file(origem, destino)

            self.assertTrue(destino.is_file())
            self.assertEqual(destino.stat().st_size, 4)

    def test_programa_vazio(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pasta = Path(temp_dir)
            origem = pasta / "vazio.tasm"
            destino = pasta / "vazio.bin"

            origem.write_text("", encoding="utf-8")

            quantidade = build_file(origem, destino)

            self.assertEqual(quantidade, 0)
            self.assertEqual(destino.read_bytes(), b"")

    def test_arquivo_de_entrada_inexistente(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pasta = Path(temp_dir)

            with self.assertRaises(FileNotFoundError):
                build_file(
                    pasta / "inexistente.tasm",
                    pasta / "saida.bin",
                )

    def test_assembly_invalido(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pasta = Path(temp_dir)
            origem = pasta / "invalido.tasm"
            destino = pasta / "invalido.bin"

            origem.write_text(
                "INSTRUCAO_INVALIDA\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                build_file(origem, destino)


if __name__ == "__main__":
    unittest.main()
