import argparse

from sintatico import Sintatico

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Arquivo .txt')
args = parser.parse_args()

print(args.filename)
print("COMPILANDO ARQUIVO: ", args.filename)

parser = Sintatico()
parser.interprete(args.filename)