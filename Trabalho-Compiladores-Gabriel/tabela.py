class TabelaSimbolos:

    def __init__(self):
        self.tabela = dict()

    def verificaSeJaExiste(self, nome):
        if nome in self.tabela:
            return True
        else:
            return False

    def declaraIdent(self, nome, tipo, qualificacao, valor):
        if not self.verificaSeJaExiste(nome):
            self.tabela[nome] = (tipo, qualificacao,valor)
            return True
        else:
            return False
    def atribuiValor(self, nome, valor):
        tipo, qualificacao, _ = self.tabela[nome]
        self.tabela[nome] = (tipo, qualificacao, valor)

    def atribuiTipo(self, tipo):
        for chave, value in self.tabela.items():
            if value[0] is None:
                _, qualificacao, valor = value
                self.tabela[chave] = (tipo, qualificacao, valor)

    def __str__(self):
        retorno = "### Tabela de Simbolos ###\n"
        for chave, value in self.tabela.items():
            retorno += f"ID: {chave}, Tipo: {value[0]}, Qualificacao: {value[1]}, Valor: {value[2]}\n"
        return retorno
