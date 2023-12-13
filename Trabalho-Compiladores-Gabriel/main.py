import argparse

from sintatico import Sintatico
import os

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Arquivo .txt')
parser.add_argument('-t', dest='tabela', help='Nome do arquivo para gravar a tabela de símbolos');
args = parser.parse_args()

if os.path.exists(args.filename):
    print("COMPILANDO ARQUIVO: ", args.filename)
    parser = Sintatico(args)
    parser.interprete(args.filename)
else:
    print(f'O arquivo {args.filename} não existe, logo não foi possivel iniciar a compilação.')

