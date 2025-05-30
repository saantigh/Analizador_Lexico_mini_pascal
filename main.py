import sys
import re

import ply.lex as lex
from src.rules import *
from src.tokens import *
from src.parser import parser
from src.semantic_analysis import *  # Aquí se importa print_symbol_table


def test_lexer(data, lexer, verbose=False):
    lexer.input(data)
    tokens_found = []
    errors = False

    if verbose:
        print("\nTokens found:")
        print("-" * 40)

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_found.append(tok)

        if verbose:
            print(f"Line {tok.lineno}: {tok.type}({tok.value})")

    print("-" * 40)
    print(f"Total tokens: {len(tokens_found)}")
    return not errors


def test_parser(data, parser, lexer):
    try:
        lexer.lineno = 1
        result = parser.parse(data, lexer=lexer, debug=True)

        if result:
            print("\nParsing successful!")
            print("The program follows Pascal syntax rules.")
            return True
        else:
            print("\nParsing failed.")
            print("The program contains syntax errors.")
            return False
    except Exception as e:
        print(f"\nParsing exception: {e}")
        return False


def main() -> None:
    lexer = lex.lex(reflags=re.IGNORECASE)

    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = "test/test_c1.pas"

    try:
        with open(fin, "r", encoding="utf-8") as f:
            data = f.read()

        print(f"Processing file: {fin}")
        print("=" * 50)

        print("\nPerforming lexical analysis...")
        lex_success = test_lexer(data, lexer, verbose=False)

        parse_success = False
        if lex_success:
            print("\nPerforming syntactic analysis...")
            parse_success = test_parser(data, parser, lexer)
        else:
            print("\nSkipping syntax analysis due to lexical errors.")

        if lex_success and parse_success:
            print("Compilation successful! No errors detected.")
            print_symbol_table()
        else:
            print("Compilation failed! Errors detected.")
    except FileNotFoundError:
        print(
            f"File '{fin}' not found. Please provide a valid Pascal source file.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        lexer.input("")
        print("\nLexer cleaned up.")


if __name__ == "__main__":
    main()
