
class Sincronismo:

    def __init__(self):
        self.sincronismo = {
            'PROG': {'program': ['id'], 'id': [';'], ';': ['var', '{']},
            'DECLS': {'var': ['id', 'if', 'while', 'read', 'write', '}'], '}': []},
            'LIST-DECLS': {'id': [',', ':'], ':': ['int', 'real', 'bool', 'char', ';']},
            'D': {'id': [], ';': ['var', '{', 'if', 'while', 'read', 'write', '}'], '}': []},
            'DECL-TIPO': {'id': [',', ':'], ':': ['int', 'real', 'bool', 'char', ';']},
            'LIST-ID': {'id': [','], ',': ['id']},
            'E': {'id': [], ',': ['id']},
            'TIPO': {'int': [';', '}'], 'real': [';', '}'], 'bool': [';', '}'], 'char': [';', ']']},
            'C-COMP': {'{': ['if', 'while', 'read', 'write', '}', 'id', 'cte', 'true', 'false', 'not', '(']},
            'LISTA-COMANDOS': {'}': [], 'if': ['if'], 'while': ['while'], 'read': ['read'], 'write': ['write'], 'id': ['id'],
                              'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'G': {'}': [], 'if': ['if'], 'while': ['while'], 'read': ['read'], 'write': ['write'], 'id': ['id'],
                  'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'COMANDOS': {'if': ['if'], 'while': ['while'], 'read': ['read'], 'write': ['write'], 'id': ['id'],
                         'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'SE': {'if': ['if'], 'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'H': {'}': [], 'if': ['if'], 'while': ['while'], 'read': ['read'], 'write': ['write'], 'id': ['id'],
                  'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'ENQUANTO': {'while': ['while'], 'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'LEIA': {'read': ['read'], 'id': ['id']},
            'ATRIBUICAO': {'id': ['id']},
            'ESCREVA': {'write': ['write'], 'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'LIST-W': {'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'L': {'}': [], ',': [',']},
            'ELEM-W': {'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'EXPR': {'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'P': {'}': [], ';': [';', ')', ']', '}', 'else'], 'oprel': ['<', '>', '<=', '>=', '==', '!=']},
            'SIMPLES': {'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'R': {'}': [], ';': [';', ')', ']', '}', 'else'], 'oprel': [], 'opad': ['+', '-']},
            'TERMO': {'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']},
            'S': {'}': [], ';': [';', ')', ']', '}', 'else'], 'oprel': [], 'opad': ['+', '-'], 'opmul': ['*', '/']},
            'FAT': {'id': ['id'], 'cte': ['cte'], 'true': ['true'], 'false': ['false'], 'not': ['not'], '(': ['id', 'cte', 'true', 'false', 'not', '(']}
        }

    def obter_sincronismo(self, regra, token):
        if regra in self.sincronismo and token in self.sincronismo[regra]:
            return self.sincronismo[regra][token]
        else:
            return []
