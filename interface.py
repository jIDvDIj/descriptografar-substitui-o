"""Interface gráfica (tkinter) do decifrador de César do Grupo 4."""

import tkinter as tk
from tkinter import messagebox, ttk

from cesar import CHAVE_MAX, CHAVE_MIN, ChaveInvalidaError, descriptografar, validar_chave

TITULO = "Grupo 4 - Descriptografia por Substituição (César)"


def _atalho(acao):
    # Retornar "break" impede o Tk de também inserir a quebra de linha no campo de texto.
    def tratar(_evento: tk.Event) -> str:
        acao()
        return "break"

    return tratar


class JanelaDecifrador:
    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        self.resultado = ""

        raiz.title(TITULO)
        raiz.minsize(560, 460)
        raiz.columnconfigure(0, weight=1)
        raiz.rowconfigure(0, weight=1)

        quadro = ttk.Frame(raiz, padding=12)
        quadro.grid(sticky="nsew")
        quadro.columnconfigure(0, weight=1)
        quadro.rowconfigure(1, weight=1)
        quadro.rowconfigure(5, weight=1)

        ttk.Label(quadro, text="Texto cifrado:").grid(row=0, column=0, sticky="w")
        self.campo_cifrado = tk.Text(quadro, height=8, wrap="word", undo=True)
        self.campo_cifrado.grid(row=1, column=0, sticky="nsew", pady=(2, 10))

        linha_chave = ttk.Frame(quadro)
        linha_chave.grid(row=2, column=0, sticky="ew")
        ttk.Label(linha_chave, text=f"Chave K ({CHAVE_MIN} a {CHAVE_MAX}):").pack(side="left")
        self.campo_chave = ttk.Entry(linha_chave, width=6)
        self.campo_chave.pack(side="left", padx=(6, 12))
        ttk.Label(
            linha_chave,
            text="Deslocamento fixo à esquerda (mesma chave usada na cifragem).",
            foreground="#555555",
        ).pack(side="left")

        botoes = ttk.Frame(quadro)
        botoes.grid(row=3, column=0, sticky="w", pady=10)
        ttk.Button(botoes, text="Descriptografar", command=self.descriptografar).pack(side="left")
        ttk.Button(botoes, text="Copiar resultado", command=self.copiar_resultado).pack(
            side="left", padx=6
        )
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="left")

        ttk.Label(quadro, text="Texto original:").grid(row=4, column=0, sticky="w")
        self.campo_resultado = tk.Text(quadro, height=8, wrap="word", state="disabled")
        self.campo_resultado.grid(row=5, column=0, sticky="nsew", pady=(2, 6))

        self.status = ttk.Label(quadro, text="")
        self.status.grid(row=6, column=0, sticky="w")

        self.campo_cifrado.bind("<Control-Return>", _atalho(self.descriptografar))
        self.campo_chave.bind("<Return>", _atalho(self.descriptografar))
        self.campo_cifrado.focus_set()

    def _ler_texto_cifrado(self) -> str:
        # "end-1c" descarta a quebra de linha que o widget Text sempre acrescenta no fim.
        return self.campo_cifrado.get("1.0", "end-1c")

    def _mostrar_resultado(self, texto: str) -> None:
        self.resultado = texto
        self.campo_resultado.configure(state="normal")
        self.campo_resultado.delete("1.0", "end")
        self.campo_resultado.insert("1.0", texto)
        self.campo_resultado.configure(state="disabled")

    def descriptografar(self) -> None:
        try:
            k = validar_chave(self.campo_chave.get())
        except ChaveInvalidaError as erro:
            self._mostrar_resultado("")
            self.status.configure(text="")
            messagebox.showerror("Chave inválida", str(erro), parent=self.raiz)
            self.campo_chave.focus_set()
            return

        texto_cifrado = self._ler_texto_cifrado()
        self._mostrar_resultado(descriptografar(texto_cifrado, k))
        if texto_cifrado == "":
            self.status.configure(text="Texto cifrado vazio: o resultado também é vazio.")
        else:
            self.status.configure(
                text=f"Descriptografado com K={k} ({len(texto_cifrado)} caracteres)."
            )

    def copiar_resultado(self) -> None:
        # Copia a string guardada, não o conteúdo do widget, para não levar
        # quebras de linha extras para a área de transferência.
        self.raiz.clipboard_clear()
        self.raiz.clipboard_append(self.resultado)
        self.status.configure(text="Resultado copiado para a área de transferência.")

    def limpar(self) -> None:
        self.campo_cifrado.delete("1.0", "end")
        self.campo_chave.delete(0, "end")
        self._mostrar_resultado("")
        self.status.configure(text="")
        self.campo_cifrado.focus_set()


def executar() -> None:
    raiz = tk.Tk()
    JanelaDecifrador(raiz)
    raiz.mainloop()
