CRIPTOGRAFIA E SEGURANÇA
DISCIPLINA: SEGURANÇA EM SISTEMAS COMPUTACIONAIS
ETAPA: PROJETO DE SOFTWARE DE CRIPTOGRAFIA/DECRIPTAÇÃO

PROF. LAURO ALVES

Documento de especificação técnica comum aos quatro grupos. As regras abaixo são obrigatórias
para garantir que os softwares produzam resultados idênticos e interoperáveis.
1. Grupos: conforme documento anexo “Projetos – Criptografia”
Grupo Operação Método
1 Criptografar Transposição por colunas
2 Descriptografar Transposição por colunas
3 Criptografar Substituição / César
4 Descriptografar Substituição / César
2. Contrato obrigatório entre os programas

I. O texto é tratado como sequência de caracteres. Não retirar espaços, acentos, números ou
pontuação.
II. Preservar letras maiúsculas e minúsculas. Não converter o texto inteiro para maiúsculas.
III. Copiar e colar o texto cifrado sem acrescentar quebras de linha, aspas ou espaços.
IV. Os programas devem exibir mensagens de erro para chaves inválidas, não devem tentar
corrigir silenciosamente a entrada.
V. Cada par de grupos deverá testar as mesmas mensagens e chaves, sem alterar o algoritmo
acordado.
3. Informações adicionais para cada grupo
Grupo 1: Criptografia por transposição
1. Entradas: texto original, número de colunas (C) e chave de permutação. A chave será uma lista
ordenada dos números de 1 a C, sem repetições. Exemplo: C=4 e chave=3,1,4,2. A chave
indica a ordem em que as colunas serão lidas, NÃO a ordem em que serão preenchidas.
2. Validar C como inteiro positivo e confirmar que a chave possui exatamente C números distintos
de 1 a C.
3. Distribuir os caracteres do texto em linhas, da esquerda para a direita, preenchendo C colunas
por linha. A última linha pode ficar incompleta.
4. Ler de cima para baixo a coluna indicada pelo primeiro número da chave; repetir para os
demais números na ordem da chave.
5. Concatenar os caracteres lidos, sem separadores e sem adicionar caracteres de
preenchimento (padding).
6. Exibir o texto cifrado e a chave utilizada.

Exemplo obrigatório: texto = ABCDEFGHIJ; C = 4; chave = 3,1,4,2. Grade: [A B C D] / [E F
G H] / [I J]. Coluna 3 = CG; coluna 1 = AEI; coluna 4 = DH; coluna 2 = BFJ. Resultado:
CGAEIDHBFJ.

Grupo 2: Descriptografia por transposição
Entradas: texto cifrado, C e a MESMA chave do Grupo 1. Não usar uma chave inversa digitada
pelo usuário.
1. Validar C e a chave com as mesmas regras do Grupo 1.
2. Calcular N = quantidade de caracteres cifrados; linhas = teto(N/C); resto = N mod C.
3. Calcular o tamanho de cada coluna ORIGINAL: se resto = 0, todas têm N/C caracteres; caso
contrário, as colunas 1 até resto têm teto(N/C) caracteres e as demais têm piso(N/C).
4. Percorrer os números da chave na ordem informada; separar do texto cifrado a quantidade
de caracteres correspondente à coluna indicada e preencher essa coluna de cima para
baixo.
5. Ler a grade reconstruída por linhas, da esquerda para a direita, ignorando células
inexistentes na última linha. Exibir o texto original.
Exemplo: CGAEIDHBFJ com C=4 e chave=3,1,4,2. Tamanhos das colunas originais:
3,3,2,2. Partes na ordem da chave: CG | AEI | DH | BFJ. Reconstrução: [A B C D] / [E F G H]
/ [I J]. Resultado: ABCDEFGHIJ.
Grupo 3: Criptografia por substituição (César)
1. Entradas: texto original e chave numérica K (inteiro de 0 a 25). A direção será FIXA À
DIREITA, não incluir escolha de direção na interface.
2. Validar K como inteiro entre 0 e 25.
3. Para cada letra de A a Z, deslocar K posições à direita no alfabeto circular (após Z, voltar a
A).
4. Aplicar a mesma regra a letras minúsculas, mantendo-as minúsculas.
5. Preservar sem alteração todos os outros caracteres: espaços, números, pontuação e letras
acentuadas.
6. Concatenar os caracteres na mesma ordem e exibir o texto cifrado.
7. Exemplo: texto = Ataque ao amanhecer!; K=3; resultado = Dwdtxh dr dpdqkhfhu!

Grupo 4: Descriptografia por substituição (César)
Entradas: texto cifrado e a MESMA chave K utilizada pelo Grupo 3. O deslocamento de
recuperação será sempre À ESQUERDA.
1. Validar K como inteiro entre 0 e 25.
2. Para cada letra de A a Z, deslocar K posições à esquerda no alfabeto circular (antes de A,
voltar a Z).
3. Aplicar o deslocamento também às minúsculas, preservando a caixa.
4. Não modificar espaços, números, pontuação e caracteres acentuados.
5. Exibir o texto original reconstruído.
6. Exemplo: texto cifrado = Dwdtxh dr dpdqkhfhu!; K=3; resultado = Ataque ao amanhecer!

Testes de integração e critérios de aceite
Grupo 1 → Grupo 2: ABCDEFGHIJ, C=4, chave=3,1,4,2 → CGAEIDHBFJ → ABCDEFGHIJ.
Grupo 1 → Grupo 2: ABCDE, C=3, chave=2,3,1 → BECAD → ABCDE.
Grupo 3 → Grupo 4: Ataque ao amanhecer!, K=3 → Dwdtxh dr dpdqkhfhu! → Ataque ao
amanhecer!.
Grupo 3 → Grupo 4: XYZ xyz 123!, K=3 → ABC abc 123! → XYZ xyz 123!.
Testar também texto vazio, chaves inválidas, mensagens com espaços, caracteres especiais e
textos cujo tamanho não é múltiplo de C.
Aprovação: a mensagem recuperada deve ser exatamente igual à original, caractere por
caractere, incluindo maiúsculas, minúsculas, espaços e pontuação.

Entrega esperada
Cada grupo entregará: software executável ou instruções de execução, código-fonte e
demonstração integrada com o grupo correspondente.