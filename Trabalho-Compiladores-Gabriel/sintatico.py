"""
    Linguagem Z

    Gramatica::

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

"""

from lexico import TipoToken as tt, Token, Lexico


class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.Init()
            self.consome(tt.FIMARQ)

            self.lex.fechaArquivo()
            print("Programa Compilado com Sucesso.")

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual(token):
            self.tokenAtual = self.lex.getToken()
        else:
            (const, msg) = token
            if self.tokenAtual.lexema == '<As aspas não foram fechadas.>':
                print('ERRO DE SINTAXE [linha %d]: era esperado " Fechar Aspas ( " ) " mas veio "%s"'
                      % (self.tokenAtual.linha,  self.tokenAtual.lexema))
            else:
                print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
                      % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def Init(self):
        if self.atualIgual(tt.PROGRAM):
            self.Prog()
        else:
            pass

    def Prog(self):
        self.consome(tt.PROGRAM)
        self.consome(tt.ID)
        self.consome(tt.PTOVIRG)
        self.Decls()
        self.C_Comp()

    def Decls(self):
        if self.atualIgual(tt.VAR):
            self.consome(tt.VAR)
            self.List_Decls()
        else:
            pass

    def List_Decls(self):
        self.Decls_Tipo()
        self.D()

    def D(self):
        if self.atualIgual(tt.ID):
            self.List_Decls()
        else:
            pass

    def Decls_Tipo(self):
        self.List_Id()
        self.consome(tt.DPONTOS)
        self.Tipo()
        self.consome(tt.PTOVIRG)

    def List_Id(self):
        self.consome(tt.ID)
        self.E()

    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.List_Id()
        else:
            pass

    def Tipo(self):
        if self.atualIgual(tt.INT):
            self.consome(tt.INT)
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
        elif self.atualIgual(tt.BOOL):
            self.consome(tt.BOOL)
        else:
            self.consome(tt.CHAR)

    def C_Comp(self):
        self.consome(tt.ABRECH)
        self.Lista_Comandos()
        self.consome(tt.FECHACH)

    def Lista_Comandos(self):
        self.Comandos()
        self.G()

    def G(self):
        if self.atualIgual(tt.IF) or self.atualIgual(tt.WHILE) or self.atualIgual(tt.READ) or self.atualIgual(tt.WRITE) or self.atualIgual(tt.ID):
            self.Lista_Comandos()
        else:
            pass

    def Comandos(self):
        if self.atualIgual(tt.IF):
            self.Se()
        elif self.atualIgual(tt.WHILE):
            self.Enquanto()
        elif self.atualIgual(tt.READ):
            self.Leia()
        elif self.atualIgual(tt.WRITE):
            self.Escreva()
        else:
            self.Atribuicao()

    def Se(self):
        self.consome(tt.IF)
        self.consome(tt.OPENPAR)
        self.Expr()
        self.consome(tt.CLOSEPAR)
        self.C_Comp()
        self.H()

    def H(self):
        if self.atualIgual(tt.ELSE):
            self.consome(tt.ELSE)
            self.C_Comp()
        else:
            pass

    def Enquanto(self):
        self.consome(tt.WHILE)
        self.consome(tt.OPENPAR)
        self.Expr()
        self.consome(tt.CLOSEPAR)
        self.C_Comp()

    def Leia(self):
        self.consome(tt.READ)
        self.consome(tt.OPENPAR)
        self.List_Id()
        self.consome(tt.CLOSEPAR)
        self.consome(tt.PTOVIRG)

    def Atribuicao(self):
        self.consome(tt.ID)
        self.consome(tt.ATRIB)
        self.Expr()
        self.consome(tt.PTOVIRG)

    def Escreva(self):
        self.consome(tt.WRITE)
        self.consome(tt.OPENPAR)
        self.List_W()
        self.consome(tt.CLOSEPAR)
        self.consome(tt.PTOVIRG)

    def List_W(self):
        self.Elemem_W()
        self.L()

    def L(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.List_W()
        else:
            pass

    def Elemem_W(self):
        if self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA)
        else:
            self.Expr()

    def Expr(self):
        self.Simples()
        self.P()

    def P(self):
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL)
            self.Simples()
        else:
            pass

    def Simples(self):
        self.Termo()
        self.R()

    def R(self):
        if self.atualIgual(tt.OPAD):
            self.consome(tt.OPAD)
            self.Simples()
        else:
            pass

    def Termo(self):
        self.Fat()
        self.S()

    def S(self):
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.Simples()
        else:
            pass

    def Fat(self):
        if self.atualIgual(tt.ID):
            self.consome(tt.ID)
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE)
        elif self.atualIgual(tt.OPENPAR):
            self.consome(tt.OPENPAR)
            self.Expr()
            self.consome(tt.CLOSEPAR)
        elif self.atualIgual(tt.TRUE):
            self.consome(tt.TRUE)
        elif self.atualIgual(tt.FALSE):
            self.consome(tt.FALSE)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG)
            self.Fat()

    ########################################


if __name__ == "__main__":
    # nome = input("Entre com o nome do arquivo: ")
    nome = 'Testes/exemplo16.txt'
    parser = Sintatico()
    parser.interprete(nome)
