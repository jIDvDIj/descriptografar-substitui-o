"""Descriptografia da cifra de César (Grupo 4).

Regras seguidas (especificação comum aos grupos 3 e 4):
- a chave K é um inteiro de 0 a 25, a mesma usada pelo Grupo 3 para cifrar;
- o deslocamento de recuperação é sempre à esquerda, com alfabeto circular;
- só as letras A-Z e a-z são deslocadas, mantendo a caixa;
- espaços, números, pontuação, letras acentuadas e qualquer outro caractere
  passam sem alteração.
"""

import re

TAMANHO_ALFABETO = 26
CHAVE_MIN = 0
CHAVE_MAX = 25

_FORMATO_INTEIRO = re.compile(r"-?[0-9]+")


class ChaveInvalidaError(ValueError):
    """Chave K fora do formato ou do intervalo aceito."""


def validar_chave(entrada: str) -> int:
    """Converte o texto digitado em K, ou levanta ChaveInvalidaError.

    A entrada não é corrigida: espaços nas bordas, decimais ou valores fora
    do intervalo são recusados com uma mensagem explicando o motivo.
    """
    if entrada == "":
        raise ChaveInvalidaError(f"Informe a chave K (inteiro de {CHAVE_MIN} a {CHAVE_MAX}).")
    if entrada != entrada.strip():
        raise ChaveInvalidaError("Chave inválida: remova os espaços antes ou depois do número.")
    if not _FORMATO_INTEIRO.fullmatch(entrada):
        raise ChaveInvalidaError(
            f'Chave inválida: "{entrada}" não é um número inteiro. '
            f"Use um inteiro de {CHAVE_MIN} a {CHAVE_MAX}."
        )
    k = int(entrada)
    if not CHAVE_MIN <= k <= CHAVE_MAX:
        raise ChaveInvalidaError(
            f"Chave inválida: {k} está fora do intervalo de {CHAVE_MIN} a {CHAVE_MAX}."
        )
    return k


def _deslocar_esquerda(caractere: str, k: int) -> str:
    # Comparação explícita com A-Z/a-z: str.isalpha() aceitaria "é", "Ç" etc.,
    # que pela especificação não podem ser alterados.
    if "A" <= caractere <= "Z":
        base = ord("A")
    elif "a" <= caractere <= "z":
        base = ord("a")
    else:
        return caractere
    return chr((ord(caractere) - base - k) % TAMANHO_ALFABETO + base)


def descriptografar(texto_cifrado: str, k: int) -> str:
    """Recupera o texto original deslocando cada letra K posições à esquerda."""
    if isinstance(k, bool) or not isinstance(k, int) or not CHAVE_MIN <= k <= CHAVE_MAX:
        raise ChaveInvalidaError(
            f"Chave inválida: K deve ser um inteiro de {CHAVE_MIN} a {CHAVE_MAX}."
        )
    return "".join(_deslocar_esquerda(c, k) for c in texto_cifrado)
