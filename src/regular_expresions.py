# Regular expression for a simple tokens

t_ASIGNATION    = r':='      # Ejemplo: operador de asignación en Pascal
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_LESS          = r'<'
t_LESSEQUAL     = r'<='
t_GREATER       = r'>'
t_GREATEREQUAL  = r'>='
t_EQUAL         = r'='
t_DISTINT       = r'<>'
t_SEMICOLON     = r';'
t_COMMA         = r','
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'
t_COLON         = r':'
t_DOBLECOLON    = r'::'
t_DOT           = r'\.'
t_DOBLEDOT      = r'\.\.'

# Regla para ignorar espacios y tabulaciones
t_ignore = ' \t'