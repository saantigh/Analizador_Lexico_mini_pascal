# Función de prueba para el lexer
import sys
import re

import ply.lex as lex
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


lexer = lex.lex(reflags=re.IGNORECASE)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = "test/test.pas"
    f = open(fin, "r")
    data = f.read()
    print(data, end="\n\n")
    lexer.input(data)
    test(data, lexer)
