from src.tokens import reserved


def t_ABSOLUTE(t):
    r"absolute"
    return t


def t_AND(t):
    r"and"
    return t


def t_ARRAY(t):
    r"array"
    return t


def t_ASM(t):
    r"asm"
    return t


def t_BEGIN(t):
    r"begin"
    return t


def t_CASE(t):
    r"case"
    return t


def t_CONST(t):
    r"const"
    return t


def t_CONSTRUCTOR(t):
    r"constructor"
    return t


def t_DESTRUCTOR(t):
    r"destructor"
    return t


def t_EXTERNAL(t):
    r"external"
    return t


def t_DIV(t):
    r"div"
    return t


def t_DO(t):
    r"do"
    return t


def t_DOWNTO(t):
    r"downto"
    return t


def t_ELSE(t):
    r"else"
    return t


def t_END(t):
    r"end"
    return t


def t_FILE(t):
    r"file"
    return t


def t_FOR(t):
    r"for"
    return t


def t_FORWARD(t):
    r"forward"
    return t


def t_FUNCTION(t):
    r"function"
    return t


def t_GOTO(t):
    r"goto"
    return t


def t_IF(t):
    r"if"
    return t


def t_IMPLEMENTATION(t):
    r"implementation"
    return t


def t_INTEGER(t):
    r"integer"
    return t


def t_IN(t):
    r"in"
    return t


def t_INLINE(t):
    r"inline"
    return t


def t_INTERFACE(t):
    r"interface"
    return t


def t_INTERRUPT(t):
    r"interrupt"
    return t


def t_LABEL(t):
    r"label"
    return t


def t_MOD(t):
    r"mod"
    return t


def t_NIL(t):
    r"nil"
    return t


def t_NOT(t):
    r"not"
    return t


def t_OBJECT(t):
    r"object"
    return t


def t_OF(t):
    r"of"
    return t


def t_OR(t):
    r"or"
    return t


def t_PACKED(t):
    r"packed"
    return t


def t_PRIVATE(t):
    r"private"
    return t


def t_PROCEDURE(t):
    r"procedure"
    return t


def t_PROGRAM(t):
    r"program"
    return t


def t_RECORD(t):
    r"record"
    return t


def t_REPEAT(t):
    r"repeat"
    return t


def t_SET(t):
    r"set"
    return t


def t_SHL(t):
    r"shl"
    return t


def t_SHR(t):
    r"shr"
    return t


def t_THEN(t):
    r"then"
    return t


def t_TO(t):
    r"to"
    return t


def t_TYPE(t):
    r"type"
    return t


def t_UNIT(t):
    r"unit"
    return t


def t_UNTIL(t):
    r"until"
    return t


def t_USES(t):
    r"uses"
    return t


def t_VAR(t):
    r"var"
    return t


def t_VIRTUAL(t):
    r"virtual"
    return t


def t_WITH(t):
    r"with"
    return t


def t_XOR(t):
    r"xor"
    return t


def t_REAL(t):
    r"real"
    return t


def t_BOOLEAN(t):
    r"boolean"
    return t


def t_CHAR(t):
    r"char"
    return t


def t_TRUE(t):
    r"true"
    return t


def t_FALSE(t):
    r"false"
    return t


def t_WHILE(t):
    r"while"
    return t


def t_ASIGNATION(t):
    r":="
    return t


def t_PLUS(t):
    r"\+"
    return t


def t_MINUS(t):
    r"-"
    return t


def t_TIMES(t):
    r"\*"
    return t


def t_DIVIDE(t):
    r"/"
    return t


def t_LESS(t):
    r"<"
    return t


def t_LESSEQUAL(t):
    r"<="
    return t


def t_GREATER(t):
    r">"
    return t


def t_GREATEREQUAL(t):
    r">="
    return t


def t_EQUAL(t):
    r"="
    return t


def t_DISTINT(t):
    r"<>"
    return t


def t_SEMICOLON(t):
    r";"
    return t


def t_COMMA(t):
    r","
    return t


def t_LPAREN(t):
    r"\("
    return t


def t_RPAREN(t):
    r"\)"
    return t


def t_LBRACKET(t):
    r"\["
    return t


def t_RBRACKET(t):
    r"\]"
    return t


def t_COLON(t):
    r":"
    return t


def t_DOT(t):
    r"\."
    return t


def t_DOBLEDOT(t):
    r"\.\."
    return t


def t_CARET(t):
    r"\^"
    return t


def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value.lower(), "ID")
    return t


def t_NUMBER(t):
    r"-?\d+(\.\d+)?([eE][-+]?\d+)?(?=\W|$)"
    return t


def t_COMMENT(t):
    r"\{[^}]*\}|\(\*[\s\S]*?\*\)|//.*"
    t.lexer.lineno += t.value.count("\n")
    pass


def t_STRING(t):
    r"'([^'\n]|'')*'"
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Error handling


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def t_error_number_id(t):
    r"\d+[A-Za-z_]+"
    print(f"Error léxico: Número seguido de letras '{t.value}'")



def t_error_invalid_char(t):
    r"[@$?]+"
    print(f"Carácter inválido en identificador: '{t.value[0]}'")


def t_STRING_UNCLOSED(t):
    r"'([^'\n]|'')*"
    print("Error léxico: Cadena no cerrada")


t_ignore = " \t"
