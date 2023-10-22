import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Arquivo .txt')
args = parser.parse_args()

print("COMPILANDO ARQUIVO: ", args.filename)