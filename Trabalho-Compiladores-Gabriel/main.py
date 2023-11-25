import argparse

from sintatico import Sintatico

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Arquivo .txt')
parser.add_argument('-t', dest='tabela', help='Nome do arquivo para gravar a tabela de símbolos');
args = parser.parse_args()

print("COMPILANDO ARQUIVO: ", args.filename)

parser = Sintatico(args)
parser.interprete(args.filename)