class TabelaSimbolos:

    def __init__(self):
        self.tabela = dict()

    def verificaSeJaExiste(self, nome):
        if nome in self.tabela:
            return True
        else:
            return False

    def declaraIdent(self, nome, tipo, qualificacao):
        if not self.verificaSeJaExiste(nome):
            self.tabela[nome] = (tipo, qualificacao)
            return True
        else:
            return False

    def atribuiTipo(self, tipo):
        for chave, value in self.tabela.items():
            if value[0] is None:
                _, qualificacao = value
                self.tabela[chave] = (tipo, qualificacao)

    def __str__(self):
        retorno = "### Tabela de Simbolos ###\n"
        for chave, value in self.tabela.items():
            retorno += f"ID: {chave}, Tipo: {value[0]}, Qualificacao: {value[1]}\n"
        return retorno
