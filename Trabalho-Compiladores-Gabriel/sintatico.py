"""

 Linguagem Toy

    Gramatica::

    F* --> C Rf
    Rf --> C Rf | lambda
    C  --> A | R | P
    A --> ident = E ;
    R --> read ( ident ) ;
    P --> print ( ident ) ;

    E --> M Rs
    Rs --> + M Rs | lambda
    M --> Op Rm
    Rm --> * Op Rm | lambda
    Op --> ( E ) | num

    Tokens::

    IDENT ATRIB READ PTOVIRG PRINT ADD MULT OPENPAR CLOSEPAR NUM ERROR FIMARQ

    Comentarios::

    iniciam com # ate o fim da linha

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

            self.Prog()
            self.consome( tt.FIMARQ )

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual( token ):
            self.tokenAtual = self.lex.getToken()
        else:
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def Prog(self):
        self.consome(tt.PROGRAM)
        self.consome(tt.ID)
        self.consome(tt.PTOVIRG)
        self.Decls()
        self.C_Comp()

    def Decls(self):
        if self.atualIgual( tt.VAR ):
            self.consome(tt.VAR)
            self.List_Decls()
        else:
            pass
    def C_Comp(self):
        self.consome(tt.ABRECH)
        self.Lista_Comandos()
        self.consome(tt.FECHACH)

    def Tipo(self):
        if self.atualIgual(tt.INT):
            self.consome(tt.INT)
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
        elif self.atualIgual(tt.BOOL):
            self.consome(tt.BOOL)
        else:
            self.consome(tt.CHAR)

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

    def List_Decls(self):
        self.Decls_Tipo()
        self.D()

    def Lista_Comandos(self):
        self.Comandos()
        self.G()

    def Comandos(self):
        if self.atualIgual(tt.IF):
            self.consome(tt.IF)
        elif self.atualIgual(tt.ELSE):
            self.consome(tt.ELSE)
        elif self.atualIgual(tt.READ):
            self.consome(tt.READ)
        elif self.atualIgual(tt.WRITE):
            self.consome(tt.WRITE)
        else:
            self.consome(tt.ATRIB)

    def G(self):
        if self.atualIgual(tt.IF) or self.atualIgual(tt.ELSE) or self.atualIgual(tt.READ) or self.atualIgual(tt.WRITE) or self.atualIgual(tt.ATRIB):
            self.Comandos()
        else:
            pass


    def List_Id(self):
        self.consome(tt.ID)
        self.E()

    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.List_Id()
        else:
            pass

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

    def Expr(self):
        self.Simples()
        self.P()

    def List_W(self):
        self.Elemem_W()
        self.L()

    def P(self):
        if self.atualIgual(tt.IGUAL):
            self.consome(tt.IGUAL)
            self.Simples()
        elif self.atualIgual(tt.MAIOR):
            self.consome(tt.MAIOR)
            self.Simples()
        elif self.atualIgual(tt.MENOR):
            self.consome(tt.MENOR)
            self.Simples()
        elif self.atualIgual(tt.MAIORIGUAL):
            self.consome(tt.MAIORIGUAL)
            self.Simples()
        elif self.atualIgual(tt.MENORIGUAL):
            self.consome(tt.MENORIGUAL)
            self.Simples()
        elif self.atualIgual(tt.DIFERENTE):
            self.consome(tt.DIFERENTE)
            self.Simples()
        else:
            pass

    def Simples(self):
        self.Termo()
        self.R()

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

    def Termo(self):
        self.Fat()
        self.S()

    def S(self):
        if self.atualIgual(tt.MULT):
            self.consome(tt.MULT)
            self.Simples()
        elif self.atualIgual(tt.DIV):
            self.consome(tt.DIV)
            self.Simples()
        else:
            pass
    def R(self):
        if self.atualIgual(tt.ADD):
            self.consome(tt.ADD)
            self.Simples()
        elif self.atualIgual(tt.SUB):
            self.consome(tt.SUB)
            self.Simples()
        else:
            pass
        
    def Fat(self):
        if self.atualIgual(tt.ID):
            self.consome(tt.ID)
        if self.atualIgual(tt.NUM):
            self.consome(tt.NUM)
        if self.consome(tt.OPENPAR):
            self.consome(tt.OPENPAR)
            self.Expr()
            self.consome(tt.CLOSEPAR)
        if self.atualIgual(tt.TRUE):
            self.consome(tt.TRUE)
        if self.atualIgual(tt.FALSE):
            self.consome(tt.FALSE)
        if self.atualIgual(tt.NEGACAO):
            self.consome(tt.NEGACAO)
            self.Fat()




    ########################################

if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo.toy'
   parser = Sintatico()
   parser.interprete(nome)
