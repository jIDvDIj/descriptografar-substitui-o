"""Ponto de entrada do decifrador de César do Grupo 4.

Sem argumentos, abre a interface gráfica. Com --chave, roda na linha de comando:

    python main.py --chave 3 --texto "Dwdtxh dr dpdqkhfhu!"
    python main.py --chave 3 < cifrado.txt
"""

import argparse
import sys
from typing import List, Optional

from cesar import ChaveInvalidaError, descriptografar, validar_chave


def _criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Grupo 4 - Descriptografia por Substituição (César). "
        "Sem argumentos, abre a interface gráfica.",
    )
    parser.add_argument(
        "-k",
        "--chave",
        help="chave K usada na cifragem (inteiro de 0 a 25)",
    )
    parser.add_argument(
        "-t",
        "--texto",
        help="texto cifrado; se omitido, é lido da entrada padrão",
    )
    return parser


def _configurar_fluxos() -> None:
    # No Windows, entrada e saída redirecionadas usam a página de código local
    # (cp1252), que corrompe acentos, e convertem \n <-> \r\n. Com UTF-8 e
    # newline="" o texto atravessa o programa sem nenhuma dessas alterações.
    for fluxo in (sys.stdin, sys.stdout):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", newline="")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        from interface import executar

        executar()
        return 0

    _configurar_fluxos()
    args = _criar_parser().parse_args(argv)
    if args.chave is None:
        print("Erro: informe a chave com --chave.", file=sys.stderr)
        return 1

    try:
        k = validar_chave(args.chave)
    except ChaveInvalidaError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    if args.texto is not None:
        print(descriptografar(args.texto, k))
    else:
        # Texto vindo de arquivo/pipe sai exatamente como entrou, sem quebra de linha extra.
        sys.stdout.write(descriptografar(sys.stdin.read(), k))
    return 0


if __name__ == "__main__":
    sys.exit(main())
