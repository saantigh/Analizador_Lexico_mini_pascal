import ply.yacc as yacc
from src.tokens import tokens
from src.semantic_analysis import *


def p_program(p):
    """program : program_header uses_clause declaration_blocks main_block"""
    if semantic_errors:
        print(
            f"Semantic errors detected: {len(semantic_errors)} errors found. Errors: {semantic_errors}"
        )
        p[0] = False
    else:
        print("Compilation successful. No semantic errors found.")
        p[0] = True
    pass


def p_program_header(p):
    """program_header : PROGRAM ID SEMICOLON
    | UNIT ID SEMICOLON"""
    program_name = p[2]
    kind = p[1].lower()

    symbol_table_stack[0]["__scope_name__"] = program_name
    symbol_table_stack[0]["__scope_kind__"] = kind

    p[0] = (kind, program_name)
    pass


def p_uses_clause(p):
    """uses_clause : USES id_list SEMICOLON
    | empty"""
    pass


def p_id_list(p):
    """id_list : ID
    | id_list COMMA ID"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]
    pass


def p_declaration_blocks(p):
    """declaration_blocks : declaration_blocks declaration_block
    | empty"""
    if len(p) == 3:
        if p[1] is None:
            p[0] = [p[2]]
        else:
            p[1].append(p[2])
            p[0] = p[1]
    else:
        p[0] = None
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
    if p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]]
    pass


def p_main_block(p):
    """main_block : compound_statement DOT"""
    p[0] = p[1]
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
    if p[2] is None:
        p[0] = []
    else:
        p[0] = p[2]
    pass


def p_const_list(p):
    """const_list : const_list const_declaration
    | const_declaration"""
    if len(p) == 2:

        if p[1] is not None:
            p[0] = [p[1]]
        else:
            p[0] = []
    else:
        if p[1] is None:
            p[1] = []
        if p[2] is not None:
            p[1].append(p[2])
        p[0] = p[1]


def p_const_declaration(p):
    """const_declaration : ID EQUAL constant SEMICOLON
    | ID COLON data_type_list EQUAL constant SEMICOLON"""
    const_name = p[1]
    lineno = p.lineno(1)

    if len(p) == 5:
        const_value_node = p[3]

        const_val = const_value_node
        const_type_desc = None
        if isinstance(const_val, bool):
            const_type_desc = ("PRIMITIVE", "BOOLEAN")
        elif isinstance(const_val, int):
            const_type_desc = ("PRIMITIVE", "INTEGER")
        elif isinstance(const_val, float):
            const_type_desc = ("PRIMITIVE", "REAL")
        elif isinstance(const_val, str) and const_val != "NIL_VALUE":

            if len(const_val) == 1:
                const_type_desc = ("PRIMITIVE", "CHAR")
            else:

                const_type_desc = ("STRING_LITERAL", len(const_val))
        elif const_val == "NIL_VALUE":
            const_type_desc = ("POINTER", "NIL")
        elif isinstance(const_val, tuple) and const_val[0] == "ORDINAL_CONSTANT_VALUE":
            const_type_desc = ("ORDINAL_FROM_CHAR_CODE", const_val[1])
            const_val = chr(const_val[1])
        else:

            print_semantic_error(
                f"Cannot determine type of constant '{const_name}' from value '{const_val}'.",
                lineno,
            )
            p[0] = None
            return

        add_symbol(const_name, "constant", const_type_desc,
                   lineno, value=const_val)
        p[0] = ("CONSTANT_DECL", const_name, const_type_desc, const_val)

    elif len(p) == 7:

        explicit_type_desc = p[3]
        const_value_node = p[5]
        const_val = const_value_node

        inferred_type_desc = None
        if isinstance(const_val, bool):
            inferred_type_desc = ("PRIMITIVE", "BOOLEAN")
        elif isinstance(const_val, int):
            inferred_type_desc = ("PRIMITIVE", "INTEGER")
        elif isinstance(const_val, float):
            inferred_type_desc = ("PRIMITIVE", "REAL")
        elif isinstance(const_val, str) and const_val != "NIL_VALUE":
            if len(const_val) == 1:
                inferred_type_desc = ("PRIMITIVE", "CHAR")
            else:
                inferred_type_desc = ("STRING_LITERAL", len(const_val))
        elif const_val == "NIL_VALUE":
            inferred_type_desc = ("POINTER", "NIL")
        elif isinstance(const_val, tuple) and const_val[0] == "ORDINAL_CONSTANT_VALUE":
            inferred_type_desc = ("ORDINAL_FROM_CHAR_CODE", const_val[1])
            const_val = chr(const_val[1])

        add_symbol(const_name, "constant", explicit_type_desc,
                   lineno, value=const_val)
        p[0] = ("CONSTANT_DECL_TYPED", const_name,
                explicit_type_desc, const_val)
    pass


def p_constant(p):
    """constant : NUMBER
    | STRING
    | TRUE
    | FALSE
    | NIL
    | ORDINAL_CONSTANT
    | set_constructor
    """
    token_type = p.slice[1].type
    token_value = p.slice[1].value

    if token_type == "set_constructor":
        p[0] = p[1]
        return
    if token_type == "NUMBER":
        p[0] = p[1]
    elif token_type == "STRING":
        p[0] = p[1]
    elif token_type == "TRUE":
        p[0] = True
    elif token_type == "FALSE":
        p[0] = False
    elif token_type == "NIL":
        p[0] = "NIL_VALUE"
    elif token_type == "ORDINAL_CONSTANT":
        p[0] = ("ORDINAL_CONSTANT_VALUE", token_value)
    else:
        print_semantic_error(
            f"Unexpected token type '{token_type}' for constant at line {p.lineno(1)}.",
            p.lineno(1),
        )
        p[0] = None
    pass


def p_type_declaration_block(p):
    """type_declaration_block : TYPE type_list"""
    p[0] = p[2]
    pass


def p_type_list(p):
    """type_list : type_list type_declaration
    | type_declaration"""
    pass


def p_type_declaration(p):
    """type_declaration : ID EQUAL type_definition SEMICOLON"""
    type_name = p[1]
    type_def_descriptor = p[3]
    lineno = p.lineno(1)

    if type_def_descriptor and type_def_descriptor[0] != "ERROR_TYPE":
        add_symbol(type_name, 'type', type_def_descriptor, lineno)
        p[0] = ('TYPE_DECL', type_name, type_def_descriptor)
    else:

        p[0] = None
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
    if p.slice[1].type == 'data_type_list' or isinstance(p[1], tuple):
        p[0] = p[1]

    elif p.slice[1].type == 'LPAREN':
        id_list_values = p[2]

        type_name_for_enum = f"__anonymous_enum_{p.lineno(1)}_{p.lexpos(1)}"
        enum_descriptor = ("ENUMERATED_TYPE",
                           type_name_for_enum, id_list_values)
        p[0] = enum_descriptor

        for index, enum_id_name in enumerate(id_list_values):
            add_symbol(enum_id_name, 'enum_literal',
                       enum_descriptor, p.lineno(1), value=index)

    elif p.slice[2].type == 'DOBLEDOT':
        lower_bound_val = p[1]
        upper_bound_val = p[3]
        lower_bound_token_type = p.slice[1].type

        base_type = None
        if lower_bound_token_type == 'NUMBER':
            if not (isinstance(lower_bound_val, int) and isinstance(upper_bound_val, int)):
                print_semantic_error(
                    "Subrange bounds for numbers must be integers.", p.lineno(1))
                p[0] = ("ERROR_TYPE", "Non-integer subrange bounds")
                return
            base_type = ("PRIMITIVE", "INTEGER")
        elif lower_bound_token_type == 'CHAR':
            base_type = ("PRIMITIVE", "CHAR")
        elif lower_bound_token_type == 'ID':

            lower_sym = lookup_symbol(lower_bound_val, p.lineno(1))
            upper_sym = lookup_symbol(upper_bound_val, p.lineno(3))

            if not (lower_sym and upper_sym and lower_sym['kind'] == 'constant' and upper_sym['kind'] == 'constant' and
                    is_ordinal_type(lower_sym['type']) and are_types_compatible(lower_sym['type'], upper_sym['type'])):
                print_semantic_error(
                    f"Subrange bounds '{lower_bound_val}'..'${upper_bound_val}' must be compatible ordinal constants.", p.lineno(1))
                p[0] = ("ERROR_TYPE", "Invalid ID subrange bounds")
                return
            base_type = lower_sym['type']
            lower_bound_val = lower_sym['value']
            upper_bound_val = upper_sym['value']

        else:
            print_semantic_error(
                f"Invalid base type for subrange: {lower_bound_token_type}", p.lineno(1))
            p[0] = ("ERROR_TYPE", "Invalid subrange base")
            return

        if lower_bound_val > upper_bound_val:
            print_semantic_error(
                f"Lower bound '{lower_bound_val}' exceeds upper bound '{upper_bound_val}' in subrange.", p.lineno(1))
            p[0] = ("ERROR_TYPE", "Subrange bounds out of order")
            return

        p[0] = ("SUBRANGE_TYPE", base_type, lower_bound_val, upper_bound_val)

    pass


def p_string_type(p):
    """string_type : STRING
    | STRING LBRACKET NUMBER RBRACKET"""
    if len(p) == 2:
        p[0] = ("STRING_FIXED", 255)
    else:
        length = p[3]
        if not isinstance(length, int):
            print(
                f"Semantic Error line {p.lineno(3)}: String length must be an integer. Got '{length}'."
            )
            p[0] = ("ERROR_TYPE",
                    f"Invalid string length type: {type(length)}")
        elif length <= 0 or length > 255:
            print(
                f"Semantic Error line {p.lineno(3)}: Invalid string length '{length}'. Must be a positive integer <= 255."
            )

            p[0] = ("STRING_FIXED", 255)
        else:
            p[0] = ("STRING_FIXED", length)

    pass


def p_record_type(p):
    """record_type : RECORD record_list END
    | PACKED RECORD record_list END"""
    is_packed = False
    current_idx = 1
    if p[current_idx].lower() == "packed":
        is_packed = True
        current_idx += 1
    list_of_field_or_variant_descriptors = p[current_idx + 1]

    if not isinstance(list_of_field_or_variant_descriptors, list):
        print(
            f"Semantic Error line {p.lineno(1)}: Malformed record field list.")
        p[0] = ("ERROR_TYPE", "Invalid record structure")
        return

    p[0] = ("record_type", list_of_field_or_variant_descriptors, is_packed)
    pass


def p_array_type(p):
    """array_type : ARRAY LBRACKET type_range_list RBRACKET OF data_type_list
    | PACKED ARRAY LBRACKET type_range_list RBRACKET OF data_type_list
    | ARRAY OF data_type_list
    """
    is_packed = False
    current_idx = 1

    if p[current_idx].lower() == "packed":
        is_packed = True
        current_idx += 1

    current_idx += 1

    if p[current_idx].lower() == "of":
        element_type_descriptor = p[current_idx + 1]
        print(
            f"Info line {p.lineno(1)}: 'ARRAY OF Type' construct found. Interpreted as dynamic/open array."
        )
        p[0] = ("open_array_type", element_type_descriptor, is_packed)
    elif p[current_idx] == "[":
        index_type_descriptors_list = p[current_idx + 1]
        element_type_descriptor = p[current_idx + 4]

        if (
            not isinstance(index_type_descriptors_list, list)
            or not index_type_descriptors_list
        ):
            print(
                f"Semantic Error line {p.lineno(1)}: Missing or invalid index type(s) for array."
            )
            p[0] = ("ERROR_TYPE", "Invalid array index definition")
            return
        if not element_type_descriptor:
            print(
                f"Semantic Error line {p.lineno(1)}: Missing element type for array.")
            p[0] = ("ERROR_TYPE", "Invalid array element type")
            return

        p[0] = (
            "array_type",
            index_type_descriptors_list,
            element_type_descriptor,
            is_packed,
        )
    else:
        print(
            f"Internal Error: Unexpected structure in p_array_type after ARRAY keyword at line {p.lineno(1)}."
        )
        p[0] = ("ERROR_TYPE", "Malformed array definition")
    pass


def get_bound_value_and_type(bound_token_value, bound_token_slice, bound_lineno):
    if bound_token_slice.type == "NUMBER":
        if not isinstance(bound_token_value, int):
            print(
                f"Semantic Error line {bound_lineno}: Array index bound '{bound_token_value}' must be an integer for subranges based on numbers."
            )
            return None, ("ERROR_TYPE", "Array index bound not integer")
        return bound_token_value, "INTEGER"
    elif bound_token_slice.type == "CHAR":
        return bound_token_value, "CHAR"
    elif bound_token_slice.type == "ID":
        print(
            f"Semantic Info line {bound_lineno}: ID '{bound_token_value}' in range. Assuming it's a resolvable ordinal constant for now."
        )
        return bound_token_value, ("UNRESOLVED_CONST_ID_FOR_RANGE", bound_token_value)

    print(
        f"Internal Error line {bound_lineno}: Unexpected token type '{bound_token_slice.type}' for subrange bound."
    )
    return None, ("ERROR_TYPE", "Unexpected token in subrange")


def p_type_range_list(p):
    """type_range_list : type_range
    | type_range_list COMMA type_range"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]
    pass


def p_type_range(p):
    """type_range : NUMBER DOBLEDOT NUMBER
    | NUMBER DOBLEDOT ID
    | ID DOBLEDOT NUMBER
    | CHAR DOBLEDOT CHAR
    | ID DOBLEDOT ID
    | ID"""
    if len(p) == 2:
        type_name_for_index = p[1]
        p[0] = ("ordinal_type_name_for_index", type_name_for_index)

    elif len(p) == 4:

        lower_val, lower_base_type_desc = get_bound_value_and_type(
            p[1], p.slice[1], p.lineno(1)
        )
        upper_val, upper_base_type_desc = get_bound_value_and_type(
            p[3], p.slice[3], p.lineno(3)
        )

        if (
            isinstance(lower_base_type_desc, tuple)
            and lower_base_type_desc[0] == "ERROR_TYPE"
        ) or (
            isinstance(upper_base_type_desc, tuple)
            and upper_base_type_desc[0] == "ERROR_TYPE"
        ):
            p[0] = ("subrange_error", "Error in bounds")
            return

        final_base_type = None
        if (
            isinstance(lower_base_type_desc, tuple)
            and lower_base_type_desc[0] == "UNRESOLVED_CONST_ID_FOR_RANGE"
        ):
            final_base_type = lower_base_type_desc
        elif (
            isinstance(upper_base_type_desc, tuple)
            and upper_base_type_desc[0] == "UNRESOLVED_CONST_ID_FOR_RANGE"
        ):
            final_base_type = upper_base_type_desc
        elif lower_base_type_desc != upper_base_type_desc:
            print(
                f"Semantic Error line {p.lineno(1)}: Mismatched base types ('{lower_base_type_desc}' and '{upper_base_type_desc}') for subrange bounds."
            )
            p[0] = ("subrange_error", "Mismatched bound types")
            return
        else:
            final_base_type = lower_base_type_desc

        if isinstance(lower_val, (int, str)) and isinstance(upper_val, (int, str)):
            if lower_val > upper_val:
                print(
                    f"Semantic Error line {p.lineno(1)}: Lower bound '{lower_val}' exceeds upper bound '{upper_val}' in subrange."
                )
                p[0] = ("subrange_error", "Bounds out of order")
                return
        p[0] = ("subrange_literal_for_index",
                final_base_type, lower_val, upper_val)

    else:
        print(
            f"Internal Error: Unexpected structure in p_type_range with {len(p)} elements."
        )
        p[0] = ("subrange_error", "Grammar issue")
    pass


def p_set_range(p):
    """set_range : data_type_set
    | NUMBER DOBLEDOT NUMBER
    | CHAR DOBLEDOT CHAR
    | ID"""
    if len(p) == 2:
        type_desc_or_name = p[1]

        p[0] = type_desc_or_name
    elif len(p) == 4:
        lower_bound_token_slice = p.slice[1]

        lower_val = p[1]
        upper_val = p[3]
        base_type_of_subrange = None

        if lower_bound_token_slice.type == "NUMBER":
            if not (isinstance(lower_val, int) and isinstance(upper_val, int)):
                print(
                    f"Semantic Error line {p.lineno(1)}: Set base subrange with NUMBER must use integers. Got '{lower_val}', '{upper_val}'."
                )
                p[0] = ("ERROR_TYPE", "Set subrange bounds not integer")
                return
            base_type_of_subrange = "INTEGER"
        elif lower_bound_token_slice.type == "CHAR":
            base_type_of_subrange = "CHAR"
        else:
            print(
                f"Internal Error: Unexpected token type '{lower_bound_token_slice.type}' for set subrange base at line {p.lineno(1)}."
            )
            p[0] = ("ERROR_TYPE", "Invalid set subrange literal type")
            return

        if lower_val > upper_val:
            print(
                f"Semantic Error line {p.lineno(1)}: Lower bound '{lower_val}' exceeds upper bound '{upper_val}' in set base subrange."
            )
            p[0] = ("ERROR_TYPE", "Set subrange bounds out of order")
            return

        p[0] = ("subrange_as_set_base",
                base_type_of_subrange, lower_val, upper_val)

    else:
        print(
            f"Internal Error: Unexpected structure in p_set_range at line {p.lineno(1)}"
        )
        p[0] = ("ERROR_TYPE", "Malformed set range")
    pass


def p_set_type(p):
    """set_type : SET OF set_range"""
    base_type_descriptor = p[3]

    p[0] = ("set_type", base_type_descriptor)

    pass


def p_pointer_type(p):
    """pointer_type : CARET ID
    | CARET data_type_list"""
    target_type_descriptor = p[2]
    p[0] = ("pointer_type", target_type_descriptor)
    pass


def p_file_type(p):
    """file_type : FILE OF data_type_list
    | FILE"""
    if len(p) == 2:
        p[0] = ("file_type", "CHAR")
    else:
        component_type_descriptor = p[3]
        p[0] = ("file_type", component_type_descriptor)
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
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]
    pass


def p_record_declaration(p):
    """record_declaration : id_list COLON data_type_list SEMICOLON
    | CASE ID COLON data_type_list OF variant_list
    | id_list COLON data_type_list"""
    if len(p) == 7:
        if isinstance(p[1], str) and p[1].upper() == 'CASE':
            tag_id_name = p[2]
            tag_type_descriptor = p[4]
            variants_list = p[6]
            p[0] = ("variant_part_tag", tag_id_name,
                    tag_type_descriptor, variants_list)
        else:
            print(f"Internal Error: p_record_declaration len 7 but p[1] is not CASE ({p[1]})")
            p[0] = ("record_decl_error", "Grammar dispatch error len 7")
    elif len(p) == 5:
        list_of_ids = p[1]
        field_type_descriptor = p[3]
        p[0] = ("fixed_field", list_of_ids, field_type_descriptor)
    elif len(p) == 4:
        list_of_ids = p[1]
        field_type_descriptor = p[3]
        p[0] = ("fixed_field", list_of_ids, field_type_descriptor) 
    else:
        print(f"Internal Error: p_record_declaration with unexpected len(p) = {len(p)}")
        p[0] = ("record_decl_error", "Unexpected rule length")
    pass


def p_variant_list(p):
    """variant_list : variant_list variant
    | variant"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]
    pass


def p_variant(p):
    """variant : constant_list COLON LPAREN record_list RPAREN SEMICOLON
    | constant_list COLON LPAREN RPAREN SEMICOLON"""
    list_of_case_constants = p[1]
    fields = []

    if len(p) == 7:
        fields = p[4]
    elif len(p) != 6:
        print(
            f"Internal Error: Unexpected structure in p_variant with {len(p)} elements."
        )
        p[0] = ("variant_error", "Grammar issue")
        return

    p[0] = ("variant_case", list_of_case_constants, fields)
    pass


def p_constant_list(p):
    """constant_list : constant
    | constant_list COMMA constant"""
    pass


def p_var_declaration_block(p):
    """var_declaration_block : VAR var_list"""
    if p[2] is None:
        p[0] = []
    else:
        p[0] = p[2]
    pass


def p_var_list(p):
    """var_list : var_list var_declaration
    | var_declaration"""
    pass


def p_var_declaration(p):
    """var_declaration : id_list COLON type_definition SEMICOLON
    | id_list COLON type_definition EQUAL expression SEMICOLON
    | id_list COLON type_definition ABSOLUTE ID SEMICOLON"""
    id_list_names = p[1]
    type_desc = p[3]
    lineno = p.lineno(1) if id_list_names else p.lineno(2)

    if not id_list_names:
        print_semantic_error(
            "Missing identifier(s) in var declaration.", p.lineno(2))
        p[0] = None
        return

    if not type_desc or (isinstance(type_desc, tuple) and type_desc[0] == "ERROR_TYPE"):
        print_semantic_error(
            f"Invalid type for variables '{', '.join(id_list_names)}'. Type error was: {type_desc[1] if isinstance(type_desc, tuple) else 'Unknown'}", lineno)

        p[0] = None
        return

    declaration_results = []

    for var_name in id_list_names:

        initial_value_expr_type = None
        absolute_var_target = None

        if len(p) == 5:
            add_symbol(var_name, 'variable', type_desc, p.lineno(1))
            declaration_results.append(('VAR_DECL', var_name, type_desc))

        elif len(p) == 7 and p[4].lower() == '=':

            initial_value_expr_type = p[5]

            if not initial_value_expr_type or initial_value_expr_type[0] == "ERROR_TYPE":
                print_semantic_error(
                    f"Invalid type in initializer for variable '{var_name}'.", p.lineno(5))
            elif not are_types_compatible(type_desc, initial_value_expr_type, for_assignment=True):
                print_semantic_error(
                    f"Type mismatch for variable '{var_name}'. Cannot initialize with type '{initial_value_expr_type}' (expected '{type_desc}').", p.lineno(5))

            add_symbol(var_name, 'variable', type_desc, p.lineno(1))
            declaration_results.append(
                ('VAR_DECL_INIT', var_name, type_desc, initial_value_expr_type))

        elif len(p) == 7 and p[4].lower() == 'absolute':
            absolute_var_name = p[5]
            absolute_var_symbol = lookup_symbol(absolute_var_name, p.lineno(5))

            if not absolute_var_symbol:

                pass
            elif absolute_var_symbol['kind'] != 'variable':
                print_semantic_error(
                    f"Identifier '{absolute_var_name}' for ABSOLUTE must be a variable.", p.lineno(5))
            else:

                symbol_entry = add_symbol(
                    var_name, 'variable', type_desc, p.lineno(1))
                if symbol_entry:

                    current_scope = symbol_table_stack[-1]
                    current_scope[var_name.lower(
                    )]['absolute_target'] = absolute_var_name
                declaration_results.append(
                    ('VAR_DECL_ABS', var_name, type_desc, absolute_var_name))
    pass


def p_procedure_declaration(p):
    """procedure_declaration : procedure_header SEMICOLON directive
    | procedure_header SEMICOLON declaration_blocks compound_statement SEMICOLON"""
    proc_name, param_descriptors, proc_header_lineno = p[1]

    parent_scope_dict = None
    if len(symbol_table_stack) > 1:
        parent_scope_dict = symbol_table_stack[-2]
    else:

        if current_scope_level > 0:
            parent_scope_dict = symbol_table_stack[current_scope_level-1]
        else:
            parent_scope_dict = symbol_table_stack[0]

    proc_type_desc = ('PROCEDURE_TYPE', param_descriptors, None)

    try:
        if len(p) == 5:
            directive_node = p[3]
            is_fwd = (directive_node[0].upper() == 'FORWARD')

            add_symbol(name=proc_name, kind='procedure',
                       type_desc=proc_type_desc, lineno=proc_header_lineno,
                       params=param_descriptors,
                       defined=not is_fwd,
                       is_forward_declaration_itself=is_fwd,
                       target_scope_dict=parent_scope_dict)

            p[0] = ('PROC_DECL_DIRECTIVE', proc_name,
                    param_descriptors, directive_node)

        elif len(p) == 6:

            add_symbol(name=proc_name, kind='procedure',
                       type_desc=proc_type_desc, lineno=proc_header_lineno,
                       params=param_descriptors,
                       defined=True,
                       is_forward_declaration_itself=False,
                       target_scope_dict=parent_scope_dict)

            local_declarations = p[3]
            body_stmts = p[4]
            p[0] = ('PROC_DEF', proc_name, param_descriptors,
                    local_declarations, body_stmts)
    finally:
        exit_scope()
    pass


def p_procedure_header(p):
    """procedure_header : PROCEDURE ID parameters"""
    proc_name = p[2]

    param_descriptors = p[3] if p[3] is not None else []
    header_lineno = p.lineno(1)

    enter_scope(f"procedure_{proc_name}")

    processed_param_names = set()
    for param_info in param_descriptors:

        if param_info['name'].lower() in processed_param_names:
            print_semantic_error(
                f"Duplicate parameter name '{param_info['name']}' in procedure '{proc_name}'.", param_info['lineno'])
        else:
            add_symbol(name=param_info['name'],
                       kind='parameter',
                       type_desc=param_info['type'],

                       lineno=param_info['lineno'],
                       value={'mode': param_info['mode']})
            processed_param_names.add(param_info['name'].lower())

    p[0] = (proc_name, param_descriptors, header_lineno)

    pass


def p_directive(p):
    """directive : FORWARD
    | EXTERNAL
    | EXTERNAL STRING
    | ASM
    | INLINE
    | VIRTUAL"""
    if len(p) == 2:
        p[0] = (p[1].upper(),)
    elif len(p) == 3:
        p[0] = (p[1].upper(), p[2])
    pass


def p_function_declaration(p):
    """function_declaration : function_header SEMICOLON directive
    | function_header SEMICOLON declaration_blocks compound_statement SEMICOLON"""
    func_name, param_descriptors, return_type_desc, func_header_lineno = p[1]

    parent_scope_dict = None
    if current_scope_level > 0:
        parent_scope_dict = symbol_table_stack[current_scope_level-1]
    else:
        parent_scope_dict = symbol_table_stack[0]

    func_type_desc = ('FUNCTION_TYPE', param_descriptors, return_type_desc)

    if not return_type_desc or (isinstance(return_type_desc, tuple) and return_type_desc[0] == "ERROR_TYPE"):
        print_semantic_error(
            f"Cannot declare function '{func_name}' due to invalid return type.", func_header_lineno)

        if p.slice[1].type == 'function_header':
            exit_scope()
        p[0] = None
        return

    try:
        if len(p) == 4:
            directive_node = p[3]
            is_fwd = (directive_node[0].upper() == 'FORWARD')

            add_symbol(name=func_name, kind='function',
                       type_desc=func_type_desc, lineno=func_header_lineno,
                       params=param_descriptors,
                       defined=not is_fwd,
                       is_forward_declaration_itself=is_fwd,
                       target_scope_dict=parent_scope_dict)

            p[0] = ('FUNC_DECL_DIRECTIVE', func_name,
                    param_descriptors, return_type_desc, directive_node)

        elif len(p) == 6:
            add_symbol(name=func_name, kind='function',
                       type_desc=func_type_desc, lineno=func_header_lineno,
                       params=param_descriptors,
                       defined=True,
                       is_forward_declaration_itself=False,
                       target_scope_dict=parent_scope_dict)

            local_declarations = p[3]
            body_stmts = p[4]
            p[0] = ('FUNC_DEF', func_name, param_descriptors,
                    return_type_desc, local_declarations, body_stmts)
    finally:
        exit_scope()
    pass


def p_function_header(p):
    """function_header : FUNCTION ID parameters COLON data_type_list"""
    func_name = p[2]
    param_descriptors = p[3] if p[3] is not None else []
    return_type_desc = p[5]
    header_lineno = p.lineno(1)

    if isinstance(return_type_desc, tuple) and return_type_desc[0] == 'file_type':
        print_semantic_error(
            f"Functions cannot return FILE types. Function '{func_name}' at line {header_lineno}.", header_lineno)

    enter_scope(f"function_{func_name}")

    processed_param_names = set()
    for param_info in param_descriptors:
        if param_info['name'].lower() in processed_param_names:
            print_semantic_error(
                f"Duplicate parameter name '{param_info['name']}' in function '{func_name}'.", param_info['lineno'])
        else:
            add_symbol(name=param_info['name'],
                       kind='parameter',
                       type_desc=param_info['type'],
                       lineno=param_info['lineno'],
                       value={'mode': param_info['mode']})
            processed_param_names.add(param_info['name'].lower())

    if not (isinstance(return_type_desc, tuple) and return_type_desc[0] == "ERROR_TYPE"):
        add_symbol(name=func_name,
                   kind='return_variable',
                   type_desc=return_type_desc,
                   lineno=header_lineno)

    p[0] = (func_name, param_descriptors, return_type_desc, header_lineno)

    pass


def p_parameters(p):
    """parameters : LPAREN parameter_list RPAREN
    | empty"""
    if len(p) == 4:
        param_list = p[2]
        if param_list is None:
            p[0] = []
        else:
            p[0] = param_list
    pass


def p_parameter_list(p):
    """parameter_list : parameter_list SEMICOLON parameter_group
    | parameter_group"""
    if len(p) == 4:
        p[1].extend(p[3])
        p[0] = p[1]
    else:
        p[0] = p[1]
    pass


def p_parameter_group(p):
    """parameter_group : id_list COLON data_type_list
    | VAR id_list COLON data_type_list
    | CONST id_list COLON data_type_list
    | procedure_header
    | function_header"""
    params_in_group = []
    param_mode = 'value'
    id_list_idx = 1
    type_list_idx = 3
    first_symbol_of_rule = p.slice[1]

    if hasattr(first_symbol_of_rule, 'type') and first_symbol_of_rule.type in ['PROCEDURE', 'FUNCTION']:
        header_info = p[1]
        print_semantic_error(
            f"Procedural/functional parameters ('{header_info[0]}') are not fully supported yet at line {p.lineno(1)}.", p.lineno(1))
        p[0] = []
        return

    elif hasattr(first_symbol_of_rule, 'type') and first_symbol_of_rule.type == 'VAR':
        param_mode = 'var'
        id_list_idx = 2
        type_list_idx = 4

    elif hasattr(first_symbol_of_rule, 'type') and first_symbol_of_rule.type == 'CONST':

        param_mode = 'const'
        id_list_idx = 2
        type_list_idx = 4
    else:
        pass
    id_names_list = p[id_list_idx]
    param_type_desc = p[type_list_idx]

    param_lineno = p.lineno(id_list_idx)

    if not isinstance(id_names_list, list):

        print_semantic_error(f"Internal error: Expected id_list to be a list in parameter group. Got: {type(id_names_list)}", param_lineno)
        p[0] = []
        return

    if not param_type_desc or (isinstance(param_type_desc, tuple) and param_type_desc[0] == "ERROR_TYPE"):
        print_semantic_error(
            f"Invalid type for parameters '{', '.join(id_names_list)}'. Type error: {param_type_desc[1] if isinstance(param_type_desc, tuple) else 'Unknown'}", param_lineno)
        p[0] = []
        return

    for param_name in id_names_list:
        if param_mode == 'var' and isinstance(param_type_desc, tuple) and param_type_desc[0] == 'file_type':
            print_semantic_error(
                f"VAR parameter '{param_name}' cannot be of a FILE type.", param_lineno)

        params_in_group.append({
            'name': param_name,
            'type': param_type_desc,
            'mode': param_mode,
            'lineno': param_lineno
        })

    p[0] = params_in_group
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
    type_token = p.slice[1].type
    type_val = p.slice[1].value

    if len(p) == 2:
        if type_token == "ID":

            p[0] = get_type_descriptor(type_val, p.lineno(1))

        elif type_token == "STRING":
            p[0] = ("STRING_DEFAULT", 255)

        elif type_token == "INTEGER":
            p[0] = ("PRIMITIVE", "INTEGER")
        elif type_token == "REAL":
            p[0] = ("PRIMITIVE", "REAL")
        elif type_token == "BOOLEAN":
            p[0] = ("PRIMITIVE", "BOOLEAN")
        elif type_token == "CHAR":
            p[0] = ("PRIMITIVE", "CHAR")
        elif type_token == "BYTE":
            p[0] = ("PRIMITIVE", "BYTE")
        elif type_token == "SHORTINT":
            p[0] = ("PRIMITIVE", "SHORTINT")
        elif type_token == "WORD":
            p[0] = ("PRIMITIVE", "WORD")
        elif type_token == "LONGINT":
            p[0] = ("PRIMITIVE", "LONGINT")

        else:

            p[0] = p[1]

    elif type_token == "STRING" and p[2] == "[":
        length = p[3]
        if not isinstance(length, int) or length <= 0 or length > 255:
            print_semantic_error(
                f"Invalid string length '{length}'. Must be a positive integer <= 255.",
                p.lineno(3),
            )
            p[0] = ("STRING_FIXED", 255)
        else:
            p[0] = ("STRING_FIXED", length)
    else:

        p[0] = p[1]

    pass


def p_data_type_set(p):
    """data_type_set : BYTE
    | SHORTINT
    | WORD
    | BOOLEAN
    | CHAR
    | ID"""
    if p.slice[1].type == "WORD":
        print(
            f"Warning line {p.lineno(1)}: WORD used as set base type. Typical sets are limited to 256 elements. Check compiler specifics."
        )

    p[0] = p.slice[1].type
    if p.slice[1].type == "ID":
        p[0] = p[1]
    pass


def p_compound_statement(p):
    """compound_statement : BEGIN sentences_list END"""
    p[0] = p[2]
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
    | variable PLUS_ASIGN    expression
    | ID       PLUS_ASIGN    expression
    | variable MINUS_ASIGN   expression
    | ID       MINUS_ASIGN   expression
    | variable TIMES_ASIGN   expression
    | ID       TIMES_ASIGN   expression
    | variable DIVIDE_ASIGN  expression
    | ID       DIVIDE_ASIGN  expression
    | variable EQUAL         expression
    | ID       EQUAL         expression
    """
    target_is_simple_id = (len(p.slice) > 1 and p.slice[1].type == 'ID' and p.slice[2].type != 'DOT' and p.slice[2].type != 'LBRACKET' and p.slice[2].type != 'CARET') 

    target_type = None
    target_name_for_id_case = None
    lineno_assign = p.lineno(2)

    if target_is_simple_id:
        target_name_for_id_case = p[1]
        target_symbol = lookup_symbol(target_name_for_id_case, p.lineno(1))
        if target_symbol:
            if target_symbol['kind'] in ['variable', 'parameter', 'return_variable', 'field']:
                target_type = target_symbol['type']
                if target_symbol['kind'] == 'parameter' and target_symbol.get('value', {}).get('mode') == 'const':
                    print_semantic_error(f"Cannot assign to CONST parameter '{target_name_for_id_case}'.", p.lineno(1))
                    target_type = ("ERROR_TYPE", "Assign to const param")
            elif target_symbol['kind'] == 'constant':
                print_semantic_error(f"Cannot assign to a constant '{target_name_for_id_case}'.", p.lineno(1))
                target_type = ("ERROR_TYPE", "Assign to const")
            else:
                print_semantic_error(f"Identifier '{target_name_for_id_case}' is not assignable (kind: {target_symbol['kind']}).", p.lineno(1))
                target_type = ("ERROR_TYPE", "Not assignable")
        else:

            target_type = ("ERROR_TYPE", f"Undeclared target: {target_name_for_id_case}")
    else:
        target_type = p[1]

    expr_type = p[3]
    op_assign = p.slice[2].type

    if not target_type or target_type[0] == "ERROR_TYPE" or \
       not expr_type or expr_type[0] == "ERROR_TYPE":

        p[0] = None
        return

    if op_assign == 'ASIGNATION':
        if not are_types_compatible(target_type, expr_type, context="assignment"):
            print_semantic_error(f"Type mismatch in assignment. Cannot assign {expr_type} to {target_type}.", lineno_assign)
    else:
        temp_op = None
        if op_assign == 'PLUS_ASIGN': temp_op = '+'
        elif op_assign == 'MINUS_ASIGN': temp_op = '-'
        elif op_assign == 'TIMES_ASIGN': temp_op = '*'
        elif op_assign == 'DIVIDE_ASIGN': temp_op = '/'
        if temp_op:
            intermediate_result_type = get_result_type(temp_op, target_type, expr_type, lineno_assign)
            if intermediate_result_type[0] != "ERROR_TYPE":
                if not are_types_compatible(target_type, intermediate_result_type, context="assignment"):
                    print_semantic_error(f"Type mismatch in compound assignment '{op_assign}'. Result of ({target_type} {temp_op} {expr_type}) is {intermediate_result_type}, which is not assignable to {target_type}.", lineno_assign)

        else:
            print_semantic_error(f"Unsupported compound assignment operator '{op_assign}'.", lineno_assign)
    p[0] = None
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
    call_name_token_idx = 1
    is_method_call = False
    is_special_call = False
    proc_name = None
    arg_expr_types_list = []
    lineno_call = 0

    if p.slice[1].type == 'ID':
        if len(p) > 2 and p.slice[2].type == 'DOT':
            is_method_call = True

            proc_name = p[3]
            call_name_token_idx = 3
            lineno_call = p.lineno(3)
            if len(p) == 7:
                arg_expr_types_list = p[5] if p[5] else []

        else:
            proc_name = p[1]
            call_name_token_idx = 1
            lineno_call = p.lineno(1)
            if len(p) == 5:
                arg_expr_types_list = p[3] if p[3] else []
    elif p.slice[1].type in ['NEW', 'DISPOSE']:
        is_special_call = True
        proc_name = p[1].upper()
        call_name_token_idx = 1
        lineno_call = p.lineno(1)
        if len(p) == 5:
            arg_expr_types_list = p[3] if p[3] else []
        elif len(p) == 4 :
            print_semantic_error(f"Procedure '{proc_name}' requires arguments.", lineno_call)
            return
    if is_special_call:
        if proc_name == 'NEW':
            if not arg_expr_types_list or len(arg_expr_types_list) != 1:
                print_semantic_error(f"Procedure 'NEW' requires exactly one pointer variable argument.", lineno_call)
                return
            arg_type = arg_expr_types_list[0]
            if not is_pointer_type(arg_type):
                print_semantic_error(f"Argument for 'NEW' must be a pointer type, got {arg_type}.", lineno_call)
                return
        elif proc_name == 'DISPOSE':
            if not arg_expr_types_list or len(arg_expr_types_list) != 1:
                print_semantic_error(f"Procedure 'DISPOSE' requires exactly one pointer variable argument.", lineno_call)
                return
            arg_type = arg_expr_types_list[0]
            if not is_pointer_type(arg_type) or arg_type[1] == "NIL":
                print_semantic_error(f"Argument for 'DISPOSE' must be a non-NIL pointer type, got {arg_type}.", lineno_call)
                return
        return

    if is_method_call:
        print_semantic_error(f"Object method calls ('{proc_name}') are not fully supported yet.", lineno_call)
        return

    if not proc_name:
        print_semantic_error(f"Could not identify procedure name in call at line {p.lineno(1)}.", p.lineno(1))
        return

    proc_symbol = lookup_symbol(proc_name, lineno_call)

    if not proc_symbol:
        return
    kind = proc_symbol.get('kind')

    if kind not in ['procedure', 'predefined_procedure']:
        if kind == 'function' or kind == 'predefined_function':
            print_semantic_error(f"Function '{proc_name}' cannot be called as a procedure (result is discarded). Some Pascals allow this, but it's often a bug.", lineno_call)

            return
        else:
            print_semantic_error(f"Identifier '{proc_name}' is not a procedure (kind: {kind}).", lineno_call)
            return

    if not proc_symbol.get('defined', False) and proc_symbol.get('is_forward', False):
        print_semantic_error(f"Cannot call procedure '{proc_name}' as it only has a FORWARD declaration without a body.", lineno_call)
        return

    defined_params = []
    if kind == 'procedure':

        defined_params = proc_symbol.get('params', [])
    elif kind == 'predefined_procedure':

        params_ok = proc_symbol['params_check_func'](arg_expr_types_list, lineno_call)
        if not params_ok:
            pass
        return

    if len(arg_expr_types_list) != len(defined_params):
        print_semantic_error(f"Incorrect number of arguments for procedure '{proc_name}'. Expected {len(defined_params)}, got {len(arg_expr_types_list)}.", lineno_call)
        return

    for i, arg_actual_type in enumerate(arg_expr_types_list):
        param_formal_info = defined_params[i]
        param_formal_type = param_formal_info['type']
        param_formal_mode = param_formal_info['mode']

        if arg_actual_type is None or arg_actual_type[0] == "ERROR_TYPE":

            print_semantic_error(f"Invalid argument {i+1} for procedure '{proc_name}' due to previous error in expression.", lineno_call)
            return

        if param_formal_mode == 'var':
            if param_formal_type != arg_actual_type:
                print_semantic_error(f"Argument {i+1} for VAR parameter '{param_formal_info['name']}' of procedure '{proc_name}' type mismatch. Expected identical type {param_formal_type}, got {arg_actual_type}.", lineno_call)
                return

        elif param_formal_mode == 'const':

            if not are_types_compatible(param_formal_type, arg_actual_type, context="assignment"):
                print_semantic_error(f"Argument {i+1} for CONST parameter '{param_formal_info['name']}' of procedure '{proc_name}' type mismatch. Expected compatible with {param_formal_type}, got {arg_actual_type}.", lineno_call)
                return
        else:
            if not are_types_compatible(param_formal_type, arg_actual_type, context="assignment"):
                print_semantic_error(f"Argument {i+1} for parameter '{param_formal_info['name']}' of procedure '{proc_name}' type mismatch. Expected compatible with {param_formal_type}, got {arg_actual_type}.", lineno_call)
                return
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
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1 = p[1]
        type2 = p[3]
        operator = p[2].upper()
        p[0] = get_result_type(operator, type1, type2, p.lineno(2))
    pass


def p_simple_expression(p):
    """simple_expression : simple_expression AND relational_expression
    | relational_expression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1 = p[1]
        type2 = p[3]
        p[0] = get_result_type("AND", type1, type2, p.lineno(2))
    pass


def p_relational_expression(p):
    """relational_expression : relational_expression relational_operator additive_expression
    | additive_expression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1 = p[1]
        operator = p[2]
        type2 = p[3]
        p[0] = get_result_type(operator, type1, type2, p.lineno(2))
    pass


def p_relational_operator(p):
    """relational_operator : EQUAL
    | DISTINT
    | LESS
    | LESSEQUAL
    | GREATER
    | GREATEREQUAL
    | IN"""
    p[0] = p[1].upper()
    pass


def p_additive_expression(p):
    """additive_expression : additive_expression PLUS multiplicative_expression
    | additive_expression MINUS multiplicative_expression
    | multiplicative_expression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1 = p[1]
        operator = p[2].upper()
        type2 = p[3]
        p[0] = get_result_type(operator, type1, type2, p.lineno(2))
    pass


def p_multiplicative_expression(p):
    """multiplicative_expression : multiplicative_expression TIMES unary_expression
    | multiplicative_expression DIVIDE unary_expression
    | multiplicative_expression DIV unary_expression
    | multiplicative_expression MOD unary_expression
    | multiplicative_expression SHL unary_expression
    | multiplicative_expression SHR unary_expression
    | unary_expression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        type1 = p[1]
        operator = p[2].upper()
        type2 = p[3]
        p[0] = get_result_type(operator, type1, type2, p.lineno(2))
    pass


def p_unary_expression(p):
    """unary_expression : NOT unary_expression
    | MINUS unary_expression %prec UMINUS
    | PLUS unary_expression %prec UPLUS
    | ADDRESS_OF unary_expression
    | primary_expression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        operator = p.slice[1].type
        operand_type = p[2]
        p[0] = get_result_type(operator, operand_type, lineno=p.lineno(1))
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
    token_slice = p.slice[1]

    if token_slice.type == 'variable':
        p[0] = p[1]
    elif token_slice.type == 'NUMBER':
        if isinstance(p[1], int):
            p[0] = ("PRIMITIVE", "INTEGER")
        elif isinstance(p[1], float):
            p[0] = ("PRIMITIVE", "REAL")
        else:
            p[0] = ("ERROR_TYPE", "Unknown number literal type")
    elif token_slice.type == 'STRING':

        if len(p[1]) == 1:
            p[0] = ("PRIMITIVE", "CHAR")
        else:
            p[0] = ("STRING_LITERAL", len(p[1]))
    elif token_slice.type == 'TRUE' or token_slice.type == 'FALSE':
        p[0] = ("PRIMITIVE", "BOOLEAN")
    elif token_slice.type == 'NIL':
        p[0] = ("POINTER", "NIL")
    elif token_slice.type == 'LPAREN':
        p[0] = p[2]
    elif token_slice.type == 'function_call':
        p[0] = p[1]
    elif token_slice.type == 'set_constructor':
        p[0] = p[1]
    else:
        print_semantic_error(
            f"Unhandled primary expression element: {p.slice[1].type}", p.lineno(1))
        p[0] = ("ERROR_TYPE", "Unknown primary expression")
    pass


def p_set_item(p):
    """set_item : expression
    | expression DOBLEDOT expression"""
    if len(p) == 2:
        expr_type = p[1]
        if not is_ordinal_type(expr_type):
            print_semantic_error(f"Set elements must be of an ordinal type, got {expr_type}.", p.lineno(1))
            p[0] = (("ERROR_TYPE", "Non-ordinal set element"), None)
        else:
            p[0] = (expr_type, None)
    else:
        type1 = p[1]
        type2 = p[3]
        if not (is_ordinal_type(type1) and is_ordinal_type(type2)):
            print_semantic_error(f"Set range bounds must be ordinal types, got {type1} and {type2}.", p.lineno(1))
            p[0] = (("ERROR_TYPE", "Non-ordinal set range"), None)
        elif not are_types_compatible(type1, type2, context="comparison"):
            print_semantic_error(f"Set range bounds type mismatch: {type1} vs {type2}.", p.lineno(1))
            p[0] = (("ERROR_TYPE", "Mismatched set range types"), None)
        else:
            p[0] = (type1, type2)
    pass


def p_set_item_list(p):
    """set_item_list : set_item
    | set_item_list COMMA set_item"""
    if len(p) == 2:
        item_desc = p[1]
        p[0] = [item_desc]
    else:
        p[1].append(p[3])
        p[0] = p[1]
    pass


def p_set_constructor(p):
    """set_constructor : LBRACKET set_item_list RBRACKET
    | LBRACKET RBRACKET"""
    if len(p) == 3:
        p[0] = ("SET_LITERAL_VALUE", [])
    else:
        base_type_of_elements = None
        item_descriptors_list = p[2]
        has_error = False

        for item_desc in item_descriptors_list:
            type_lower, type_upper = item_desc
            if type_lower[0] == "ERROR_TYPE" or (type_upper and type_upper[0] == "ERROR_TYPE"):
                has_error = True
                base_type_of_elements = ("ERROR_TYPE", "Error in set element/range")
                break

            current_item_base_type = type_lower
            if not is_ordinal_type(current_item_base_type):
                print_semantic_error(f"Set elements/ranges must be ordinal. Found {current_item_base_type}.", p.lineno(1))
                has_error = True
                base_type_of_elements = ("ERROR_TYPE", "Non-ordinal in set literal")
                break
            if base_type_of_elements is None:
                base_type_of_elements = current_item_base_type
            elif not are_ordinal_types_compatible_for_set(base_type_of_elements, current_item_base_type):
                print_semantic_error(f"Inconsistent element types in set constructor. Expected compatible with {base_type_of_elements}, got {current_item_base_type}.", p.lineno(1))
                has_error = True
                base_type_of_elements = ("ERROR_TYPE", "Inconsistent set element types")
                break
        if has_error:
            p[0] = ("ERROR_TYPE", base_type_of_elements[1] if isinstance(base_type_of_elements, tuple) else "Set literal error")
        else:
            p[0] = ("SET_LITERAL_VALUE", base_type_of_elements, item_descriptors_list)

    pass


def p_variable(p):
    """variable : ID
    | variable DOT ID
    | variable LBRACKET expression_list RBRACKET
    | variable CARET
    | LPAREN variable RPAREN CARET
    """
    if len(p) == 2 and p.slice[1].type == 'ID':
        var_name = p[1]
        symbol_info = lookup_symbol(var_name, p.lineno(1))
        if symbol_info:
            if symbol_info['kind'] in ['variable', 'constant', 'parameter', 'return_variable', 'enum_literal']:
                p[0] = symbol_info['type']

            elif symbol_info['kind'] == 'function' and not symbol_info.get('params'):

                print_semantic_error(
                    f"Cannot use function '{var_name}' as a variable here (did you mean to call it?).", p.lineno(1))
                p[0] = ("ERROR_TYPE", f"Function {var_name} used as variable")
            else:
                print_semantic_error(
                    f"Identifier '{var_name}' is not a variable, constant or parameter (kind: {symbol_info['kind']}).", p.lineno(1))
                p[0] = ("ERROR_TYPE", f"Not a variable: {var_name}")
        else:

            p[0] = ("ERROR_TYPE", f"Undeclared variable: {var_name}")

    elif p.slice[2].type == 'DOT':
        record_var_type = p[1]
        field_name = p[3].lower()
        lineno_field = p.lineno(3)

        if not record_var_type or record_var_type[0] == "ERROR_TYPE":
            p[0] = record_var_type
            return

        actual_record_type = record_var_type
        if record_var_type[0] == 'POINTER':
            actual_record_type = record_var_type[1]
            if not actual_record_type or actual_record_type[0] == "ERROR_TYPE":
                print_semantic_error(
                    f"Pointer does not point to a valid type for field access of '{field_name}'.", lineno_field)
                p[0] = ("ERROR_TYPE", "Invalid pointer deref for field")
                return

        if actual_record_type[0] == 'record_type':

            found_field_type = None
            fields_and_variants = actual_record_type[1]
            for field_desc in fields_and_variants:
                if field_desc[0] == 'fixed_field':
                    if field_name in [name.lower() for name in field_desc[1]]:
                        found_field_type = field_desc[2]
                        break

            if found_field_type:
                p[0] = found_field_type
            else:
                print_semantic_error(
                    f"Field '{field_name}' not found in record type {actual_record_type}.", lineno_field)
                p[0] = ("ERROR_TYPE", f"Unknown field {field_name}")
        else:
            print_semantic_error(
                f"Left side of '.' operator must be a record or pointer to record, got {record_var_type}.", p.lineno(1))
            p[0] = ("ERROR_TYPE", "Not a record for DOT access")

    elif p.slice[2].type == 'LBRACKET':
        array_var_type = p[1]

        index_expr_types = p[3]
        lineno_bracket = p.lineno(2)

        if not array_var_type or array_var_type[0] == "ERROR_TYPE":
            p[0] = array_var_type
            return

        if array_var_type[0] == 'array_type':

            defined_index_types = array_var_type[1]
            element_type = array_var_type[2]

            if len(index_expr_types) != len(defined_index_types):
                print_semantic_error(
                    f"Incorrect number of dimensions for array access. Expected {len(defined_index_types)}, got {len(index_expr_types)}.", lineno_bracket)
                p[0] = ("ERROR_TYPE", "Array dimension mismatch")
                return

            valid_indices = True
            for i, expr_idx_type in enumerate(index_expr_types):
                def_idx_type_info = defined_index_types[i]

                if not is_ordinal_type(expr_idx_type):
                    print_semantic_error(
                        f"Array index for dimension {i+1} must be an ordinal type, got {expr_idx_type}.", lineno_bracket)
                    valid_indices = False
                    break

            if valid_indices:
                p[0] = element_type
            else:
                p[0] = ("ERROR_TYPE", "Invalid array index type")

        elif is_string_type(array_var_type):
            if len(index_expr_types) == 1:
                if is_integer_type(index_expr_types[0]):
                    p[0] = ("PRIMITIVE", "CHAR")
                else:
                    print_semantic_error(
                        f"String index must be an INTEGER, got {index_expr_types[0]}.", lineno_bracket)
                    p[0] = ("ERROR_TYPE", "Invalid string index type")
            else:
                print_semantic_error(
                    f"String access requires one INTEGER index, got {len(index_expr_types)} indices.", lineno_bracket)
                p[0] = ("ERROR_TYPE", "String index dimension error")
        else:
            print_semantic_error(
                f"Identifier '{p[1] if isinstance(p[1],str) else 'expression'}' is not an array or string type for [] access, got {array_var_type}.", p.lineno(1))
            p[0] = ("ERROR_TYPE", "Not an array/string for []")

    elif p.slice[-1].type == 'CARET':
        ptr_var_type = p[1]
        lineno_caret = p.lineno(len(p)-1)

        if not ptr_var_type or ptr_var_type[0] == "ERROR_TYPE":
            p[0] = ptr_var_type
            return

        if ptr_var_type[0] == 'POINTER':

            if ptr_var_type[1] == "NIL":
                print_semantic_error(
                    f"Cannot dereference a NIL pointer.", lineno_caret)
                p[0] = ("ERROR_TYPE", "NIL pointer dereference")
            else:
                p[0] = ptr_var_type[1]
        elif ptr_var_type[0] == 'file_type':

            p[0] = ptr_var_type[1]
        else:
            print_semantic_error(
                f"Cannot dereference non-pointer/non-file type {ptr_var_type} with '^'.", lineno_caret)
            p[0] = ("ERROR_TYPE", "Not a pointer/file for ^")

    pass


def p_function_call(p):
    """function_call : ID LPAREN expression_list RPAREN
    | ID LPAREN RPAREN
    | variable DOT ID LPAREN expression_list RPAREN
    | variable DOT ID LPAREN RPAREN
    """
    func_name_token_idx = 1
    arg_expr_types = []

    is_method_call = (len(p) > 3 and p.slice[2].type == 'DOT')
    base_var_type_for_method = None
    lineno_call = 0

    if is_method_call:
        base_var_type_for_method = p[1]
        func_name = p[3]
        func_name_token_idx = 3
        lineno_call = p.lineno(func_name_token_idx)
        if len(p) == 7:
            arg_expr_types = p[5] if p[5] else []
        print_semantic_error(
            f"Object method calls ('{func_name}') are not fully supported yet.", lineno_call)
        p[0] = ("ERROR_TYPE", "Method call not fully supported")
        return

    else:
        func_name = p[1]
        func_name_token_idx = 1
        lineno_call = p.lineno(func_name_token_idx)
        if len(p) == 5:
            arg_expr_types = p[3] if p[3] else []

    func_symbol = lookup_symbol(func_name, lineno_call)

    if not func_symbol:
        p[0] = ("ERROR_TYPE", f"Function {func_name} not found during lookup")
        return

    if func_symbol['kind'] not in ['function', 'predefined_function']:
        print_semantic_error(
            f"'{func_name}' is not a function (kind: {func_symbol['kind']}).", lineno_call)
        p[0] = ("ERROR_TYPE", f"Not a function: {func_name}")
        return

    if func_symbol['kind'] == 'function' and \
       not func_symbol.get('defined', False) and \
       func_symbol.get('is_forward', False):
        print_semantic_error(
            f"Cannot call function '{func_name}' as it only has a FORWARD declaration without a body.", lineno_call)
        p[0] = ("ERROR_TYPE", f"Call to undefined forward function {func_name}")
        return

    return_type = None
    defined_params = []
    valid_args = True

    if func_symbol['kind'] == 'predefined_function':
        return_type = func_symbol.get('type')
        if 'params_check_func' in func_symbol:
            if not func_symbol['params_check_func'](arg_expr_types, lineno_call):
                valid_args = False
        else:
            if arg_expr_types:
                print_semantic_error(
                    f"Predefined function '{func_name}' called with arguments, but has no specific parameter checker.", lineno_call)
                valid_args = False
    elif func_symbol['kind'] == 'function':
        type_tuple = func_symbol.get('type')
        if type_tuple and len(type_tuple) >= 3 and type_tuple[0] == 'FUNCTION_TYPE':
            return_type = type_tuple[2]
        else:
            print_semantic_error(f"Malformed type descriptor for function '{func_name}'.", lineno_call)
            p[0] = ("ERROR_TYPE", f"Malformed type for {func_name}")
            return
        defined_params = func_symbol.get('params', [])
        if len(arg_expr_types) != len(defined_params):
            print_semantic_error(
                f"Incorrect number of arguments for function '{func_name}'. Expected {len(defined_params)}, got {len(arg_expr_types)}.", lineno_call)
            valid_args = False
        else:
            for i, arg_type in enumerate(arg_expr_types):
                if not valid_args: break

                def_param_info = defined_params[i]
                def_param_type = def_param_info['type']
                def_param_mode = def_param_info['mode']

                if arg_type is None or arg_type[0] == "ERROR_TYPE":
                    print_semantic_error(f"Argument {i+1} for function '{func_name}' has an error or is unresolved.", lineno_call)
                    valid_args = False
                    break
                compatibility_context = "assignment"
                if def_param_mode == 'var':
                    if def_param_type != arg_type:
                        print_semantic_error(
                            f"Argument {i+1} for VAR parameter '{def_param_info['name']}' of function '{func_name}' type mismatch. Expected identical type {def_param_type}, got {arg_type}.", lineno_call)
                        valid_args = False
                elif not are_types_compatible(def_param_type, arg_type, context=compatibility_context):
                    print_semantic_error(
                        f"Argument {i+1} for {'CONST ' if def_param_mode == 'const' else ''}parameter '{def_param_info['name']}' of function '{func_name}' type mismatch. Expected compatible with {def_param_type}, got {arg_type}.", lineno_call)
                    valid_args = False

    if not return_type:
        print_semantic_error(f"Could not determine return type for function '{func_name}'.", lineno_call)
        p[0] = ("ERROR_TYPE", f"No return type for {func_name}")
        return

    if valid_args:
        p[0] = return_type
    else:
        p[0] = ("ERROR_TYPE", f"Argument type mismatch or count error for {func_name}")
    pass


def p_expression_list(p):
    """expression_list : expression
    | expression_list COMMA expression"""
    if len(p) == 2:
        if p[1] is None or p[1][0] == "ERROR_TYPE":
            p[0] = [("ERROR_TYPE", "Error in expression list item")]
        else:
            p[0] = [p[1]]
    else:
        if p[3] is None or p[3][0] == "ERROR_TYPE":
            p[1].append(("ERROR_TYPE", "Error in expression list item"))
        else:
            p[1].append(p[3])
        p[0] = p[1]
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

            print(f"\nSyntactic error in line {line_num}, column {column}:")
            print(f"{line_num}: {error_line}")
            print(" " * (column - 1) + "^")
            print(f"Unexpected token '{p.value}' of type {p.type}")

            state = parser.statestack[-1]
            expected = [
                tok for tok in tokens if parser.action[state].get(tok, 0) != 0]
            if expected:
                expected_str = ", ".join(expected)
                print(
                    f"One of the following tokens was expected: {expected_str}")
            else:
                print("Expected tokens could not be determined.")

            if line_num > 1:
                print(f"{line_num-1}: {lines[line_num-2]}")
            if line_num < len(lines):
                print(f"{line_num+1}: {lines[line_num]}")
        else:
            print(
                f"\nSintactic error of type {p.type}, value '{p.value}', line {p.lineno}"
            )
            print(
                f"WARNING: The line {p.lineno} is outside the range of file(1-{len(lines)})"
            )

        raise SyntaxError(
            f"Sintactic error in line {p.lineno}, column {column}: unexpected token '{p.type}'"
        )
    else:
        print("\nSintactic error at end of file (EOF).")
        raise SyntaxError("Syntactic error: unexpected end of file")


parser = yacc.yacc()
