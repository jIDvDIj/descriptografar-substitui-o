"""Interface gráfica (tkinter) do decifrador de César do Grupo 4."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict

from cesar import (
    CHAVE_MAX,
    CHAVE_MIN,
    ChaveInvalidaError,
    descriptografar,
    forca_bruta,
    validar_chave,
)

TITULO = "Grupo 4 - Descriptografia por Substituição (César)"
LIMITE_PREVIA = 200


def _ler_texto(campo: tk.Text) -> str:
    # "end-1c" descarta a quebra de linha que o widget Text sempre acrescenta no fim.
    return campo.get("1.0", "end-1c")


def _atalho(acao):
    # Retornar "break" impede o Tk de também inserir a quebra de linha no campo de texto.
    def tratar(_evento: tk.Event) -> str:
        acao()
        return "break"

    return tratar


def _copiar(widget: tk.Misc, texto: str) -> None:
    widget.clipboard_clear()
    widget.clipboard_append(texto)


class AbaDescriptografar(ttk.Frame):
    """Fluxo do contrato entre os grupos: texto cifrado + a mesma chave K do Grupo 3."""

    def __init__(self, pai: tk.Misc) -> None:
        super().__init__(pai, padding=12)
        self.resultado = ""

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)

        ttk.Label(self, text="Texto cifrado:").grid(row=0, column=0, sticky="w")
        self.campo_cifrado = tk.Text(self, height=8, wrap="word", undo=True)
        self.campo_cifrado.grid(row=1, column=0, sticky="nsew", pady=(2, 10))

        linha_chave = ttk.Frame(self)
        linha_chave.grid(row=2, column=0, sticky="ew")
        ttk.Label(linha_chave, text=f"Chave K ({CHAVE_MIN} a {CHAVE_MAX}):").pack(side="left")
        self.campo_chave = ttk.Entry(linha_chave, width=6)
        self.campo_chave.pack(side="left", padx=(6, 12))
        ttk.Label(
            linha_chave,
            text="Deslocamento fixo à esquerda (mesma chave usada na cifragem).",
            foreground="#555555",
        ).pack(side="left")

        botoes = ttk.Frame(self)
        botoes.grid(row=3, column=0, sticky="w", pady=10)
        ttk.Button(botoes, text="Descriptografar", command=self.descriptografar).pack(side="left")
        ttk.Button(botoes, text="Copiar resultado", command=self.copiar_resultado).pack(
            side="left", padx=6
        )
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="left")

        ttk.Label(self, text="Texto original:").grid(row=4, column=0, sticky="w")
        self.campo_resultado = tk.Text(self, height=8, wrap="word", state="disabled")
        self.campo_resultado.grid(row=5, column=0, sticky="nsew", pady=(2, 6))

        self.status = ttk.Label(self, text="")
        self.status.grid(row=6, column=0, sticky="w")

        self.campo_cifrado.bind("<Control-Return>", _atalho(self.descriptografar))
        self.campo_chave.bind("<Return>", _atalho(self.descriptografar))

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
            messagebox.showerror("Chave inválida", str(erro), parent=self)
            self.campo_chave.focus_set()
            return

        texto_cifrado = _ler_texto(self.campo_cifrado)
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
        _copiar(self, self.resultado)
        self.status.configure(text="Resultado copiado para a área de transferência.")

    def limpar(self) -> None:
        self.campo_cifrado.delete("1.0", "end")
        self.campo_chave.delete(0, "end")
        self._mostrar_resultado("")
        self.status.configure(text="")
        self.campo_cifrado.focus_set()


class AbaForcaBruta(ttk.Frame):
    """Demonstração da fraqueza da cifra: decifra com as 26 chaves de uma vez."""

    def __init__(self, pai: tk.Misc) -> None:
        super().__init__(pai, padding=12)
        self.resultados: Dict[int, str] = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)

        ttk.Label(
            self,
            text=(
                "A cifra de César tem só 26 chaves possíveis. Sem conhecer K, basta "
                "testar todas e procurar a tentativa que forma um texto legível."
            ),
            foreground="#555555",
            wraplength=520,
            justify="left",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.campo_cifrado = tk.Text(self, height=4, wrap="word", undo=True)
        ttk.Label(self, text="Texto cifrado:").grid(row=1, column=0, sticky="w")
        self.campo_cifrado.grid(row=2, column=0, sticky="nsew", pady=(2, 8))

        botoes = ttk.Frame(self)
        botoes.grid(row=3, column=0, sticky="w", pady=(0, 8))
        ttk.Button(botoes, text="Testar as 26 chaves", command=self.testar_todas).pack(side="left")
        ttk.Button(botoes, text="Copiar tentativa selecionada", command=self.copiar).pack(
            side="left", padx=6
        )

        ttk.Label(self, text="Tentativas:").grid(row=4, column=0, sticky="w")
        tabela_quadro = ttk.Frame(self)
        tabela_quadro.grid(row=5, column=0, sticky="nsew", pady=(2, 6))
        tabela_quadro.columnconfigure(0, weight=1)
        tabela_quadro.rowconfigure(0, weight=1)

        self.tabela = ttk.Treeview(
            tabela_quadro, columns=("k", "texto"), show="headings", selectmode="browse"
        )
        self.tabela.heading("k", text="K")
        self.tabela.heading("texto", text="Texto decifrado")
        self.tabela.column("k", width=40, minwidth=40, stretch=False, anchor="center")
        self.tabela.column("texto", width=480)
        self.tabela.grid(row=0, column=0, sticky="nsew")
        rolagem = ttk.Scrollbar(tabela_quadro, orient="vertical", command=self.tabela.yview)
        rolagem.grid(row=0, column=1, sticky="ns")
        self.tabela.configure(yscrollcommand=rolagem.set)

        self.status = ttk.Label(self, text="")
        self.status.grid(row=6, column=0, sticky="w")

        self.campo_cifrado.bind("<Control-Return>", _atalho(self.testar_todas))
        self.tabela.bind("<Double-1>", _atalho(self.copiar))

    @staticmethod
    def _previa(texto: str) -> str:
        # A tabela mostra uma linha por chave; quebras viram "⏎" só na exibição.
        previa = texto.replace("\r\n", "⏎").replace("\n", "⏎").replace("\t", " ")
        if len(previa) > LIMITE_PREVIA:
            previa = previa[:LIMITE_PREVIA] + "…"
        return previa

    def testar_todas(self) -> None:
        self.tabela.delete(*self.tabela.get_children())
        self.resultados = dict(forca_bruta(_ler_texto(self.campo_cifrado)))
        for k, texto in self.resultados.items():
            self.tabela.insert("", "end", iid=str(k), values=(k, self._previa(texto)))
        self.status.configure(
            text="Selecione a tentativa legível e copie (ou dê dois cliques na linha)."
        )

    def copiar(self) -> None:
        selecionada = self.tabela.selection()
        if not selecionada:
            self.status.configure(text="Selecione uma tentativa na tabela primeiro.")
            return
        k = int(selecionada[0])
        _copiar(self, self.resultados[k])
        self.status.configure(text=f"Tentativa com K={k} copiada para a área de transferência.")


class JanelaDecifrador:
    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        raiz.title(TITULO)
        raiz.minsize(600, 500)

        abas = ttk.Notebook(raiz)
        abas.pack(fill="both", expand=True)
        self.aba_descriptografar = AbaDescriptografar(abas)
        self.aba_forca_bruta = AbaForcaBruta(abas)
        abas.add(self.aba_descriptografar, text="Descriptografar")
        abas.add(self.aba_forca_bruta, text="Força bruta")

        self.aba_descriptografar.campo_cifrado.focus_set()


def executar() -> None:
    raiz = tk.Tk()
    JanelaDecifrador(raiz)
    raiz.mainloop()
