from lexico import Lexico


class Sintatico:

    def __init__(self):
        self.lexArquivo = None
        self.token = None
        self.erro = False
        self.linhaErro = None


    def iniciar(self, nomeArq):
        self.lexArquivo = Lexico(nomeArq)
        self.lexArquivo.abrirArquivo()


