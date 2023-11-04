"""

 Linguagem Toy

    Gramatica::

    F* --> C F | C
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

from os import path

class TipoToken:
    ID = (1, 'id')
    ATRIB = (2, '=')
    READ = (3, 'read')
    PTOVIRG = (4, ';')
    WRITE = (5, 'write')
    ADD = (6, '+')
    MULT = (7, '*')
    OPENPAR = (8, '(')
    CLOSEPAR = (9, ')')
    NUM = (10, 'numero')
    ERROR = (11, 'erro')
    FIMARQ = (12, 'fim-de-arquivo')
    PROGRAM = (13, 'program')
    IF = (14, 'if')
    ELSE = (15, 'else')
    VAR = (16, 'var')
    INT = (17, 'int')
    REAL = (18, 'real')
    BOOL = (19, 'bool')
    CHAR = (20, 'char')
    WHILE = (21, 'while')
    FALSE = (22, 'false')
    TRUE = (23, 'true')
    IGUAL = (24, '==')
    MAIOR = (25, '>')
    MENOR = (26, '<')
    MAIORIGUAL = (27, '>=')
    MENORIGUAL = (28, '<=')
    DIFERENTE = (29, '<>')
    SUB = (30, '-')
    DIV = (31, '/')
    ABRECH = (32, '{')
    FECHACH = (33, '}')
    VIRG = (34, ',')
    DPONTOS = (34, ':')

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha

class Lexico:
    # dicionario de palavras reservadas
    reservadas = { 'write': TipoToken.WRITE, 'read': TipoToken.READ, 'program': TipoToken.PROGRAM, 'if': TipoToken.IF,
                   'else': TipoToken.ELSE, 'var': TipoToken.VAR , 'int': TipoToken.INT, 'real': TipoToken.REAL,
                   'bool': TipoToken.BOOL, 'char': TipoToken.CHAR , 'while': TipoToken.WHILE, 'false': TipoToken.FALSE,
                   'true': TipoToken.TRUE}

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    estado = 3
                elif car in {'=', ';', '+', '*', '-', '(', ')', ',', ':','{','}'}:
                    estado = 4
                elif car == '/':
                    estado = 5
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isalnum()):
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        return Token(TipoToken.ID, lexema, self.linha)
            elif estado == 3:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isdigit()):
                    # terminou o numero
                    self.ungetChar(car)
                    return Token(TipoToken.NUM, lexema, self.linha)
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                carNext = car[1:]
                car = car[0]
                lexema = lexema + car
                self.ungetChar(carNext)
                if car == '=':
                    return Token(TipoToken.ATRIB, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PTOVIRG, lexema, self.linha)
                elif car == '+':
                    return Token(TipoToken.ADD, lexema, self.linha)
                elif car == ':':
                    return Token(TipoToken.DPONTOS, lexema, self.linha)
                elif car == ',':
                    return Token(TipoToken.VIRG, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.MULT, lexema, self.linha)
                elif car == '-':
                    return Token(TipoToken.SUB, lexema, self.linha)
                elif car == '/':
                    return Token(TipoToken.DIV, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.OPENPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.CLOSEPAR, lexema, self.linha)
                elif car == '{':
                    return Token(TipoToken.ABRECH, lexema, self.linha)
                elif car == '}':
                    return Token(TipoToken.FECHACH, lexema, self.linha)
                elif car == '>':
                    return Token(TipoToken.MAIOR, lexema, self.linha)
                elif car == '<':
                    return Token(TipoToken.MENOR, lexema, self.linha)
                elif car == '>=':
                    return Token(TipoToken.MAIORIGUAL, lexema, self.linha)
                elif car == '<=':
                    return Token(TipoToken.MENORIGUAL, lexema, self.linha)
                elif car == '<>':
                    return Token(TipoToken.DIFERENTE, lexema, self.linha)
            elif estado == 5:
                car = car + self.getChar()
                carAux = car[1:]
                if carAux == '/' or carAux == '*':
                    estado = 6
                else:
                    estado = 4
            elif estado == 6:
                # consumindo comentario
                if car == '//':
                    while (not car is None) and (car != '\n'):
                        car = self.getChar()
                else:
                    carStop = ''
                    while (not car is None) and (carStop != '*/'):
                        car = self.getChar()
                        if car == '*' or car == "/":
                            carStop += car
                            if carStop == "*/":
                                car = self.getChar()
                        if car == '\n':
                            self.linha += 1
                self.ungetChar(car)
                estado = 1



if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'Testes/exemplo1.txt'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
       if token.const == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()
