import io
import string
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from cesar import ChaveInvalidaError, descriptografar, forca_bruta, validar_chave
from main import main


def cifrar_referencia(texto: str, k: int) -> str:
    """Cifragem do Grupo 3 (deslocamento à direita), só para os testes de ida e volta."""
    saida = []
    for c in texto:
        if "A" <= c <= "Z":
            saida.append(chr((ord(c) - ord("A") + k) % 26 + ord("A")))
        elif "a" <= c <= "z":
            saida.append(chr((ord(c) - ord("a") + k) % 26 + ord("a")))
        else:
            saida.append(c)
    return "".join(saida)


class TestCriteriosDeAceite(unittest.TestCase):
    """Casos de integração Grupo 3 -> Grupo 4 definidos na especificação."""

    def test_exemplo_obrigatorio(self):
        self.assertEqual(descriptografar("Dwdtxh dr dpdqkhfhu!", 3), "Ataque ao amanhecer!")

    def test_volta_do_alfabeto(self):
        self.assertEqual(descriptografar("ABC abc 123!", 3), "XYZ xyz 123!")


class TestDescriptografar(unittest.TestCase):
    def test_chave_zero_nao_altera(self):
        texto = "Qualquer Texto, 123!"
        self.assertEqual(descriptografar(texto, 0), texto)

    def test_chave_maxima(self):
        self.assertEqual(descriptografar("ZAza", 25), "ABab")

    def test_texto_vazio(self):
        self.assertEqual(descriptografar("", 7), "")

    def test_preserva_maiusculas_e_minusculas(self):
        self.assertEqual(descriptografar("KhOor ZrUog", 3), "HeLlo WoRld")

    def test_acentuados_nao_sao_alterados(self):
        self.assertEqual(descriptografar("áéíóú ÁÉÍÓÚ ç Ç ã õ ñ ü", 5), "áéíóú ÁÉÍÓÚ ç Ç ã õ ñ ü")

    def test_letras_com_acento_ao_lado_de_letras_comuns(self):
        self.assertEqual(descriptografar("Fçãr", 3), "Cção")

    def test_espacos_quebras_de_linha_e_tabulacoes(self):
        self.assertEqual(descriptografar("  d\tb\n\nc  ", 1), "  c\ta\n\nb  ")

    def test_numeros_pontuacao_e_especiais(self):
        especiais = string.digits + string.punctuation + " ºª§°€£¥©®™←→😀"
        self.assertEqual(descriptografar(especiais, 13), especiais)

    def test_ida_e_volta_para_todas_as_chaves(self):
        original = (
            string.ascii_letters
            + string.digits
            + string.punctuation
            + " \n\tÀÁÂÃÉÊÍÓÔÕÚÇàáâãéêíóôõúç"
            + "Ataque ao amanhecer!"
        )
        for k in range(26):
            with self.subTest(k=k):
                self.assertEqual(descriptografar(cifrar_referencia(original, k), k), original)

    def test_recusa_chave_fora_do_intervalo(self):
        for k in (-1, 26, 100):
            with self.subTest(k=k), self.assertRaises(ChaveInvalidaError):
                descriptografar("abc", k)

    def test_recusa_chave_que_nao_e_inteiro(self):
        for k in ("3", 3.0, None, True):
            with self.subTest(k=k), self.assertRaises(ChaveInvalidaError):
                descriptografar("abc", k)


class TestForcaBruta(unittest.TestCase):
    def test_testa_as_26_chaves_em_ordem(self):
        resultados = forca_bruta("abc")
        self.assertEqual([k for k, _ in resultados], list(range(26)))

    def test_a_chave_certa_aparece_entre_as_tentativas(self):
        resultados = dict(forca_bruta("Dwdtxh dr dpdqkhfhu!"))
        self.assertEqual(resultados[3], "Ataque ao amanhecer!")

    def test_cada_tentativa_igual_a_descriptografar(self):
        cifrado = "Fçãr Á é! 123\nXyZ"
        for k, texto in forca_bruta(cifrado):
            with self.subTest(k=k):
                self.assertEqual(texto, descriptografar(cifrado, k))

    def test_texto_vazio(self):
        self.assertEqual(forca_bruta(""), [(k, "") for k in range(26)])


class TestValidarChave(unittest.TestCase):
    def test_chaves_validas(self):
        for entrada, esperado in (("0", 0), ("3", 3), ("25", 25), ("07", 7)):
            with self.subTest(entrada=entrada):
                self.assertEqual(validar_chave(entrada), esperado)

    def test_chaves_invalidas(self):
        invalidas = ("", " ", "26", "-1", "-0x", "abc", "3.0", "3,5", "1e1", " 3", "3 ", "+3", "٣")
        for entrada in invalidas:
            with self.subTest(entrada=entrada), self.assertRaises(ChaveInvalidaError):
                validar_chave(entrada)

    def test_mensagem_explica_o_erro(self):
        with self.assertRaisesRegex(ChaveInvalidaError, "fora do intervalo"):
            validar_chave("30")
        with self.assertRaisesRegex(ChaveInvalidaError, "não é um número inteiro"):
            validar_chave("abc")
        with self.assertRaisesRegex(ChaveInvalidaError, "Informe a chave"):
            validar_chave("")
        with self.assertRaisesRegex(ChaveInvalidaError, "espaços"):
            validar_chave(" 3")


class TestLinhaDeComando(unittest.TestCase):
    def _executar(self, argv):
        saida, erro = io.StringIO(), io.StringIO()
        with redirect_stdout(saida), redirect_stderr(erro):
            codigo = main(argv)
        return codigo, saida.getvalue(), erro.getvalue()

    def test_descriptografa(self):
        codigo, saida, _ = self._executar(["--chave", "3", "--texto", "Dwdtxh dr dpdqkhfhu!"])
        self.assertEqual(codigo, 0)
        self.assertEqual(saida, "Ataque ao amanhecer!\n")

    def test_chave_invalida_retorna_erro(self):
        codigo, saida, erro = self._executar(["--chave", "26", "--texto", "abc"])
        self.assertEqual(codigo, 1)
        self.assertEqual(saida, "")
        self.assertIn("fora do intervalo", erro)

    def test_le_da_entrada_padrao_sem_acrescentar_quebra(self):
        with mock.patch("sys.stdin", io.StringIO("Dwdtxh\r\ndr!\n")):
            codigo, saida, _ = self._executar(["--chave", "3"])
        self.assertEqual(codigo, 0)
        self.assertEqual(saida, "Ataque\r\nao!\n")

    def test_sem_chave_retorna_erro(self):
        codigo, _, erro = self._executar(["--texto", "abc"])
        self.assertEqual(codigo, 1)
        self.assertIn("--chave", erro)


if __name__ == "__main__":
    unittest.main()
