
"""Depurador interativo para programas binários da TITAN-ISA."""

import argparse
import sys
from pathlib import Path

from sim.binary_cpu import BinaryCPU
from sim.binary_loader import load_binary


def show_registers(cpu):
    """Mostra o PC, o estado da CPU e os 16 registradores."""
    print(f"\nPC: {cpu.pc}")
    print(f"Passos executados: {cpu.steps}")
    print(f"CPU parada: {'sim' if cpu.halted else 'não'}")
    print("\nRegistradores:")

    for reg in range(16):
        print(f"R{reg:<2} = {cpu.read_reg(reg):>10}")

    print()


def show_memory(cpu, address):
    """Mostra uma palavra de memória no endereço informado."""
    try:
        value = cpu.load_word(address)
    except RuntimeError as exc:
        print(f"Erro: {exc}")
        return

    print(f"Memória[{address}] = {value} (0x{value:08X})")


def show_trace(cpu):
    """Mostra o histórico de execução disponível."""
    if not cpu.trace_log:
        print("Nenhum evento de trace registrado.")
        return

    for entry in cpu.trace_log:
        changes = entry["register_changes"]
        changes_text = ", ".join(changes) if changes else "nenhum"

        print(
            f"Passo {entry['step']:04} | "
            f"PC={entry['pc_before']:04} | "
            f"{entry['instruction']} | "
            f"PC seguinte={entry['pc_after']:04} | "
            f"Alterações: {changes_text}"
        )


def run_debugger(program, max_steps=10000):
    """Inicia a sessão interativa de depuração."""
    cpu = BinaryCPU(program, trace=True)

    print("=== TITAN-ISA: DEPURADOR INTERATIVO ===")
    print(f"Instruções carregadas: {len(program)}")
    print(f"Limite de passos: {max_steps}")
    print("\nComandos:")
    print("  s       Executar uma instrução")
    print("  r       Mostrar registradores e PC")
    print("  m N     Ler memória no endereço N")
    print("  t       Mostrar histórico de execução")
    print("  c       Continuar até HALT ou atingir o limite")
    print("  q       Sair")
    print("\nDigite um comando.\n")

    while True:
        try:
            command = input("TITAN> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo do depurador.")
            break

        if not command:
            continue

        parts = command.split()
        action = parts[0]

        if action == "q":
            print("Depuração encerrada.")
            break

        elif action == "r":
            show_registers(cpu)

        elif action == "m":
            if len(parts) != 2:
                print("Uso: m ENDEREÇO")
                continue

            try:
                address = int(parts[1], 0)
            except ValueError:
                print("Endereço inválido. Use decimal ou hexadecimal.")
                continue

            show_memory(cpu, address)

        elif action == "t":
            show_trace(cpu)

        elif action == "s":
            if len(parts) != 1:
                print("Uso: s")
                continue

            if cpu.halted:
                print("A CPU já executou HALT.")
                continue

            if cpu.steps >= max_steps:
                print("Limite de execução atingido.")
                continue

            try:
                cpu.step()
            except RuntimeError as exc:
                print(f"Erro de execução: {exc}")
                break

            if cpu.halted:
                print("A CPU executou HALT.")

        elif action == "c":
            if len(parts) != 1:
                print("Uso: c")
                continue

            if cpu.halted:
                print("A CPU já executou HALT.")
                continue

            try:
                while not cpu.halted and cpu.steps < max_steps:
                    cpu.step()
            except RuntimeError as exc:
                print(f"Erro de execução: {exc}")
                break

            if cpu.halted:
                print("Programa finalizado com HALT.")
            else:
                print("Limite de execução atingido.")

            show_registers(cpu)

        else:
            print("Comando desconhecido. Use s, r, m N, t, c ou q.")

    return cpu


def main():
    parser = argparse.ArgumentParser(
        description="Depurador interativo de binários TITAN-ISA."
    )
    parser.add_argument(
        "arquivo",
        type=Path,
        help="Caminho para o arquivo .bin",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="Limite total de instruções executadas (padrão: 10000)",
    )

    args = parser.parse_args()

    if args.max_steps < 1:
        parser.error("--max-steps deve ser maior que zero")

    try:
        program = load_binary(args.arquivo)

        if not program:
            print("Erro: o arquivo não contém instruções.", file=sys.stderr)
            return 1

        run_debugger(program, max_steps=args.max_steps)

    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
