
"""Testes do carregador binário da TITAN-ISA."""

import tempfile
import unittest
from pathlib import Path

from sim.binary_loader import load_binary


class TestBinaryLoader(unittest.TestCase):
    def test_carrega_instrucoes_little_endian(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            arquivo = Path(temp_dir) / "programa.bin"
            instrucoes = [0x12345678, 0xABCDEF01]

            dados = b"".join(
                instrucao.to_bytes(4, byteorder="little")
                for instrucao in instrucoes
            )
            arquivo.write_bytes(dados)

            resultado = load_binary(arquivo)

            self.assertEqual(resultado, instrucoes)

    def test_carrega_arquivo_vazio(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            arquivo = Path(temp_dir) / "vazio.bin"
            arquivo.write_bytes(b"")

            self.assertEqual(load_binary(arquivo), [])

    def test_rejeita_arquivo_com_tamanho_invalido(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            arquivo = Path(temp_dir) / "incompleto.bin"
            arquivo.write_bytes(b"\x01\x02\x03")

            with self.assertRaisesRegex(ValueError, "múltiplo de 4"):
                load_binary(arquivo)

    def test_arquivo_inexistente(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            arquivo = Path(temp_dir) / "inexistente.bin"

            with self.assertRaises(FileNotFoundError):
                load_binary(arquivo)


if __name__ == "__main__":
    unittest.main()
