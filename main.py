# Función de prueba para el lexer
import ply.lex as lex
import sys
from src.rules import *
from src.tokens import *
from src.simple_tokens import *


def test(data, lexer):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


lexer = lex.lex()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = "test/test.pas"
    f = open(fin, "r")
    data = f.read()
    print(data)
    lexer.input(data)
    test(data, lexer)
