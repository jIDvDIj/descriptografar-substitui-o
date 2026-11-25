# Grupo 4 — Descriptografia por Substituição (César)

Projeto de software de criptografia/decriptação da disciplina **Segurança em Sistemas
Computacionais** (Prof. Lauro Alves). A especificação completa está em
[`doc/descrição da atividade.md`](doc/descrição%20da%20atividade.md).

O programa recebe um texto cifrado pelo Grupo 3 e a mesma chave K usada na cifragem, e
recupera o texto original deslocando cada letra K posições **à esquerda** no alfabeto.

## Regras implementadas

- K precisa ser um inteiro de 0 a 25. Qualquer outra entrada (vazia, com espaços, decimal,
  negativa, maior que 25, letras) é recusada com mensagem de erro, sem correção automática.
- Só as letras `A`–`Z` e `a`–`z` são deslocadas, e cada uma mantém a caixa original. Antes
  de `A`, volta para `Z`.
- Espaços, quebras de linha, números, pontuação e letras acentuadas (`á`, `Ç`, `õ`...) não
  são alterados.
- O resultado tem exatamente o mesmo tamanho do texto cifrado: nada é removido nem
  acrescentado.

## Requisitos

Python 3.8 ou mais recente. Não há dependências externas.

- **Windows:** o instalador do [python.org](https://www.python.org/downloads/) já traz o
  tkinter (interface gráfica).
- **Linux:** pode ser necessário instalar o tkinter à parte, por exemplo
  `sudo apt install python3-tk`.

## Como executar

### Interface gráfica

```bash
python main.py
```

1. Cole o texto cifrado no campo **Texto cifrado**.
2. Digite a chave K.
3. Clique em **Descriptografar** (ou pressione `Enter` no campo da chave / `Ctrl+Enter`).
4. Use **Copiar resultado** para levar o texto à área de transferência sem quebras de
   linha extras.

### Linha de comando

```bash
python main.py --chave 3 --texto "Dwdtxh dr dpdqkhfhu!"
# Ataque ao amanhecer!

python main.py --chave 3 < cifrado.txt > original.txt
```

Sem `--texto`, o texto é lido da entrada padrão e escrito na saída exatamente como chegou
(inclusive as quebras de linha). Com chave inválida, a mensagem de erro vai para a saída de
erro e o programa termina com código 1.

## Testes

```bash
python -m unittest -v
```

Os testes cobrem os casos de integração da especificação, texto vazio, chaves inválidas,
acentos, caracteres especiais, quebras de linha e a ida e volta (cifrar e descriptografar)
para todas as 26 chaves.

### Lint e formatação

O código segue o [ruff](https://docs.astral.sh/ruff/), configurado no `pyproject.toml`. O CI
recusa pull requests com erro de lint ou fora da formatação.

```bash
pip install ruff
ruff check .          # aponta problemas
ruff format .         # formata o código
```

## Gerar executável (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name DecifradorCesarGrupo4 main.py
```

O executável fica em `dist/DecifradorCesarGrupo4.exe` e abre direto a interface gráfica.

## Como contribuir

A `main` é protegida: mudanças entram por pull request, e o merge só é liberado depois que o
workflow [`ci.yml`](.github/workflows/ci.yml) passa.

```bash
git switch -c minha-mudanca
# ... edite, rode python -m unittest ...
git commit -m "fix: descrição da correção"
git push -u origin minha-mudanca
gh pr create --fill
```

O [Dependabot](.github/dependabot.yml) abre toda segunda-feira um pull request com as
atualizações das GitHub Actions usadas nos workflows. Ele passa pelo mesmo CI antes do merge.

## Releases

Cada push na `main` (inclusive o merge de um pull request) dispara o workflow
[`release.yml`](.github/workflows/release.yml), que passa pelo mesmo CI dos pull requests,
gera o `.exe` e publica uma nova versão em [Releases](../../releases) com o executável
anexado. Se o CI falhar, nada é publicado.

O número da versão segue os commits feitos desde a última release
([Conventional Commits](https://www.conventionalcommits.org/pt-br/)):

| Commit                                        | Exemplo de versão |
|-----------------------------------------------|-------------------|
| `fix:`, `docs:`, `chore:`, `refactor:`, etc.  | 1.0.0 → 1.0.1     |
| `feat:`                                       | 1.0.1 → 1.1.0     |
| `feat!:` ou `BREAKING CHANGE:` no corpo       | 1.1.0 → 2.0.0     |

## Testes de integração com o Grupo 3

| Texto original         | K | Cifrado pelo Grupo 3   | Resultado esperado aqui |
|------------------------|---|------------------------|-------------------------|
| `Ataque ao amanhecer!` | 3 | `Dwdtxh dr dpdqkhfhu!` | `Ataque ao amanhecer!`  |
| `XYZ xyz 123!`         | 3 | `ABC abc 123!`         | `XYZ xyz 123!`          |

A aprovação exige que o texto recuperado seja igual ao original caractere por caractere.

## Estrutura

```
cesar.py           validação da chave e descriptografia
interface.py       interface gráfica (tkinter)
main.py            ponto de entrada (interface gráfica ou linha de comando)
tests/             testes automatizados (unittest)
doc/               especificação da atividade
```
