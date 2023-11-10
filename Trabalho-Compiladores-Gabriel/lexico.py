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

from os import path

class TipoToken:
    ID = (1, 'id')
    ATRIB = (2, '=')
    READ = (3, 'read')
    PTOVIRG = (4, ';')
    WRITE = (5, 'write')
    OPREL = (6, 'operadores relacionais ==, <, >, <=, >=, <>')
    OPAD = (7, 'os operadores + e -')
    OPMUL = (8, 'os operadores * e /')
    OPENPAR = (9, '(')
    CLOSEPAR = (10, ')')
    CTE = (11, 'cte')
    ERROR = (12, 'erro')
    FIMARQ = (13, 'fim-de-arquivo')
    PROGRAM = (14, 'program')
    IF = (15, 'if')
    ELSE = (16, 'else')
    VAR = (17, 'var')
    INT = (18, 'int')
    REAL = (19, 'real')
    BOOL = (20, 'bool')
    CHAR = (21, 'char')
    WHILE = (22, 'while')
    FALSE = (23, 'false')
    TRUE = (24, 'true')
    ABRECH = (25, '{')
    FECHACH = (26, '}')
    VIRG = (27, ',')
    DPONTOS = (28, ':')
    CADEIA = (29, 'cadeia')
    OPNEG = (30, '!')

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

    def desempilhaLetra(self,car, lexema):
        carNext = car[1:]
        car = car[0]
        lexema = lexema + car
        self.ungetChar(carNext)
        return car, lexema

    def desempilhaLetraV2(self,car, lexema):
        carNext = car[1:]
        car = car[0]
        self.ungetChar(carNext)
        return car, lexema

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
                elif car in {'=', ';', ')','(', ',', ':','{','}','>','<','>=','<=','<>'}:
                    estado = 4
                elif car == '/':
                    estado = 5
                elif car == '"':
                    estado = 7
                elif car == '+' or '-':
                    estado = 9
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or car == ' ' or not car.isalnum():
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        return Token(TipoToken.ID, lexema, self.linha)
                elif car.isalpha():
                    estado = 10
            elif estado == 3:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isdigit()):
                    if car == '.':
                        estado = 8
                    else:
                        self.ungetChar(car)
                        return Token(TipoToken.CTE, lexema, self.linha)
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                car, lexema = self.desempilhaLetra(car,lexema)
                if car == '=':
                    return Token(TipoToken.ATRIB, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PTOVIRG, lexema, self.linha)
                elif car == '+':
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == ':':
                    return Token(TipoToken.DPONTOS, lexema, self.linha)
                elif car == ',':
                    return Token(TipoToken.VIRG, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '-':
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == '/':
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.OPENPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.CLOSEPAR, lexema, self.linha)
                elif car == '{':
                    return Token(TipoToken.ABRECH, lexema, self.linha)
                elif car == '}':
                    return Token(TipoToken.FECHACH, lexema, self.linha)
                elif car == '>':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '<':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '>=':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '<=':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '<>':
                    return Token(TipoToken.OPREL, lexema, self.linha)
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
                        if car is None:
                            return Token(TipoToken.ERROR, '</*>', self.linha)
                self.ungetChar(car)
                estado = 1
            elif estado == 7:
                lexema = lexema + car
                car = self.getChar()
                if (car == '"'):
                    # terminou o nome
                    lexema = lexema + car
                    return Token(TipoToken.CADEIA, lexema, self.linha)
                if car is None:
                    return Token(TipoToken.ERROR, '<' + lexema + '>', self.linha)
            elif estado == 8:
                lexema = lexema + car
                car = self.getChar()
                if not car.isalnum():
                    return Token(TipoToken.ERROR, '<' + lexema + '>', self.linha)
                elif car == '' or car is None:
                    return Token(TipoToken.CTE, lexema, self.linha)
            elif estado == 9:
                car = car + self.getChar()
                carAux = car[1:]
                if carAux.isalnum():
                    car, lexema = self.desempilhaLetraV2(car,lexema)
                    estado = 2
                else:
                    estado = 4
            elif estado == 10:
                lexema = lexema + car
                if len(lexema) > 32:
                    return Token(TipoToken.ERROR, '<' + lexema + ', Id com mais de 32 caracteres.' + '>', self.linha)
                car = self.getChar()
                if car is None or car == ' ' or not car.isalnum():
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        return Token(TipoToken.ID, lexema, self.linha)





if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'Testes/exemplo16.txt'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
       if token.const == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()
