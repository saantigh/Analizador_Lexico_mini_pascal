# Pascal rules


def t_ABSOLUTE(t):
    r"ABSOLUTE|absolute"
    return t


def t_AND(t):
    r"AND|and"
    return t


def t_ARRAY(t):
    r"ARRAY|array"
    return t


def t_ASM(t):
    r"ASM|asm"
    return t


def t_BEGIN(t):
    r"BEGIN|begin"
    return t


def t_CASE(t):
    r"CASE|case"
    return t


def t_CONST(t):
    r"CONST|const"
    return t


def t_CONSTRUCTOR(t):
    r"CONSTRUCTOR|constructor"
    return t


def t_DESTRUCTOR(t):
    r"DESTRUCTOR|destructor"
    return t


def t_EXTERNAL(t):
    r"EXTERNAL|external"
    return t


def t_DIV(t):
    r"DIV|div"
    return t


def t_DO(t):
    r"DO|do"
    return t


def t_DOWNTO(t):
    r"DOWNTO|downto"
    return t


def t_ELSE(t):
    r"ELSE|else"
    return t


def t_END(t):
    r"END|end"
    return t


def t_FILE(t):
    r"FILE|file"
    return t


def t_FOR(t):
    r"FOR|for"
    return t


def t_FORWARD(t):
    r"FORWARD|forward"
    return t


def t_FUNCTION(t):
    r"FUNCTION|function"
    return t


def t_GOTO(t):
    r"GOTO|goto"
    return t


def t_IF(t):
    r"IF|if"
    return t


def t_IMPLEMENTATION(t):
    r"IMPLEMENTATION|implementation"
    return t


def t_IN(t):
    r"IN|in"
    return t


def t_INLINE(t):
    r"INLINE|inline"
    return t


def t_INTERFACE(t):
    r"INTERFACE|interface"
    return t


def t_INTERRUPT(t):
    r"INTERRUPT|interrupt"
    return t


def t_LABEL(t):
    r"LABEL|label"
    return t


def t_MOD(t):
    r"MOD|mod"
    return t


def t_NIL(t):
    r"NIL|nil"
    return t


def t_NOT(t):
    r"NOT|not"
    return t


def t_OBJECT(t):
    r"OBJECT|object"
    return t


def t_OF(t):
    r"OF|of"
    return t


def t_OR(t):
    r"OR|or"
    return t


def t_PACKED(t):
    r"PACKED|packed"
    return t


def t_PRIVATE(t):
    r"PRIVATE|private"
    return t


def t_PROCEDURE(t):
    r"PROCEDURE|procedure"
    return t


def t_PROGRAM(t):
    r"PROGRAM|program"
    return t


def t_RECORD(t):
    r"RECORD|record"
    return t


def t_REPEAT(t):
    r"REPEAT|repeat"
    return t


def t_SET(t):
    r"SET|set"
    return t


def t_SHL(t):
    r"SHL|shl"
    return t


def t_SHR(t):
    r"SHR|shr"
    return t


def t_STRING(t):
    r"STRING|string"
    return t


def t_THEN(t):
    r"THEN|then"
    return t


def t_TO(t):
    r"TO|to"
    return t


def t_TYPE(t):
    r"TYPE|type"
    return t


def t_UNIT(t):
    r"UNIT|unit"
    return t


def t_UNTIL(t):
    r"UNTIL|until"
    return t


def t_USES(t):
    r"USES|uses"
    return t


def t_VAR(t):
    r"VAR|var"
    return t


def t_VIRTUAL(t):
    r"VIRTUAL|virtual"
    return t


def t_WITH(t):
    r"WITH|with"
    return t


def t_XOR(t):
    r"XOR|xor"
    return t


# Symbol's rules


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


# Other's


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    return t


def t_NUMBER(t):
    r"\d+"
    return t
