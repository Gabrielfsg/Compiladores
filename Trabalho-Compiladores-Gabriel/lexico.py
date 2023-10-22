
"""

GRAMÁTICA:

P= {
PROG → program id pvirg DECLS C-COMP
DECLS →  | var LIST-DECLS
LIST-DECLS → DECL-TIPO D
D →  | LIST-DECLS
DECL-TIPO → LIST-ID dpontos TIPO pvirg
LIST-ID → id E
E →  | virg LIST-ID
TIPO → int | real | bool | char
C-COMP → abrech LISTA-COMANDOS fechach
LISTA-COMANDOS → COMANDOS G
G →  | LISTA-COMANDOS
COMANDOS → SE | ENQUANTO | LEIA | ESCREVA | ATRIBUICAO
SE → if abrepar EXPR fechapar C-COMP H
H →  | else C-COMP
ENQUANTO → while abrepar EXPR fechapar C-COMP
LEIA → read abrepar LIST-ID fechapar pvirg
ATRIBUICAO → id atrib EXPR pvirg
ESCREVA → write abrepar LIST-W fechapar pvirg
LIST-W → ELEM-W L
L →  | virg LIST-W
ELEM-W → EXPR | cadeia
EXPR → SIMPLES P
P →  | oprel SIMPLES
SIMPLES → TERMO R
R →  | opad SIMPLES
TERMO → FAT S
S →  | opmul TERMO
FAT → id | cte | abrepar EXPR fechapar | true | false | opneg FAT}

PALAVRAS RESERVADAS:

program, var, int, real, bool, char, if, else,
while, read, write, false, true

COMENTÁRIOS:

Igual C.

// = para linha
/* */ = para blocos

"""

class BancoTokens:
    print("BancoTokens")


class Lexico:
    print("Lexico")

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq
        self.arquivo = None


    def abrirArquivo(self):
        print("Abrir Arquivo")
