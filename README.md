<h1 align="center">Compilador da linguagem Toy</h1>

<p align="center">
  Implementação de um compilador em Python para a linguagem fictícia <strong>Toy</strong>, com analisador léxico, sintático e tabela de símbolos.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

## 📋 Sobre o projeto

Trabalho da disciplina de **Compiladores** que implementa, do zero, um compilador para a linguagem **Toy**. Cobre as etapas iniciais de compilação:

- **Análise léxica** (tokenização)
- **Análise sintática** (parsing baseado na gramática definida)
- **Tabela de símbolos**

## 📜 Gramática da linguagem Toy

A linguagem Toy suporta declaração de variáveis (`int`, `real`, `bool`, `char`), estruturas de controle `if/else` e `while`, atribuição, entrada/saída (`read`, `write`) e expressões aritméticas/lógicas.

```
PROG       → program id ; DECLS C-COMP
DECLS      → ε | var LIST-DECLS
DECL-TIPO  → LIST-ID : TIPO ;
TIPO       → int | real | bool | char
SE         → if ( EXPR ) C-COMP H
ENQUANTO   → while ( EXPR ) C-COMP
LEIA       → read ( LIST-ID ) ;
ESCREVA    → write ( LIST-W ) ;
ATRIBUICAO → id := EXPR ;
```

## 🛠️ Tecnologias

- **Python 3**

## 📁 Estrutura

```
Trabalho-Compiladores-Gabriel/
├── main.py            # Ponto de entrada
├── lexico.py          # Analisador léxico
├── sintatico.py       # Analisador sintático
├── tabela.py          # Tabela de símbolos
├── tabela.txt         # Definição da tabela
├── exemplo.toy        # Programa exemplo
└── Testes/            # Casos de teste (exemplo1.txt, ...)
```

## ✅ Pré-requisitos

- Python 3.7+

## 🚀 Como executar

```bash
cd Trabalho-Compiladores-Gabriel
python main.py exemplo.toy
```

Ou rode contra um dos arquivos da pasta `Testes/`:

```bash
python main.py Testes/exemplo1.txt
```

## 🎯 Conceitos aplicados

- Construção de gramáticas formais
- Análise léxica baseada em autômatos
- Análise sintática descendente
- Construção e consulta de tabela de símbolos

---

Trabalho da disciplina de Compiladores — [IFMG Formiga](https://www.formiga.ifmg.edu.br/).
