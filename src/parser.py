# parser.py
import ply.yacc as yacc
from src.tokens import tokens

# Program structure


def p_program(p):
    """program : program_header uses_clause declaration_blocks main_block"""
    p[0] = True
    pass


def p_program_header(p):
    """program_header : PROGRAM ID SEMICOLON
    | UNIT ID SEMICOLON"""
    pass


def p_uses_clause(p):
    """uses_clause : USES id_list SEMICOLON
    | empty"""
    pass


def p_id_list(p):
    """id_list : ID
    | id_list COMMA ID"""
    pass


def p_declaration_blocks(p):
    """declaration_blocks : declaration_blocks declaration_block
    | empty"""
    pass


def p_declaration_block(p):
    """declaration_block : label_declaration
    | const_declaration_block
    | type_declaration_block
    | var_declaration_block
    | procedure_declaration
    | function_declaration
    | constructor_implementation
    | destructor_implementation
    | method_implementation
    | implementation_block
    | interface_block"""
    pass


def p_main_block(p):
    """main_block : compound_statement DOT"""
    pass


def p_interface_block(p):
    """interface_block : INTERFACE declaration_blocks"""
    pass


def p_implementation_block(p):
    """implementation_block : IMPLEMENTATION declaration_blocks"""
    pass


def p_label_declaration(p):
    """label_declaration : LABEL number_list SEMICOLON"""
    pass


def p_number_list(p):
    """number_list : NUMBER
    | number_list COMMA NUMBER"""
    pass


def p_const_declaration_block(p):
    """const_declaration_block : CONST const_list"""
    pass


def p_const_list(p):
    """const_list : const_list const_declaration
    | const_declaration"""
    pass


def p_const_declaration(p):
    """const_declaration : ID EQUAL constant SEMICOLON
    | ID COLON data_type_list EQUAL constant SEMICOLON"""  # Added typed constants
    pass


def p_constant(p):
    """constant : NUMBER
    | STRING
    | TRUE
    | FALSE
    | NIL
    | ORDINAL_CONSTANT"""  # Can reference other constants
    p[0] = p[1]
    pass


def p_type_declaration_block(p):
    """type_declaration_block : TYPE type_list"""
    pass


def p_type_list(p):
    """type_list : type_list type_declaration
    | type_declaration"""
    pass


def p_type_declaration(p):
    """type_declaration : ID EQUAL type_definition SEMICOLON"""
    pass


def p_type_definition(p):
    """type_definition : data_type_list
    | LPAREN id_list RPAREN
    | NUMBER DOBLEDOT NUMBER
    | CHAR DOBLEDOT CHAR
    | ID DOBLEDOT ID
    | record_type
    | array_type
    | set_type
    | pointer_type
    | file_type
    | object_type
    | string_type"""
    pass


def p_string_type(p):
    """string_type : STRING
    | STRING LBRACKET NUMBER RBRACKET"""
    pass


def p_record_type(p):
    """record_type : RECORD record_list END
    | PACKED RECORD record_list END"""
    pass


def p_array_type(p):
    """array_type : ARRAY LBRACKET type_range_list RBRACKET OF data_type_list
    | PACKED ARRAY LBRACKET type_range_list RBRACKET OF data_type_list
    | ARRAY OF data_type_list
    """
    pass


def p_type_range_list(p):
    """type_range_list : type_range
    | type_range_list COMMA type_range"""
    pass


def p_type_range(p):
    """type_range : NUMBER DOBLEDOT NUMBER
    | NUMBER DOBLEDOT ID
    | ID DOBLEDOT NUMBER
    | CHAR DOBLEDOT CHAR
    | ID DOBLEDOT ID
    | ID"""
    pass


def p_set_type(p):
    """set_type : SET OF set_range"""
    pass


def p_set_range(p):
    """set_range : data_type_set
    | NUMBER DOBLEDOT NUMBER
    | CHAR DOBLEDOT CHAR
    | ID"""
    pass


def p_pointer_type(p):
    """pointer_type : CARET ID
    | CARET data_type_list"""
    pass


def p_file_type(p):
    """file_type : FILE OF data_type_list
    | FILE"""
    pass


def p_object_type(p):
    """object_type : OBJECT object_heritage object_fields object_methods END"""
    pass


def p_object_heritage(p):
    """object_heritage : LPAREN ID RPAREN
    | empty"""
    pass


def p_object_fields(p):
    """object_fields : object_fields var_declaration
    | empty"""
    pass


def p_object_methods(p):
    """object_methods : object_methods method_declaration
    | empty"""
    pass


def p_method_declaration(p):
    """method_declaration : procedure_header SEMICOLON
    | function_header SEMICOLON
    | constructor_declaration
    | destructor_declaration
    | procedure_header SEMICOLON directive
    | function_header SEMICOLON directive"""
    pass


def p_constructor_implementation(p):
    """constructor_implementation : CONSTRUCTOR ID DOT ID parameters SEMICOLON declaration_blocks compound_statement SEMICOLON"""
    pass


def p_destructor_implementation(p):
    """destructor_implementation : DESTRUCTOR ID DOT ID parameters SEMICOLON declaration_blocks compound_statement SEMICOLON"""
    pass


def p_method_implementation(p):
    """method_implementation : PROCEDURE ID DOT ID parameters SEMICOLON declaration_blocks compound_statement SEMICOLON
    | FUNCTION ID DOT ID parameters COLON data_type_list SEMICOLON declaration_blocks compound_statement SEMICOLON
    """
    pass


def p_constructor_declaration(p):
    """constructor_declaration : CONSTRUCTOR ID parameters SEMICOLON
    | CONSTRUCTOR ID parameters SEMICOLON directive"""
    pass


def p_destructor_declaration(p):
    """destructor_declaration : DESTRUCTOR ID parameters SEMICOLON
    | DESTRUCTOR ID parameters SEMICOLON directive"""
    pass


def p_record_list(p):
    """record_list : record_list record_declaration
    | record_declaration"""
    pass


def p_record_declaration(p):
    """record_declaration : id_list COLON data_type_list SEMICOLON
    | CASE ID COLON data_type_list OF variant_list
    | id_list COLON data_type_list"""
    pass


def p_variant_list(p):
    """variant_list : variant_list variant
    | variant"""
    pass


def p_variant(p):
    """variant : constant_list COLON LPAREN record_list RPAREN SEMICOLON
    | constant_list COLON LPAREN RPAREN SEMICOLON"""
    pass


def p_constant_list(p):
    """constant_list : constant
    | constant_list COMMA constant"""
    pass


def p_var_declaration_block(p):
    """var_declaration_block : VAR var_list"""
    pass


def p_var_list(p):
    """var_list : var_list var_declaration
    | var_declaration"""
    pass


def p_var_declaration(p):
    """var_declaration : id_list COLON type_definition SEMICOLON
    | id_list COLON type_definition EQUAL expression SEMICOLON
    | id_list COLON type_definition ABSOLUTE ID SEMICOLON"""  # Added ABSOLUTE
    pass


def p_procedure_declaration(p):
    """procedure_declaration : procedure_header SEMICOLON directive SEMICOLON
    | procedure_header SEMICOLON declaration_blocks compound_statement SEMICOLON"""
    pass


def p_procedure_header(p):
    """procedure_header : PROCEDURE ID parameters"""
    pass


def p_directive(p):
    """directive : FORWARD
    | EXTERNAL
    | EXTERNAL STRING
    | ASM
    | INLINE
    | VIRTUAL"""
    pass


def p_function_declaration(p):
    """function_declaration : function_header SEMICOLON directive
    | function_header SEMICOLON declaration_blocks compound_statement SEMICOLON"""
    pass


def p_function_header(p):
    """function_header : FUNCTION ID parameters COLON data_type_list"""
    pass


def p_parameters(p):
    """parameters : LPAREN parameter_list RPAREN
    | empty"""
    pass


def p_parameter_list(p):
    """parameter_list : parameter_list SEMICOLON parameter_group
    | parameter_group"""
    pass


def p_parameter_group(p):
    """parameter_group : id_list COLON data_type_list
    | VAR id_list COLON data_type_list
    | CONST id_list COLON data_type_list
    | procedure_header
    | function_header"""
    pass


def p_data_type_list(p):
    """
    data_type_list : INTEGER
                   | BYTE
                   | LONGINT
                   | SHORTINT
                   | WORD
                   | REAL
                   | SINGLE
                   | DOUBLE
                   | EXTENDED
                   | SHORT
                   | BOOLEAN
                   | CHAR
                   | STRING
                   | STRING LBRACKET NUMBER RBRACKET
                   | ID
                   | ABSOLUTE ID
                   | FILE
                   | array_type
                   | pointer_type
                   | record_type
                   | set_type
                   | file_type
                   | object_type
                   | string_type"""
    pass


def p_data_type_set(p):
    """data_type_set : BYTE
    | SHORTINT
    | WORD
    | BOOLEAN
    | CHAR
    | ID"""
    pass


# Statements


def p_compound_statement(p):
    """compound_statement : BEGIN sentences_list END"""
    pass


def p_sentences_list(p):
    """sentences_list : sentences_list sentence SEMICOLON
    | sentence SEMICOLON
    | empty"""
    pass


def p_sentence(p):
    """sentence : assignment
    | procedure_call
    | compound_statement
    | if_statement
    | case_statement
    | for_statement
    | while_statement
    | repeat_statement
    | with_statement
    | goto_statement
    | labeled_sentence
    | asm_statement
    | empty"""
    pass


def p_asm_statement(p):
    """asm_statement : ASM"""
    pass


def p_assignment(p):
    """assignment : variable ASIGNATION expression
    | ID ASIGNATION expression
    """
    pass


def p_procedure_call(p):
    """procedure_call : ID
    | ID LPAREN expression_list RPAREN
    | ID LPAREN RPAREN
    | variable DOT ID LPAREN expression_list RPAREN
    | variable DOT ID LPAREN RPAREN
    | NEW LPAREN expression_list RPAREN
    | NEW LPAREN RPAREN
    | DISPOSE LPAREN expression_list RPAREN
    | DISPOSE LPAREN RPAREN"""
    pass


def p_if_statement(p):
    """if_statement : IF expression THEN sentence
    | IF expression THEN sentence ELSE sentence"""
    pass


def p_case_statement(p):
    """case_statement : CASE expression OF case_list END
    | CASE expression OF case_list ELSE sentences_list SEMICOLON END
    | CASE expression OF case_list ELSE sentences_list END"""
    pass


def p_case_list(p):
    """case_list : case_list case_label COLON sentence SEMICOLON
    | case_label COLON sentence SEMICOLON
    | empty"""
    pass


def p_case_label(p):
    """case_label : constant
    | constant DOBLEDOT constant
    | case_label COMMA constant"""
    pass


def p_for_statement(p):
    """for_statement : FOR ID ASIGNATION expression TO expression DO sentence
    | FOR ID ASIGNATION expression DOWNTO expression DO sentence
    | FOR ID IN expression DO sentence"""
    pass


def p_while_statement(p):
    """while_statement : WHILE expression DO sentence"""
    pass


def p_repeat_statement(p):
    """repeat_statement : REPEAT sentences_list UNTIL expression"""
    pass


def p_with_statement(p):
    """with_statement : WITH variable_list DO sentence"""
    pass


def p_variable_list(p):
    """variable_list : variable
    | variable_list COMMA variable"""
    pass


def p_goto_statement(p):
    """goto_statement : GOTO NUMBER"""
    pass


def p_labeled_sentence(p):
    """labeled_sentence : NUMBER COLON sentence"""
    pass


def p_empty(p):
    """empty :"""
    pass


def p_expression(p):
    """expression : expression OR simple_expression
    | expression XOR simple_expression
    | simple_expression"""
    pass


def p_simple_expression(p):
    """simple_expression : simple_expression AND relational_expression
    | relational_expression"""
    pass


def p_relational_expression(p):
    """relational_expression : relational_expression relational_operator additive_expression
    | additive_expression"""
    pass


def p_relational_operator(p):
    """relational_operator : EQUAL
    | DISTINT
    | LESS
    | LESSEQUAL
    | GREATER
    | GREATEREQUAL
    | IN"""
    pass


def p_additive_expression(p):
    """additive_expression : additive_expression PLUS multiplicative_expression
    | additive_expression MINUS multiplicative_expression
    | multiplicative_expression"""
    pass


def p_multiplicative_expression(p):
    """multiplicative_expression : multiplicative_expression TIMES unary_expression
    | multiplicative_expression DIVIDE unary_expression
    | multiplicative_expression DIV unary_expression
    | multiplicative_expression MOD unary_expression
    | multiplicative_expression SHL unary_expression
    | multiplicative_expression SHR unary_expression
    | unary_expression"""
    pass


def p_unary_expression(p):
    """unary_expression : NOT unary_expression
    | MINUS unary_expression %prec UMINUS
    | PLUS unary_expression %prec UPLUS
    | ADDRESS_OF unary_expression
    | primary_expression"""
    pass


def p_primary_expression(p):
    """primary_expression : variable
    | NUMBER
    | STRING
    | TRUE
    | FALSE
    | NIL
    | LPAREN expression RPAREN
    | function_call
    | set_constructor"""
    pass


def p_set_item(p):
    """set_item : expression
    | expression DOBLEDOT expression"""
    pass


def p_set_item_list(p):
    """set_item_list : set_item
    | set_item_list COMMA set_item"""
    pass


def p_set_constructor(p):
    """set_constructor : LBRACKET set_item_list RBRACKET
    | LBRACKET RBRACKET"""
    pass


def p_variable(p):
    """variable : ID
    | variable DOT ID
    | variable LBRACKET expression_list RBRACKET
    | variable CARET
    | LPAREN variable RPAREN CARET
    """
    pass


def p_function_call(p):
    """function_call : ID LPAREN expression_list RPAREN
    | ID LPAREN RPAREN
    | variable DOT ID LPAREN expression_list RPAREN
    | variable DOT ID LPAREN RPAREN
    """
    pass


def p_expression_list(p):
    """expression_list : expression
    | expression_list COMMA expression"""
    pass


precedence = (
    ("left", "OR", "XOR"),
    ("left", "AND"),
    ("right", "NOT"),
    (
        "nonassoc",
        "EQUAL",
        "DISTINT",
        "LESS",
        "LESSEQUAL",
        "GREATER",
        "GREATEREQUAL",
        "IN",
    ),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "DIV", "MOD", "SHL", "SHR"),
    ("right", "UMINUS", "UPLUS", "ADDRESS_OF"),
)


def p_error(p):
    if p:
        lines = p.lexer.lexdata.split("\n")
        line_num = p.lineno

        if 0 < line_num <= len(lines):
            error_line = lines[line_num - 1]
            start_of_line = p.lexer.lexdata.rfind("\n", 0, p.lexpos) + 1
            column = p.lexpos - start_of_line + 1

            print(f"\nError sintáctico en la línea {line_num}, columna {column}:")
            print(f"{line_num}: {error_line}")
            print(" " * (column - 1) + "^")
            print(f"Token inesperado '{p.value}' de tipo {p.type}")

            state = parser.statestack[-1]
            expected = [tok for tok in tokens if parser.action[state].get(tok, 0) != 0]
            if expected:
                expected_str = ", ".join(expected)
                print(f"Se esperaba uno de los siguientes tokens: {expected_str}")
            else:
                print("No se pudo determinar los tokens esperados.")

            if line_num > 1:
                print(f"{line_num-1}: {lines[line_num-2]}")
            if line_num < len(lines):
                print(f"{line_num+1}: {lines[line_num]}")
        else:
            print(
                f"\nError sintáctico en token {p.type}, valor '{p.value}', línea {p.lineno}"
            )
            print(
                f"ADVERTENCIA: La línea {p.lineno} está fuera del rango del archivo (1-{len(lines)})"
            )

        raise SyntaxError(
            f"Error de sintaxis en línea {p.lineno}, columna {column}: token inesperado '{p.type}'"
        )
    else:
        print("\nError sintáctico al final del archivo")
        raise SyntaxError("Error de sintaxis: fin de archivo inesperado")


parser = yacc.yacc()
